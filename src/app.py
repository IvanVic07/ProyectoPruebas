from flask import Flask
from flask_restful import Api
from api.models import db, UserModel, AuthorModel, BookModel, LoanModel
from api.controllers import UserRegistration, UserValidation, BookRegistration, AuthorList,AuthorUpdate,AuthorDelete, AuthorRegistration, BookValidation,LoanRegistration,LoanDeletion,LoanUpdate, UserUpdate, UserDelete, BookUpdate, BookDelete



app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos con la aplicación
db.init_app(app)

# Inicializar API
api = Api(app)

# Crear tablas si no existen al inicio de la aplicación
with app.app_context():
    db.create_all()

@app.route("/api/health", methods=['GET'])
def home():
    return {"message": "API está funcionando correctamente"}, 200

api.add_resource(UserRegistration, '/api/users/register')  # Ruta para registrar usuarios
api.add_resource(UserValidation, '/api/users/validate')    # Ruta para validar datos de usuarios

# Rutas para libros
api.add_resource(BookRegistration, '/api/books/register')
api.add_resource(BookValidation, '/api/books/validate')
# Rutas para manejar autores
api.add_resource(AuthorRegistration, '/api/authors/register')
api.add_resource(AuthorList, '/api/authors')

api.add_resource(LoanRegistration, '/api/loans/register')

api.add_resource(UserUpdate, '/api/users/<int:user_id>/update')
api.add_resource(UserDelete, '/api/users/<int:user_id>/delete')
api.add_resource(BookUpdate, '/api/books/<int:book_id>/update')
api.add_resource(BookDelete, '/api/books/<int:book_id>/delete')
api.add_resource(AuthorUpdate, '/api/authors/<int:author_id>/update')
api.add_resource(AuthorDelete, '/api/authors/<int:author_id>/delete')
api.add_resource(LoanDeletion, '/api/loans/<int:loan_id>/delete')
api.add_resource(LoanUpdate, '/api/loans/<int:loan_id>/update')

if __name__ == '__main__':
    app.run(debug=True)
