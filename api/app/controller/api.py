from flask_restful import Resource
from flask_restful import fields, marshal_with, reqparse, marshal
from app.utils.validation import ListValidationError, CardValidationError, CardsValidationError, UserValidationError, ExportImportValidationError
from app.data.database import db
from app.data.models import User, List, Card
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
import json
import pandas as pd
from flask import send_file
from flask import current_app as app
from app.jobs import tasks
import werkzeug
from app.data import data_access
from time import perf_counter
from app.data.cache import cache
from app.jobs.workers import celery


create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument('username')
create_user_parser.add_argument('email')
create_user_parser.add_argument('password')

auth_user_parser = reqparse.RequestParser()
auth_user_parser.add_argument('email')
auth_user_parser.add_argument('password')


create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('name')

update_list_parser = reqparse.RequestParser()
update_list_parser.add_argument('name')

import_csv_parser = reqparse.RequestParser()
import_csv_parser.add_argument(
    'file', type=werkzeug.datastructures.FileStorage, location='files')

user_login_output_fields = {
    "token": fields.String,
    "id": fields.Integer,
    "username": fields.String
}


card_output_fields = {
    "card_id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "deadline": fields.String,
    "completed": fields.Integer,
    "list": fields.Integer,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
    "completed_datetime": fields.DateTime,
}

list_output_fields = {
    "list_id": fields.Integer,
    "name": fields.String,
    "user": fields.Integer,
    'cards': fields.List(fields.Nested(card_output_fields)),
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
}


user_summary_output_fields = {
    "list_id": fields.Integer,
    "list_name": fields.String,
    "total": fields.Integer,
    "total_completed": fields.Integer,
    "total_incomplete": fields.Integer,
    "d_passed": fields.Integer,
    'date_count': fields.List(fields.String),
    "date_labels": fields.List(fields.String),
    "date_data": fields.List(fields.String),
}


other_response = {
    "message": fields.String
}


create_card_parser = reqparse.RequestParser()
create_card_parser.add_argument('title')
create_card_parser.add_argument('content')
create_card_parser.add_argument('deadline')
create_card_parser.add_argument('completed')
create_card_parser.add_argument('list')

update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument('list')
update_card_parser.add_argument('title')
update_card_parser.add_argument('content')
update_card_parser.add_argument('deadline')
update_card_parser.add_argument('completed')

move_cards_parser = reqparse.RequestParser()
move_cards_parser.add_argument('from_list_id')
move_cards_parser.add_argument('to_list_id')


class UserAPI(Resource):
    # logout a user
    @jwt_required()
    @marshal_with(other_response)
    def get(self):
        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        response = {
            "message": "User has been logged out successfully"
        }

        return response, 200

    # create a user
    @marshal_with(other_response)
    def post(self):
        args = create_user_parser.parse_args()
        username = args.get("username", None)
        email = args.get("email", None)
        password = args.get("password", None)

        if username is None:
            raise UserValidationError(
                status_code=400, error_code="U101", error_message="username is required")

        if email is None:
            raise UserValidationError(
                status_code=400, error_code="U102", error_message="email is required")

        if password is None:
            raise UserValidationError(
                status_code=400, error_code="U103", error_message="password is required")

        if len(username) < 4 or len(username) > 24:
            raise UserValidationError(
                status_code=400, error_code="U109", error_message="Username must be minimum 4 and maximum 24 characters in length")

        if len(password) < 6 or len(password) > 36:
            raise UserValidationError(
                status_code=400, error_code="U110", error_message="Password must be minimum 6 and maximum 36 characters in length")

        user_with_email = User.query.filter(User.email == email).first()

        if user_with_email:
            raise UserValidationError(
                status_code=403, error_code="U105", error_message="User with this email already exits")

        user_with_username = User.query.filter(
            User.username == username).first()

        if user_with_username:
            raise UserValidationError(
                status_code=403, error_code="U106", error_message="This username is already taken")

        hashed = generate_password_hash(password, method='sha256')

        new_user = User(username=username, email=email, password=hashed)
        db.session.add(new_user)
        db.session.commit()

        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        response = {
            "message": "User registered successfully"
        }

        return response, 200


class AuthAPI(Resource):
    # authenticate a user
    @marshal_with(user_login_output_fields)
    def post(self):
        args = auth_user_parser.parse_args()
        email = args.get("email", None)
        password = args.get("password", None)

        if email is None:
            raise UserValidationError(
                status_code=400, error_code="U102", error_message="email is required")

        if password is None:
            raise UserValidationError(
                status_code=400, error_code="U103", error_message="password is required")

        user = User.query.filter(User.email == email).first()

        if user is None:
            raise UserValidationError(
                status_code=404, error_code="U104", error_message="User does not exist")

        check_password = check_password_hash(user.password, password)

        if not check_password:
            raise UserValidationError(
                status_code=400, error_code="U108", error_message="Incorrect password")

        access_token = create_access_token(identity=user.id)

        response = {
            "token": access_token,
            "id": user.id,
            "username": user.username
        }

        return response, 200


