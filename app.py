from flask import Flask, render_template, url_for, redirect, request, session, abort
from database import db, desc
from flask_migrate import Migrate
from models import User, Blog, Comentario
from forms import UserForm, BlogForm, ComentarioForm
from datetime import date

app = Flask(__name__)
#USER_DB = "postgres"
#PASS_DB = "admin"
#URL_DB = "localhost"
#NAME_DB = "blog_flask_db"
#FULL_URL_DB = f"postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}"

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://blog_pro_5toj_user:fAV5y3fEdxo1k9Q6s5OW9ulTrYtzl7kW@dpg-d04lejqdbo4c73eng2vg-a.oregon-postgres.render.com/blog_pro_5toj"



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
    if request.method == "POST" and usuarioForm.validate_on_submit():
        usuarioForm.populate_obj(usuario)
        usuario_existente = User.query.filter_by(usuario=usuario.usuario).first()
        if usuario_existente and usuario_existente.contraseña == usuario.contraseña:
            session["usuario"] = usuario.usuario
            return redirect(url_for("inicio"))
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
        if usuario_existente is None:
            db.session.add(usuario)
            db.session.commit()
            session["usuario"] = usuario.usuario
            return redirect(url_for("inicio"))
        error_usuario = "Usuario ya existente"
    return render_template("registro.html", form=usuarioForm, error=error_usuario)

@app.route("/ver_usuario")
def ver_usuario():
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    return render_template("ver_usuario.html", usuario=usuario)

@app.route("/editar_usuario/<string:data>", methods=["GET","POST"])
def editar_usuario(data):
    usuario = User.query.filter_by(usuario=session["usuario"]).first()
    if not usuario:
        return abort(404)
    usuarioForm = UserForm(obj=usuario)
    if request.method == "POST":
        if usuarioForm.validate_on_submit():
            usuarioForm.populate_obj(usuario)
            db.session.commit()
            session["usuario"] = usuario.usuario
        return redirect(url_for("ver_usuario"))
    if data == "nombre":
        return render_template("editar_nombre.html", form=usuarioForm)
    elif data == "contraseña":
        return render_template("editar_contraseña.html", form=usuarioForm)
    return abort(404)

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
        comentario_nuevo.usuario = session["usuario"]
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
        blog.usuario = session["usuario"]
        blog.fecha = date.today()
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("agregar_mensaje.html", form=blogForm, usuario=usuario)

@app.route("/editar_mensaje/<int:id>", methods=["GET","POST"])
def editar_mensaje(id):
    blog = Blog.query.get_or_404(id)
    if blog.usuario != session["usuario"]:
        abort(404)
    blogForm = BlogForm(obj=blog)
    if request.method == "POST" and blogForm.validate_on_submit():
        blogForm.populate_obj(blog)
        blog.usuario = session["usuario"]
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