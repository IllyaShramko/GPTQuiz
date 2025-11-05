import flask_mail
from .settings import project
from dotenv import load_dotenv
import os

load_dotenv()

project.config["MAIL_SERVER"] = "smtp.gmail.com"
project.config["MAIL_PORT"] = 465
project.config["MAIL_USE_TLS"] = False
project.config["MAIL_USE_SSL"] = True
project.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
project.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
project.config["MAIL_DEFAULT_SENDER"] = ("GPTQuiz", "test.python.1488@gmail.com")

mail = flask_mail.Mail(project)