class ListsAPI(Resource):
    @jwt_required()
    @marshal_with(list_output_fields)
    def get(self):  # get all lists by current user(user id)
        current_user = get_jwt_identity()
        # t1_start = perf_counter()
        lists = data_access.get_lists_by_user(current_user)
        # t1_stop = perf_counter()
        # print("Elapsed time during the whole program in seconds:",
        #       t1_stop-t1_start)

        return lists, 200


class ListAPI(Resource):
    @jwt_required()
    @marshal_with(list_output_fields)
    def get(self, id):  # get a list by id
        list = List.query.get(id)

        if list:
            return list, 200
        else:
            raise ListValidationError(
                status_code=404, error_code="L104", error_message="List does not exist")

    @jwt_required()
    @marshal_with(list_output_fields)
    def post(self):  # create a list for a user
        args = create_list_parser.parse_args()
        name = args.get("name", None)

        current_user = get_jwt_identity()
        user_id = current_user

        if name is None:
            raise ListValidationError(
                status_code=400, error_code="L101", error_message="name is required")

        if user_id is None:
            raise ListValidationError(
                status_code=400, error_code="L102", error_message="user id is required")

        user = User.query.get(user_id)

        if user is None:
            raise UserValidationError(status_code=404,
                                      error_code="U104", error_message="User does not exist")

        lists = db.session.query(List).filter((List.user == user_id)).all()

        if len(lists) > 4:
            raise ListValidationError(status_code=400, error_code="L103",
                                      error_message="Cannot create more than 5 lists for a user")

        new_list = List(name=name, user=user_id)

        db.session.add(new_list)
        db.session.commit()
        db.session.refresh(new_list)

        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        return new_list, 201

    @jwt_required()
    @marshal_with(list_output_fields)
    def put(self, id):  # update a list by id
        args = update_list_parser.parse_args()
        name = args.get('name', None)

        if name is None:
            raise ListValidationError(
                status_code=400, error_code="L101", error_message="name is required")

        list = List.query.get(id)

        if list is None:
            raise ListValidationError(
                status_code=404, error_code="L104", error_message="List does not exist")

        list.name = name
        db.session.add(list)
        db.session.commit()

        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        return list, 200

    @jwt_required()
    def delete(self, id):  # delete a list by id
        list = List.query.get(id)

        if list is None:
            raise ListValidationError(
                status_code=404, error_code="L104", error_message="List does not exist")

        db.session.delete(list)
        db.session.commit()

        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        response = {
            "message": "List has been deleted successfully"
        }

        return response, 200


class CardsAPI(Resource):
    @jwt_required()
    @marshal_with(other_response)
    def post(self):
        args = move_cards_parser.parse_args()
        from_list_id = args.get('from_list_id', None)
        to_list_id = args.get('to_list_id', None)

        if from_list_id is None:
            raise CardsValidationError(
                status_code=400, error_code="CS101", error_message="from_list_id is required")

        if to_list_id is None:
            raise CardsValidationError(
                status_code=400, error_code="CS102", error_message="to_list_id is required")

        cards = Card.query.filter(Card.list == from_list_id).all()

        print(cards)

        update_list = []

        for c in cards:
            update_list.append({"card_id": c.card_id, "list": to_list_id})

        list_to_delete = List.query.get(from_list_id)

        db.session.bulk_update_mappings(
            Card,
            update_list
        )

        db.session.commit()

        db.session.delete(list_to_delete)

        db.session.commit()

        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        response = {
            "message": "Cards moved and list deleted"
        }

        return response, 200


