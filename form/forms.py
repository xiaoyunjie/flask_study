# -*- coding:utf-8 -*-

"""
@Author     :   Browser
@file       :   forms.py 
@time       :   2019/07/22
@software   :   PyCharm 
@description:   " "
"""

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,IntegerField,TextAreaField,MultipleFileField
from wtforms.validators import DataRequired,Length,ValidationError,Email
from flask_wtf.file import FileAllowed,FileRequired,FileField
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class FortyTwoForm(FlaskForm):
    answer = IntegerField('The number')
    submit = SubmitField()

    def validate_answer(form,field):
        if field.data != 42:
            raise ValidationError('Must be 42!!')

class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField()

class MultiUploadForm(FlaskForm):
    photo = MultipleFileField('Upload Image',validators=[DataRequired()])
    submit = SubmitField()

class RichTextForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,50)])
    body = CKEditorField('Body',validators=[DataRequired()])
    submit = SubmitField('Publish')

class NewPostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,50)])
    body = TextAreaField('Body',validators=[DataRequired()])
    save = SubmitField('Save')
    publish = SubmitField('Publish')

class SigninForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(1,20)])
    password = PasswordField('Password',validators=(DataRequired(),Length(8,128)))
    submit1 = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(1,20)])
    email = StringField('Email',validators=[DataRequired(),Email(),Length(1,254)])
    password = PasswordField('Password',validators=[DataRequired(),Length(8,128)])
    submit2 = SubmitField()

