import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from api.controllers import UserRegistration, UserValidation, BookRegistration, AuthorList,AuthorUpdate,AuthorDelete, AuthorRegistration, BookValidation,LoanRegistration,LoanDeletion,LoanUpdate, UserUpdate, UserDelete, BookUpdate, BookDelete
from src.app import app as flask_app
import json
from unittest.mock import patch, MagicMock, Mock
from src.app import app, db
from api.models import db, UserModel, AuthorModel, BookModel, LoanModel
from datetime import datetime



@pytest.fixture
def client():
    # Configuración del entorno de prueba
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with flask_app.app_context():
        db.create_all()  # Crear las tablas en la base de datos en memoria

    with flask_app.test_client() as client:
        yield client

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()  # Eliminar las tablas después de la prueba


### TESTS DE USUARIOS ###

def test_register_user(client):
    response = client.post('/api/users/register', json={
        "username": "usuario1",
        "email": "usuario1@test.com"
    })
    assert response.status_code == 201
    assert response.json["message"] == "Usuario registrado exitosamente."


def test_register_user_duplicate(client):
    client.post('/api/users/register', json={
        "username": "usuario1",
        "email": "usuario1@test.com"
    })
    response = client.post('/api/users/register', json={
        "username": "usuario2",
        "email": "usuario1@test.com"
    })
    assert response.status_code == 400
    assert response.json["message"] == "El correo ya está registrado."


def test_update_user(client):
    client.post('/api/users/register', json={
        "username": "usuario1",
        "email": "usuario1@test.com"
    })
    response = client.put('/api/users/1/update', json={
        "username": "usuario_modificado",
        "email": "usuario_modificado@test.com"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Usuario actualizado exitosamente."


def test_delete_user(client):
    client.post('/api/users/register', json={
        "username": "usuario1",
        "email": "usuario1@test.com"
    })
    response = client.delete('/api/users/1/delete')
    assert response.status_code == 200
    assert response.json["message"] == "Usuario eliminado exitosamente."


### TESTS DE AUTORES ###

def test_register_author(client):
    response = client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    assert response.status_code == 201
    assert response.json["message"] == "Autor registrado exitosamente."


def test_update_author(client):
    client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    response = client.put('/api/authors/1/update', json={
        "name": "Autor Actualizado",
        "bio": "Nueva biografía"
    })
    assert response.status_code == 200
    assert response.json["message"] == "Autor actualizado exitosamente."


def test_delete_author(client):
    client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    response = client.delete('/api/authors/1/delete')
    assert response.status_code == 200
    assert response.json["message"] == "Autor eliminado exitosamente."


### TESTS DE LIBROS ###

def test_register_book(client):
    client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    response = client.post('/api/books/register', json={
        "title": "Libro1",
        "author_id": 1
    })
    assert response.status_code == 201
    assert response.json["message"] == "Libro registrado exitosamente."


def test_register_book_duplicate(client):
    client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    client.post('/api/books/register', json={
        "title": "Libro1",
        "author_id": 1
    })
    response = client.post('/api/books/register', json={
        "title": "Libro1",
        "author_id": 1
    })
    assert response.status_code == 400
    assert response.json["message"] == "Ya existe un libro con este título."


def test_update_book(client):
    client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    client.post('/api/books/register', json={
        "title": "Libro1",
        "author_id": 1
    })
    response = client.put('/api/books/1/update', json={
        "title": "Libro Actualizado",
        "author_id": 1
    })
    assert response.status_code == 200
    assert response.json["message"] == "Libro actualizado exitosamente."


def test_delete_book(client):
    client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    client.post('/api/books/register', json={
        "title": "Libro1",
        "author_id": 1
    })
    response = client.delete('/api/books/1/delete')
    assert response.status_code == 200
    assert response.json["message"] == "Libro eliminado exitosamente."


### TESTS DE PRÉSTAMOS ###

def test_register_loan(client):
    client.post('/api/users/register', json={
        "username": "usuario1",
        "email": "usuario1@test.com"
    })
    client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    client.post('/api/books/register', json={
        "title": "Libro1",
        "author_id": 1
    })
    response = client.post('/api/loans/register', json={
        "user_id": 1,
        "book_id": 1
    })
    assert response.status_code == 201
    assert response.json["message"] == "Préstamo registrado exitosamente."


def test_register_loan_duplicate(client):
    client.post('/api/users/register', json={
        "username": "usuario1",
        "email": "usuario1@test.com"
    })
    client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    client.post('/api/books/register', json={
        "title": "Libro1",
        "author_id": 1
    })
    client.post('/api/loans/register', json={
        "user_id": 1,
        "book_id": 1
    })
    response = client.post('/api/loans/register', json={
        "user_id": 1,
        "book_id": 1
    })
    assert response.status_code == 400
    # Cambia según tu preferencia:
    assert response.json["message"] == "El libro ya está prestado y no está disponible."
    # O
    # assert "El libro ya está prestado" in response.json["message"]


def test_return_loan(client):
    client.post('/api/users/register', json={
        "username": "usuario1",
        "email": "usuario1@test.com"
    })
    client.post('/api/authors/register', json={
        "name": "Autor1",
        "bio": "Biografía de Autor1"
    })
    client.post('/api/books/register', json={
        "title": "Libro1",
        "author_id": 1
    })
    client.post('/api/loans/register', json={
        "user_id": 1,
        "book_id": 1
    })
    response = client.put('/api/loans/1/update', json={
        "return_date": str(datetime.now().date())
    })
    assert response.status_code == 200
    assert response.json["message"] == "Préstamo actualizado exitosamente."