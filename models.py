from database import db
from datetime import datetime

foto_default_url = "https://res.cloudinary.com/di1j5rbuq/image/upload/v1746024973/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju_wrvwww.webp"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contraseña = db.Column(db.String(255))
    email = db.Column(db.String(120), nullable=True)
    foto = db.Column(db.String(512), default=foto_default_url)
    codigo_verificacion = db.Column(db.String(10), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    blogs = db.relationship("Blog", backref="autor", lazy=True, cascade="all, delete-orphan")
    comentarios = db.relationship("Comentario", backref="autor", lazy=True, cascade="all, delete-orphan")

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    cuerpo = db.Column(db.String(1000))
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id", ondelete="CASCADE"))

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    fecha = db.Column(db.Date)
    titulo = db.Column(db.String(50))
    cuerpo = db.Column(db.String(1000))
    
    comentarios = db.relationship("Comentario", backref="blog", lazy=True, cascade="all, delete-orphan")

