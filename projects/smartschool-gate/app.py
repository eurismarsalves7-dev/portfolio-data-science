import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from database import AccessEvent, Vehicle, db
from plate_reader import extract_plate

load_dotenv()

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_IMAGE_BYTES = 8 * 1024 * 1024

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-only-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///smartschool_gate.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = MAX_IMAGE_BYTES

db.init_app(app)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
def index():
    recent_events = AccessEvent.query.order_by(AccessEvent.created_at.desc()).limit(10).all()
    return render_template("index.html", events=recent_events, result=None)


@app.post("/scan")
def scan():
    uploaded = request.files.get("vehicle_image")
    if not uploaded or not uploaded.filename:
        flash("Selecione uma imagem para analisar.", "warning")
        return redirect(url_for("index"))
    if not allowed_file(uploaded.filename):
        flash("Formato inválido. Use JPG, JPEG, PNG ou WEBP.", "danger")
        return redirect(url_for("index"))

    # Read the uploaded image in memory; do not save it to disk.
    raw = uploaded.read(MAX_IMAGE_BYTES + 1)
    if len(raw) > MAX_IMAGE_BYTES:
        flash("A imagem ultrapassa o limite de 8 MB.", "danger")
        return redirect(url_for("index"))
    if not raw:
        flash("O arquivo enviado está vazio.", "danger")
        return redirect(url_for("index"))

    detected_plate, ocr_text = extract_plate(raw)
    vehicle = None
    status = "plate_not_detected"
    message = "Não foi possível identificar uma placa com confiança. Faça uma verificação manual."

    if detected_plate:
        vehicle = Vehicle.query.filter_by(plate=detected_plate, authorized=True).first()
        if vehicle:
            status = "authorized_vehicle_found"
            message = "Placa encontrada no cadastro de demonstração. Confirme a identidade e a autorização manualmente."
        else:
            status = "vehicle_not_authorized_or_unknown"
            message = "Placa não encontrada entre os veículos autorizados de demonstração. Encaminhe para verificação manual."

    event = AccessEvent(
        plate=detected_plate,
        status=status,
        created_at=datetime.now(timezone.utc),
    )
    db.session.add(event)
    db.session.commit()

    result = {
        "plate": detected_plate or "Não identificada",
        "message": message,
        "status": status,
        "ocr_text": ocr_text,
        "vehicle": vehicle,
    }
    recent_events = AccessEvent.query.order_by(AccessEvent.created_at.desc()).limit(10).all()
    return render_template("index.html", events=recent_events, result=result)


@app.errorhandler(413)
def too_large(_error):
    flash("A imagem ultrapassa o limite de 8 MB.", "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # Local demo only. Use a production WSGI server and secure configuration for deployment.
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