class CardAPI(Resource):
    @jwt_required()
    @marshal_with(card_output_fields)
    def get(self, id):  # get a card by id
        card = Card.query.get(id)

        if card:
            return card, 200
        else:
            raise CardValidationError(
                status_code=404, error_code="C106", error_message="Card does not exist")

    @jwt_required()
    @marshal_with(card_output_fields)
    def post(self):  # create a card for a list
        args = create_card_parser.parse_args()
        title = args.get("title", None)
        content = args.get("content", None)
        deadline = args.get("deadline", None)
        completed = args.get("completed", None)
        list = args.get("list", None)

        if title is None:
            raise CardValidationError(
                status_code=400, error_code="C101", error_message="title is required")

        if content is None:
            raise CardValidationError(
                status_code=400, error_code="C102", error_message="content is required")

        if deadline is None:
            raise CardValidationError(
                status_code=400, error_code="C103", error_message="deadline is required")

        if completed is None:
            raise CardValidationError(
                status_code=400, error_code="C104", error_message="completed flag is required")

        if list is None:
            raise CardValidationError(
                status_code=400, error_code="C105", error_message="list id is required")

        list_q = List.query.get(list)

        if list_q is None:
            raise ListValidationError(
                status_code=404, error_code="L104", error_message="List does not exist")

        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()

        completed_datetime = None

        if completed == '1':
            completed_datetime = datetime.now()

        new_card = Card(title=title, content=content, deadline=deadline,
                        completed=completed, list=list, completed_datetime=completed_datetime)

        db.session.add(new_card)
        db.session.commit()
        db.session.refresh(new_card)

        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        return new_card, 201

    @jwt_required()
    @marshal_with(card_output_fields)
    def put(self, id):  # update a card by id
        args = update_card_parser.parse_args()
        list = args.get('list', None)
        title = args.get("title", None)
        content = args.get("content", None)
        deadline = args.get("deadline", None)
        completed = args.get("completed", None)

        if title is None:
            raise CardValidationError(
                status_code=400, error_code="C101", error_message="title is required")

        if content is None:
            raise CardValidationError(
                status_code=400, error_code="C102", error_message="content is required")

        if deadline is None:
            raise CardValidationError(
                status_code=400, error_code="C103", error_message="deadline is required")

        if completed is None:
            raise CardValidationError(
                status_code=400, error_code="C104", error_message="completed flag is required")

        if list is None:
            raise CardValidationError(
                status_code=400, error_code="C105", error_message="list id is required")

        list_q = List.query.get(list)

        if list_q is None:
            raise ListValidationError(
                status_code=404, error_code="L104", error_message="List does not exist")

        card = Card.query.get(id)

        if card is None:
            raise CardValidationError(
                status_code=404, error_code="C106", error_message="Card does not exist")

        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()

        completed_datetime = None

        if completed == '1':
            completed_datetime = datetime.now()

        card.title = title
        card.content = content
        card.deadline = deadline
        card.completed = completed
        card.completed_datetime = completed_datetime
        card.list = list

        db.session.add(card)
        db.session.commit()

        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        return card, 200

    @jwt_required()
    @marshal_with(card_output_fields)
    def patch(self, card_id, list_id):  # move a card to another list
        if list_id is None:
            raise CardValidationError(
                status_code=400, error_code="C105", error_message="list id is required")

        list_q = List.query.get(list_id)

        if list_q is None:
            raise ListValidationError(
                status_code=404, error_code="L104", error_message="List does not exist")

        card = Card.query.get(card_id)

        if card is None:
            raise CardValidationError(
                status_code=404, error_code="C106", error_message="Card does not exist")

        card.list = list_id

        db.session.add(card)
        db.session.commit()

        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        return card, 200

    @jwt_required()
    @marshal_with(other_response)
    def delete(self, id):  # delete a card by id
        card = Card.query.get(id)

        if card is None:
            raise CardValidationError(
                status_code=404, error_code="C106", error_message="Card does not exist")

        db.session.delete(card)
        db.session.commit()

        cache.delete_memoized(data_access.get_lists_by_user)
        cache.delete_memoized(data_access.get_summary_by_user)

        response = {
            "message": "Card has been deleted successfully"
        }

        return response, 200


class SummaryAPI(Resource):
    @jwt_required()
    @marshal_with(user_summary_output_fields)
    def get(self):  # get summary data of the user
        current_user = get_jwt_identity()

        user_summary = data_access.get_summary_by_user(current_user)

        return user_summary


class ExportAPI(Resource):
    @jwt_required()
    def get(self):  # run the async job of export csv
        current_user = get_jwt_identity()

        job = tasks.export_data.delay(current_user)
        result = job.wait()

        return send_file(f'{app.static_folder}/csv/{result["file_name"]}', as_attachment=True)

    @jwt_required()
    def post(self):
        args = import_csv_parser.parse_args()
        csv_file = args.get('file', None)

        current_user = get_jwt_identity()

        if csv_file is None:
            raise ExportImportValidationError(
                status_code=400, error_code="EI101", error_message="csv file is required")

        csv_file.save(f'{app.static_folder}/csv/user_{current_user}_data.csv')

        try:
            df = pd.read_csv(
                f'{app.static_folder}/csv/user_{current_user}_data.csv')
        except:
            raise ExportImportValidationError(
                status_code=400, error_code="EI103", error_message="The file has no data")

        if list(df.columns) != ['list_id', 'name']:
            raise ExportImportValidationError(
                status_code=400, error_code="EI102", error_message="Invalid csv file")

        for i in range(len(df)):
            cache.delete_memoized(data_access.get_lists_by_user)
            cache.delete_memoized(data_access.get_summary_by_user)
            lists = List.query.filter(List.user == current_user).all()
            if len(lists) > 4:
                raise ListValidationError(status_code=400, error_code="L103",
                                          error_message="Cannot create more than 5 lists for a user")
            data = df.iloc[i]
            new_list = List(name=data['name'], user=current_user)
            db.session.add(new_list)
            db.session.commit()

        response = {
            "message": "Data imported successfully"
        }

        return response, 200


class ExportByListAPI(Resource):
    @jwt_required()
    def get(self, id):  # run the async job of export csv by list_id

        job = tasks.export_data_by_list_id.delay(id)
        result = job.wait()

        return send_file(f'{app.static_folder}/csv/{result["file_name"]}', as_attachment=True)
