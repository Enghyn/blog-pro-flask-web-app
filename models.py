from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(30))
    contraseña = db.Column(db.String(30))
    blogs = db.relationship("Blog", backref="autor", lazy=True)
    comentarios = db.relationship("Comentario", backref="autor", lazy=True)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(30))
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    cuerpo = db.Column(db.String(1000))
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(30))
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    fecha = db.Column(db.Date)
    titulo = db.Column(db.String(50))
    cuerpo = db.Column(db.String(1000))
    comentarios = db.relationship("Comentario", backref="blog", lazy=True)

