from app import db
from api.models import UserModel

with db.session.begin():
    # Eliminar todos los registros de la tabla 'users'
    db.session.query(UserModel).delete()
    db.session.commit()
    print("Todos los datos de la tabla 'users' fueron eliminados.")
