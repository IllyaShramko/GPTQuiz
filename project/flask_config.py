import flask_mail
from .settings import project
from dotenv import load_dotenv
import os

project.config["MAIL_SERVER"] = "smtp.gmail.com"
project.config["MAIL_PORT"] = 587 
project.config["MAIL_USE_TLS"] = True
project.config["MAIL_USE_SSL"] = False
project.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
project.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
project.config["MAIL_DEFAULT_SENDER"] = ("GPTQuiz", "test.python.1488@gmail.com")

mail = flask_mail.Mail(project)
