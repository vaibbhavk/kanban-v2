import time
from app.jobs.workers import celery
from datetime import datetime
from flask import current_app as app
from celery.schedules import crontab
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from app.utils.daily_reminder_template import t
from app.utils.per_user_progress_report import pur
from app.utils.user_report_inform import user_report_inform_t
from app.data.database import db
from app.data.models import List, User
from flask_restful import marshal, fields
import json
import pandas as pd
from flask import send_file
from flask import current_app as app
import uuid
from weasyprint import HTML

card_by_list_id_output_fields = {
    "card_id": fields.Integer,
    "title": fields.String,
    "content": fields.String,
    "deadline": fields.String,
    "completed": fields.Integer,
    "list_id": fields.Integer,
    "list_name": fields.String,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
    "completed_datetime": fields.DateTime,
}

list_output_fields = {
    "list_id": fields.Integer,
    "name": fields.String,
}


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=17, minute=30),
                             send_reminder_email.s(), name='everyday at 5:30 PM')


# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0,
#                              send_reminder_email.s(), name='every 10 seconds reminder')

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=0, minute=0, day_of_month=1),
                             generate_report.s(), name='first day of every month at 12:00 AM')


# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0,
#                              generate_report.s(), name='every 10 seconds generate report')


def render_jinja(t, body):
    template = Template(t)
    message = template.render(data=body)
    return message


def get_users_summary():
    users = User.query.all()

    output = []

    for u in users:
        user_data = {"id": u.id, "email": u.email,
                     "username": u.username, "total_incomplete": 0}
        lists = List.query.filter(List.user == u.id).all()
        if lists != []:
            for l in lists:
                if l.cards != []:
                    for c in l.cards:
                        if c.completed == 0:
                            user_data['total_incomplete'] += 1
        if user_data['total_incomplete'] > 0:
            output.append(user_data)

    return output


def get_user_summary(id):
    users = User.query.all()

    output = []

    for u in users:
        user_data = {"id": u.id, "email": u.email,
                     "username": u.username, "total_incomplete": 0}
        lists = List.query.filter(List.user == u.id).all()
        if lists != []:
            for l in lists:
                if l.cards != []:
                    for c in l.cards:
                        if c.completed == 0:
                            user_data['total_incomplete'] += 1
        if user_data['total_incomplete'] > 0:
            output.append(user_data)

    return output


def per_user_progress_report(user_id):
    lists = List.query.filter(List.user == user_id).all()
    u = User.query.get(user_id)
    user_summary = {"id": u.id, "email": u.email,
                    "username": u.username, "total_completed": 0, 'total': 0}
    if lists != []:
        for l in lists:
            if l.cards != []:
                for c in l.cards:
                    user_summary['total'] += 1
                    if c.completed == 1:
                        user_summary['total_completed'] += 1

    return user_summary


@celery.task()
def send_reminder_email():
    summary = get_users_summary()

    if summary != []:
        for s in summary:
            message = None
            body = {
                'username': s['username'],
                "total_incomplete": s['total_incomplete'],
            }
            message = render_jinja(t, body)

            msg = MIMEMultipart()
            msg['FROM'] = app.config['SENDER_ADDRESS']
            msg['To'] = s['email']
            msg["Subject"] = 'Task Pending'

            msg.attach(MIMEText(message, "html"))

            s = smtplib.SMTP(
                host=app.config["SMTP_SERVER_HOST"], port=app.config["SMTP_SERVER_PORT"])
            s.login(app.config["SENDER_ADDRESS"],
                    app.config["SENDER_PASSWORD"])
            s.send_message(msg)
            s.quit()

        return "Main sent!"

    return "No task pending"


def create_pdf_report(data, user):
    message = render_jinja(pur, data)
    html = HTML(string=message)
    html.write_pdf(target=f'static/pdf/{user.username}.pdf')


@celery.task()
def generate_report():
    users = User.query.all()

    for u in users:
        report = per_user_progress_report(u.id)

        create_pdf_report(report, u)

        body = {
            "username": u.username,
        }

        message = render_jinja(user_report_inform_t, body)

        msg = MIMEMultipart()
        msg['FROM'] = app.config['SENDER_ADDRESS']
        msg['To'] = u.email
        msg["Subject"] = 'Task Pending'

        msg.attach(MIMEText(message, "html"))

        with open(f'static/pdf/{u.username}.pdf', "rb") as att:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(att.read())

        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        f'attachment; filename={u.username}.pdf')

        msg.attach(part)

        s = smtplib.SMTP(
            host=app.config["SMTP_SERVER_HOST"], port=app.config["SMTP_SERVER_PORT"])
        s.login(app.config["SENDER_ADDRESS"],
                app.config["SENDER_PASSWORD"])
        s.send_message(msg)
        s.quit()

    return "Mail sent!"


@celery.task()
def export_data(user_id):
    user = User.query.get(user_id)
    file_name = f'{user.username}_report.csv'
    lists = List.query.filter(List.user == user.id).all()
    output = []
    for l in lists:
        l_dict = {}
        l_dict["list_id"] = l.list_id
        l_dict["name"] = l.name
        list_data = marshal(l_dict, list_output_fields)
        output.append(list_data)

    dumped = json.dumps(output)
    df = pd.read_json(dumped)
    df.to_csv(f'static/csv/{file_name}', index=False)

    result = {
        "file_name": file_name
    }
    return result


@celery.task()
def export_data_by_list_id(list_id):
    l = List.query.filter(List.list_id == list_id).first()
    file_name = f'{list_id}_report.csv'
    cards = []
    for c in l.cards:
        c_dict = {"card_id": c.card_id,
                  "title": c.title, "content": c.content, "deadline": c.deadline, "completed": c.completed, "created_at": c.created_at,
                  "updated_at": c.updated_at, "completed_datetime": c.completed_datetime, }
        c_dict["list_id"] = l.list_id
        c_dict["list_name"] = l.name
        card_data = marshal(c_dict, card_by_list_id_output_fields)
        cards.append(card_data)

    dumped = json.dumps(cards)
    df = pd.read_json(dumped)
    df.to_csv(f'static/csv/{file_name}', index=False)

    result = {
        "file_name": file_name
    }
    return result
