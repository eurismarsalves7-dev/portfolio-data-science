"""Create tables and insert fictional demonstration records."""
from dotenv import load_dotenv

from app import app
from database import Vehicle, db

load_dotenv()

DEMO_VEHICLES = [
    {
        "plate": "ABC1D23",
        "responsible_name": "Responsável de Demonstração",
        "student_name": "Aluno Fictício",
        "class_name": "5º Ano A",
        "room": "Sala 204",
        "authorized": True,
    },
    {
        "plate": "XYZ1234",
        "responsible_name": "Responsável Exemplo",
        "student_name": "Estudante de Teste",
        "class_name": "3º Ano B",
        "room": "Sala 105",
        "authorized": True,
    },
]


with app.app_context():
    db.create_all()
    for item in DEMO_VEHICLES:
        if not Vehicle.query.filter_by(plate=item["plate"]).first():
            db.session.add(Vehicle(**item))
    db.session.commit()
    print("Banco de demonstração pronto. Todos os dados são fictícios.")
