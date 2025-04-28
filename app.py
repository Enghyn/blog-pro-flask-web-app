from flask import Flask, render_template, url_for, redirect, request, session, abort
from database import db, desc
from flask_migrate import Migrate
from models import User, Blog, Comentario
from forms import UserForm, BlogForm, ComentarioForm
from datetime import date
from flask_mail import Mail, Message
import secrets

app = Flask(__name__)
USER_DB = "postgres"
PASS_DB = "admin"
URL_DB = "localhost"
NAME_DB = "blog_flask_db"
FULL_URL_DB = f"postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}"
render_external_url = "postgresql://blog_pro_sgdy_user:GvohOVd2gysovaDfKj5sbybx2S1i0fiG@dpg-d04omn1r0fns73cmq9f0-a.oregon-postgres.render.com/blog_pro_sgdy"

app.config["SQLALCHEMY_DATABASE_URI"] = FULL_URL_DB

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'blogpro882@gmail.com'
app.config['MAIL_PASSWORD'] = 'tfvh gfth paiv ntav'
app.config['MAIL_DEFAULT_SENDER'] = 'blogpro882@gmail.com'

mail = Mail(app)

db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)

app.config["SECRET_KEY"]="blog_key"

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def inicio():
    if "usuario" in session:
        usuario = User.query.filter_by(usuario=session["usuario"]).first()
        blogs = Blog.query.order_by(desc("fecha"))
        return render_template("index.html", usuario=usuario, blogs=blogs)
    return redirect(url_for("inicio_sesion"))

@app.route("/inicio_sesion", methods=["GET","POST"])
def inicio_sesion():
    usuario = User()
    usuarioForm = UserForm(obj=usuario)
    error_usuario = None
    usuarioForm.email.data = "None"
    if request.method == "POST" and usuarioForm.validate_on_submit():
        usuarioForm.populate_obj(usuario)
        usuario_existente = User.query.filter_by(usuario=usuario.usuario).first()
        if usuario_existente and usuario_existente.contraseña == usuario.contraseña:
            if usuario_existente.is_verified:
                session["usuario"] = usuario.usuario
                return redirect(url_for("inicio"))
            error_usuario = "Su cuenta no ha sido verificada aún."
            return render_template("inicio_sesion.html", form=usuarioForm, error=error_usuario)
        error_usuario = "Usuario o contraseña incorrectos"
    return render_template("inicio_sesion.html", form=usuarioForm, error=error_usuario)

@app.route("/registro", methods=["GET","POST"])
def registro():
    usuario = User()
    usuarioForm = UserForm(obj=usuario)
    error_usuario = None
    if request.method == "POST" and usuarioForm.validate_on_submit():
        usuarioForm.populate_obj(usuario)
        usuario_existente = User.query.filter_by(usuario=usuario.usuario).first()
        email_existente = User.query.filter_by(email=usuario.email).first()
        if usuario_existente is None and email_existente is None:
            codigo = secrets.token_hex(3).upper()
            usuario.codigo_verificacion = codigo
            usuario.is_verified = False
            db.session.add(usuario)
            db.session.commit()
            session["usuario_email"] = usuario.email
            msg = Message("Código de verificación", sender="blogpro882@gmail.com", recipients=[usuario.email])
            msg.body = f"Tu código de verificación: {codigo}"
            mail.send(msg)
            return redirect(url_for("verificar_codigo"))
        error_usuario = "Usuario o email ya existente"
    return render_template("registro.html", form=usuarioForm, error=error_usuario)

@app.route("/verificar_codigo", methods=["GET", "POST"])
def verificar_codigo():
    error_codigo = None
    if "usuario_email" not in session:
        return redirect(url_for("inicio_sesion"))
    if request.method == "POST":
        codigo_ingresado = request.form.get("codigo")
        usuario = User.query.filter_by(email=session["usuario_email"]).first()
        if usuario and usuario.codigo_verificacion == codigo_ingresado:
            usuario.is_verified = True
            db.session.commit()
            session["usuario"] = usuario.usuario
            session.pop("usuario_email", None)
            return redirect(url_for("inicio"))
        else:
            error_codigo = "Código incorrecto. Intenta de nuevo."
    return render_template("verificar_codigo.html", error=error_codigo)

