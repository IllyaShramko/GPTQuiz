# import uuid
# import flask_login
# from project.settings import DATABASE
# class Student(DATABASE.Model, flask_login.UserMixin):
#     id= DATABASE.Column(DATABASE.Integer, primary_key= True)

#     login= DATABASE.Column(DATABASE.String(40), nullable= False)
#     name= DATABASE.Column(DATABASE.String(30), nullable= False)
#     surname= DATABASE.Column(DATABASE.String(30), nullable= False)
#     password= DATABASE.Column(DATABASE.String(8), nullable= False, default=lambda: uuid.uuid4().hex)
    
#     is_student = DATABASE.Column(DATABASE.Boolean, default=True)

#     my_reports = DATABASE.relationship("StudentReport", backref='student', lazy=True)

#     my_class_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("class.id"))

# class Class(DATABASE.Model):
#     id= DATABASE.Column(DATABASE.Integer, primary_key= True)

#     teacher_id = DATABASE.Column(DATABASE.Integer, DATABASE.ForeignKey("user.id"))
#     students = DATABASE.relationship("Student", backref="class", lazy=True)