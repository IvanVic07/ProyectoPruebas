from app import app, db
from api.models import UserModel, AuthorModel, BookModel, LoanModel  # Importa los modelos

with app.app_context():
    db.create_all()
    print("Base de datos y tablas creadas correctamente")