@app.route("/ver_usuario")
def ver_usuario():
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    return render_template("ver_usuario.html", usuario=usuario)

@app.route("/editar_nombre", methods=["GET","POST"])
def editar_nombre():
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    if not usuario:
        return abort(404)
    usuarioForm = UserForm(obj=usuario)
    error_usuario = None
    if request.method == "POST" and usuarioForm.validate_on_submit():
        usuario_existente = User.query.filter_by(usuario=usuarioForm.usuario.data).first()
        if not usuario_existente and usuario.usuario != usuarioForm.usuario.data:
            usuarioForm.populate_obj(usuario)
            db.session.commit()
            session["usuario"] = usuario.usuario
            return redirect(url_for("ver_usuario"))
        error_usuario = "Usuario ya existente"
    return render_template("editar_nombre.html", form=usuarioForm, error=error_usuario)

@app.route("/editar_contraseña", methods=["GET","POST"])
def editar_contraseña():
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    if not usuario:
        return abort(404)
    usuarioForm = UserForm(obj=usuario)
    if request.method == "POST" and usuarioForm.validate_on_submit():
        usuarioForm.populate_obj(usuario)
        db.session.commit()
        return redirect(url_for("ver_usuario"))
    return render_template("editar_contraseña.html", form=usuarioForm)

@app.route("/eliminar_usuario")
def eliminar_usuario():
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    db.session.delete(usuario)
    db.session.commit()
    session.pop("usuario", None)
    return redirect(url_for("inicio"))

@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.pop("usuario", None)
    return redirect(url_for("inicio"))

@app.route("/detalle_mensaje/<int:id>", methods=["GET","POST"])
def detalle_mensaje(id):
    blog = Blog.query.get_or_404(id)
    comentarios = Comentario.query.filter_by(blog_id=id)
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    comentario_nuevo = Comentario()
    comentarioForm = ComentarioForm(obj=comentario_nuevo)
    if request.method == "POST" and comentarioForm.validate_on_submit():
        comentarioForm.populate_obj(comentario_nuevo)
        comentario_nuevo.blog_id = id
        comentario_nuevo.usuario_id = usuario.id
        db.session.add(comentario_nuevo)
        db.session.commit()
        return redirect(url_for("detalle_mensaje", id=id))
    return render_template("detalle_mensaje.html", usuario=usuario, blog=blog, comentarios=comentarios, cform=comentarioForm)

@app.route("/agregar_mensaje", methods=["GET","POST"])
def agregar_mensaje():
    blog = Blog()
    blogForm = BlogForm(obj=blog)
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    if request.method == "POST" and blogForm.validate_on_submit():
        blogForm.populate_obj(blog)
        blog.usuario_id = usuario.id
        blog.fecha = date.today()
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("agregar_mensaje.html", form=blogForm, usuario=usuario)

@app.route("/editar_mensaje/<int:id>", methods=["GET","POST"])
def editar_mensaje(id):
    blog = Blog.query.get_or_404(id)
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    if blog.usuario_id != usuario.id:
        abort(404)
    blogForm = BlogForm(obj=blog)
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    if request.method == "POST" and blogForm.validate_on_submit():
        blogForm.populate_obj(blog)
        blog.usuario = usuario.id
        blog.fecha = date.today()
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("editar_mensaje.html", form=blogForm)

@app.route("/eliminar_mensaje/<int:id>")
def eliminar_mensaje(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for("inicio"))

@app.errorhandler(404)
def error_404(error):
    return render_template("error404.html", error=error), 404

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)