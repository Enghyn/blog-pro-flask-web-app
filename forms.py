from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TextAreaField, EmailField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    usuario = StringField("Usuario", validators=[DataRequired()])
    contraseña = PasswordField("Contraseña", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])

class BlogForm(FlaskForm):
    usuario = StringField("Usuario")
    fecha = DateField("Fecha")
    titulo = StringField("Título", validators=[DataRequired()])
    cuerpo = TextAreaField("Mensaje", validators=[DataRequired()])

class ComentarioForm(FlaskForm):
    cuerpo = TextAreaField("Escribe un comentario:", validators=[DataRequired()])