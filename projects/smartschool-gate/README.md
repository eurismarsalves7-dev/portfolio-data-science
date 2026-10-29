# SmartSchool Gate — Protótipo de controle de retirada escolar

**Autor:** Eurismar S. Alves  
**Área:** Python · Visão computacional · OCR · Flask · Banco de dados  
**Status:** Protótipo demonstrativo / prova de conceito

## Sobre o projeto

O SmartSchool Gate é uma proposta para apoiar a organização da saída de alunos. A ideia é ler a placa de um veículo a partir de uma imagem, consultar um cadastro de demonstração e exibir à equipe autorizada informações de retirada.

Este repositório transforma a proposta documentada em um protótipo de software. O PDF original descreve leitura de placas e consulta a cadastro; reconhecimento facial é citado como possível expansão futura, portanto não está implementado neste protótipo.

## Funcionalidades do protótipo

- Upload pontual de uma imagem de veículo pelo painel web.
- OCR com EasyOCR para localizar texto que se pareça com uma placa brasileira.
- Normalização da placa e consulta ao cadastro de veículos autorizados.
- Registro de eventos de demonstração com data e resultado.
- Painel web em Flask.
- PostgreSQL configurável por variável de ambiente; SQLite é usado por padrão para facilitar testes locais.
- Dados fictícios para demonstração.

## Tecnologias

- Python 3.11+
- Flask
- OpenCV
- EasyOCR
- SQLAlchemy
- PostgreSQL (opcional/configurável) ou SQLite para execução local

## Executar localmente

1. Crie um ambiente virtual:

   `python -m venv .venv`

2. Ative o ambiente virtual.

   Windows PowerShell: `.venv\\Scripts\\Activate.ps1`  
   Linux/macOS: `source .venv/bin/activate`

3. Instale as dependências:

   `pip install -r requirements.txt`

4. Copie `.env.example` para `.env` e ajuste as configurações, se necessário.

5. Crie o banco e dados fictícios:

   `python seed_demo.py`

6. Inicie o painel:

   `python app.py`

7. Abra `http://127.0.0.1:5000` no navegador.

Na primeira execução, o EasyOCR pode baixar os modelos de idioma. Para testes, use uma foto própria de um veículo de demonstração, sem pessoas identificáveis nem placas de terceiros.

## Banco PostgreSQL

Defina `DATABASE_URL` no formato:

`postgresql+psycopg://usuario:senha@localhost:5432/smartschool_gate`

Execute o arquivo `schema.sql` no banco escolhido ou rode `python seed_demo.py` para criar as tabelas via SQLAlchemy.

## Limitações importantes

- O OCR é uma prova de conceito e pode errar; a placa detectada deve ser confirmada por uma pessoa autorizada.
- Não existe conexão com câmeras IP ao vivo nesta versão.
- Não existe reconhecimento facial nesta versão.
- Os nomes e registros usados no seed são inteiramente fictícios.
- O sistema não deve autorizar sozinho a entrega de uma criança. A escola deve verificar autorização por um processo seguro e ter procedimento manual alternativo.
- Antes de qualquer piloto real, são necessários avaliação de segurança, controle de acesso, registro de auditoria, política de retenção, consentimento/base legal apropriada e análise de conformidade com a LGPD.
- Não envie imagens, nomes, placas ou informações de alunos reais para este repositório público.

## Estrutura

```
smartschool-gate/
├── app.py
├── database.py
├── plate_reader.py
├── seed_demo.py
├── schema.sql
├── requirements.txt
├── .env.example
└── templates/
    └── index.html
```

## Origem da proposta

Projeto conceitual de portfólio elaborado por Eurismar S. Alves. Este código é uma implementação demonstrativa criada para documentar e testar a ideia; não afirma que houve implantação em uma escola.

## Licença

Consulte o arquivo LICENSE antes de reutilizar ou redistribuir o código.
