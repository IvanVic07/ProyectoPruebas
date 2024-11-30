from flask_restful import Resource, reqparse
from api.models import UserModel, BookModel, AuthorModel,LoanModel, db
from datetime import datetime


# Configurar el parser para manejar los datos enviados en la solicitud de usuarios
user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=str, required=True, help="El nombre de usuario es obligatorio")
user_parser.add_argument("email", type=str, required=True, help="El correo es obligatorio")

# Configurar el parser para manejar los datos enviados en la solicitud de libros
book_parser = reqparse.RequestParser()
book_parser.add_argument("title", type=str, required=True, help="El título es obligatorio")
book_parser.add_argument("author_id", type=int, required=True, help="El ID del autor es obligatorio")

# Configurar el parser para manejar los datos enviados en la solicitud de autores
author_parser = reqparse.RequestParser()
author_parser.add_argument("name", type=str, required=True, help="El nombre del autor es obligatorio")
author_parser.add_argument("bio", type=str, required=False, help="La biografía es opcional")

# Configurar el parser para manejar los datos enviados en la solicitud de préstamos
loan_parser = reqparse.RequestParser()
loan_parser.add_argument("user_id", type=int, required=True, help="El ID del usuario es obligatorio")
loan_parser.add_argument("book_id", type=int, required=True, help="El ID del libro es obligatorio")

# Clase para registrar usuarios
class UserRegistration(Resource):
    def post(self):
        args = user_parser.parse_args()

        # Verificar si el usuario ya existe
        if UserModel.query.filter_by(email=args["email"]).first():
            return {"message": "El correo ya está registrado."}, 400

        # Crear un nuevo usuario
        new_user = UserModel(username=args["username"], email=args["email"])
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al registrar el usuario.", "error": str(e)}, 500

        return {
            "message": "Usuario registrado exitosamente.",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
            },
        }, 201

#CLASE PARA ACTUALIZAR USUARIOS
class UserUpdate(Resource):
    def put(self, user_id):
        args = user_parser.parse_args()

        # Buscar el usuario por ID
        user = UserModel.query.get(user_id)
        if not user:
            return {"message": "Usuario no encontrado."}, 404

        # Actualizar campos
        user.username = args["username"] or user.username
        user.email = args["email"] or user.email

        try:
            db.session.commit()
            return {"message": "Usuario actualizado exitosamente.", "user": {"id": user.id, "username": user.username, "email": user.email}}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el usuario.", "error": str(e)}, 500

#clase para borrar usuario

class UserDelete(Resource):
    def delete(self, user_id):
        # Buscar el usuario por ID
        user = UserModel.query.get(user_id)
        if not user:
            return {"message": "Usuario no encontrado."}, 404

        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": "Usuario eliminado exitosamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar el usuario.", "error": str(e)}, 500


# Clase para validar datos de usuarios
class UserValidation(Resource):
    def post(self):
        # Intentar registrar un usuario con campos incompletos
        args = user_parser.parse_args()

        # Validar campos obligatorios
        if not args.get("username") or not args.get("email"):
            return {"message": "Faltan datos requeridos: nombre de usuario o correo."}, 400

        return {"message": "Datos completos recibidos correctamente."}, 200

# Clase para registrar libros
class BookRegistration(Resource):
    def post(self):
        args = book_parser.parse_args()

        # Verificar si el autor existe
        author = AuthorModel.query.get(args["author_id"])
        if not author:
            return {"message": "El autor especificado no existe."}, 400

        # Verificar si el libro ya existe con el mismo título
        if BookModel.query.filter_by(title=args["title"]).first():
            return {"message": "Ya existe un libro con este título."}, 400

        # Crear un nuevo libro
        new_book = BookModel(title=args["title"], author_id=args["author_id"])
        try:
            db.session.add(new_book)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al registrar el libro.", "error": str(e)}, 500

        return {
            "message": "Libro registrado exitosamente.",
            "book": {
                "id": new_book.id,
                "title": new_book.title,
                "author_id": new_book.author_id,
                "author_name": author.name
            },
        }, 201

#clase para actualizar libros
class BookUpdate(Resource):
    def put(self, book_id):
        args = book_parser.parse_args()

        # Buscar el libro por ID
        book = BookModel.query.get(book_id)
        if not book:
            return {"message": "Libro no encontrado."}, 404

        # Verificar si el nuevo autor existe
        if args["author_id"]:
            author = AuthorModel.query.get(args["author_id"])
            if not author:
                return {"message": "El autor especificado no existe."}, 400

            book.author_id = args["author_id"]

        # Actualizar título
        book.title = args["title"] or book.title

        try:
            db.session.commit()
            return {"message": "Libro actualizado exitosamente.", "book": {"id": book.id, "title": book.title, "author_id": book.author_id}}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el libro.", "error": str(e)}, 500

#clase para elimianr libros

class BookDelete(Resource):
    def delete(self, book_id):
        # Buscar el libro por ID
        book = BookModel.query.get(book_id)
        if not book:
            return {"message": "Libro no encontrado."}, 404

        try:
            db.session.delete(book)
            db.session.commit()
            return {"message": "Libro eliminado exitosamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar el libro.", "error": str(e)}, 500


