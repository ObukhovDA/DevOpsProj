import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from app import db
from user_policy import UsersPolicy
from sqlalchemy.sql import func, text

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role_id == 1
    
    def is_moder(self):
        return self.role_id == 2
    
    def can(self, action, record=None):
        users_policy = UsersPolicy(record)
        method = getattr(users_policy, action, None)
        if method:
            return method()
        return False
    
    def can_write_comment(self, item_id):
        data = db.session.query(Comment).filter(Comment.item_id == item_id, Comment.user_id == self.id).count()
        if data == 0:
            return True
        else:
            return False

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.login
    
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.title
        

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_id = db.Column(db.String(250), db.ForeignKey('images.id'), nullable=False)

    def __repr__(self):
        return '<Item %r>' % self.title

    def avg_rating(self):
        query = db.session.query(func.avg(Comment.rating).label('average')).filter(Comment.item_id==self.id)
        return db.session.execute(query).scalar()
    
    @property
    def image(self):
        return db.session.execute(db.select(Image).filter_by(id=self.image_id)).scalar()

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())
    
    def get_author_full_name(self):
        return db.session.execute(db.Select(User).filter_by(id = self.user_id)).scalar().full_name
    
    
class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.String(250), primary_key=True)
    file_name = db.Column(db.String(250), nullable=False)
    MIME = db.Column(db.String(250), nullable=False)
    MD5 = db.Column(db.String(150), nullable=False)
    
    def __repr__(self):
        return '<Image %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('image', image_id=self.id)
    
    