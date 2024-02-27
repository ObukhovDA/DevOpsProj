from flask import Flask, render_template, request, send_from_directory, flash
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import math
from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)

application = app

app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from auth import bp as auth_bp, init_login_manager
from items import bp as items_bp
from comments import bp as comments_bp


app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)
app.register_blueprint(comments_bp)


init_login_manager(app)

from models import *

@app.route('/')
def index():
    # try:
        ITEMS_PER_PAGE = 4
        page = request.args.get('page', 1, type=int)

        items = db.session.execute(db.select(Item).limit(ITEMS_PER_PAGE).offset(ITEMS_PER_PAGE * (page - 1))).scalars()

        page_count = math.ceil(db.session.query(Item).count() / ITEMS_PER_PAGE) or 1
                
        return render_template(
            'index.html',
            items = items,
            page = page,
            page_count = page_count,
        )
    # except:
    #     flash("Ошибка при загрузке данных",'danger')
    #     return render_template(
    #         'index.html',
    #         items = [],
    #         page = 1,
    #         page_count = 1,
    #     )
        
@app.route('/images/<image_id>')
def image(image_id):
    img = db.get_or_404(Image, image_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               img.storage_filename)