#validar libros
class BookValidation(Resource):
    def post(self):
        args = book_parser.parse_args()

        # Validar campos obligatorios
        if not args.get("title") or not args.get("author_id"):
            return {"message": "Faltan datos requeridos: título o ID del autor."}, 400

#registrar nuevo autor  
class AuthorRegistration(Resource):
    def post(self):
        args = author_parser.parse_args()

        # Verificar si el autor ya existe (por nombre)
        if AuthorModel.query.filter_by(name=args["name"]).first():
            return {"message": "El autor ya está registrado."}, 400

        # Crear un nuevo autor
        new_author = AuthorModel(name=args["name"], bio=args.get("bio"))
        try:
            db.session.add(new_author)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al registrar el autor.", "error": str(e)}, 500

        return {
            "message": "Autor registrado exitosamente.",
            "author": {
                "id": new_author.id,
                "name": new_author.name,
                "bio": new_author.bio,
            },
        }, 201

#clase para actualizar autores

class AuthorUpdate(Resource):
    def put(self, author_id):
        args = author_parser.parse_args()

        # Buscar el autor por ID
        author = AuthorModel.query.get(author_id)
        if not author:
            return {"message": "Autor no encontrado."}, 404

        # Actualizar campos
        author.name = args["name"] or author.name
        author.bio = args["bio"] or author.bio

        try:
            db.session.commit()
            return {"message": "Autor actualizado exitosamente.", "author": {"id": author.id, "name": author.name, "bio": author.bio}}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el autor.", "error": str(e)}, 500

#clase para eliminar autor
class AuthorDelete(Resource):
    def delete(self, author_id):
        # Buscar el autor por ID
        author = AuthorModel.query.get(author_id)
        if not author:
            return {"message": "Autor no encontrado."}, 404

        try:
            db.session.delete(author)
            db.session.commit()
            return {"message": "Autor eliminado exitosamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar el autor.", "error": str(e)}, 500

#validar autores
class AuthorList(Resource):
    def get(self):
        # Obtener todos los autores registrados
        authors = AuthorModel.query.all()
        authors_list = [
            {"id": author.id, "name": author.name, "bio": author.bio}
            for author in authors
        ]
        return {"authors": authors_list}, 200
#registrar nuevo prestamo    
class LoanRegistration(Resource):
    def post(self):
        args = loan_parser.parse_args()

        # Verificar si el usuario existe
        user = UserModel.query.get(args["user_id"])
        if not user:
            return {"message": "El usuario especificado no existe."}, 400

        # Verificar si el libro existe
        book = BookModel.query.get(args["book_id"])
        if not book:
            return {"message": "El libro especificado no existe."}, 400

        # Verificar si el libro ya está prestado y no ha sido devuelto
        active_loan = LoanModel.query.filter_by(book_id=args["book_id"], return_date=None).first()
        if active_loan:
            return {"message": "El libro ya está prestado y no está disponible."}, 400

        # Crear un nuevo préstamo
        new_loan = LoanModel(user_id=args["user_id"], book_id=args["book_id"], loan_date=datetime.now().date())
        try:
            db.session.add(new_loan)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al registrar el préstamo.", "error": str(e)}, 500

        return {
            "message": "Préstamo registrado exitosamente.",
            "loan": {
                "id": new_loan.id,
                "user_id": new_loan.user_id,
                "book_id": new_loan.book_id,
                "loan_date": new_loan.loan_date.isoformat(),  # Convierte la fecha a un formato serializable
                "return_date": new_loan.return_date.isoformat() if new_loan.return_date else None
            },
        }, 201
    
#ELIMINAR PRESTAMOS
class LoanDeletion(Resource):
    def delete(self, loan_id):
        # Buscar el préstamo por ID
        loan = LoanModel.query.get(loan_id)
        if not loan:
            return {"message": "Préstamo no encontrado."}, 404

        try:
            db.session.delete(loan)
            db.session.commit()
            return {"message": "Préstamo eliminado exitosamente."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al eliminar el préstamo.", "error": str(e)}, 500

#actualizar prestamo
class LoanUpdate(Resource):
    def put(self, loan_id):
        parser = reqparse.RequestParser()
        parser.add_argument("return_date", type=str, required=False, help="Fecha de devolución en formato YYYY-MM-DD")
        args = parser.parse_args()

        # Buscar el préstamo por ID
        loan = LoanModel.query.get(loan_id)
        if not loan:
            return {"message": "Préstamo no encontrado."}, 404

        # Actualizar los campos
        if args.get("return_date"):
            try:
                loan.return_date = datetime.strptime(args["return_date"], "%Y-%m-%d").date()
            except ValueError:
                return {"message": "Formato de fecha inválido. Use YYYY-MM-DD."}, 400

        try:
            db.session.commit()
            return {
                "message": "Préstamo actualizado exitosamente.",
                "loan": {
                    "id": loan.id,
                    "user_id": loan.user_id,
                    "book_id": loan.book_id,
                    "loan_date": loan.loan_date.strftime("%Y-%m-%d"),
                    "return_date": loan.return_date.strftime("%Y-%m-%d") if loan.return_date else None
                },
            }, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error al actualizar el préstamo.", "error": str(e)}, 500

