from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db, app
from models import Item, Comment, Image
from flask_login import login_required
from auth import check_rights
from saver import ImageSaver
import bleach, os

bp = Blueprint('items', __name__, url_prefix='/items')

BOOK_PARAMS = [
    'title', 'description', 'price'
]

def params():
    return { p: request.form.get(p) for p in BOOK_PARAMS }

@bp.route('/create', methods=['GET','POST'])
@login_required
@check_rights('create_item')
def create():
        if request.method == 'POST':
            # try:
                params_from_form = params()
                for param in params_from_form:
                    param = bleach.clean(param)
                
                item = Item(**params_from_form)

                image = request.files.get('image')
                if image and image.filename:
                    image = ImageSaver(image).save()
                    if image is None:
                        return(redirect(url_for('index')))
                    item.image_id = image.id

                db.session.add(item)
                db.session.commit()

                flash(f'Информация о "{item.title}" успешно добавлена', 'success')
                return redirect(url_for('index'))
            # except:
                # db.session.rollback()
                # flash('При сохранении возникла ошибка', 'danger')
                # return redirect(url_for('index'))

        try:
            return render_template('items/add.html')
        except:
            db.session.rollback()
            flash('Ошибка при отображении данных', 'danger')
            return redirect(url_for('index'))

@bp.route('/info/<int:item_id>')
def info(item_id):
    try:
        item = db.session.query(Item).get(item_id)
        comments = db.session.execute(db.select(Comment).filter(Comment.item_id == item_id)).scalars()
        return render_template('items/info.html', item=item, comments=comments)
    except:
        flash('Ошибка при загрузке данных', 'danger')
        return redirect(url_for('index'))

@bp.route('/edit/<int:item_id>', methods=['GET','POST'])
@login_required
@check_rights('edit_item')
def edit(item_id):
        if request.method == 'POST':
            try:
                params_from_form = params()
                for param in params_from_form:
                    param = bleach.clean(param)
                book = db.session.execute(db.select(Item).filter(Item.id == item_id)).scalar()

                db.session.query(Item).filter(Item.id == item_id).update(params_from_form)

                db.session.commit()
                
                flash('Информация успешно изменена','success')
                return redirect(url_for('index'))
            except:
                db.session.rollback()
                flash('Ошибка при сохранении изменений', 'danger')
                return redirect(url_for('index'))
            
        try:
            item = db.session.execute(db.select(Item).filter(Item.id == item_id)).scalar()
            return render_template('items/edit.html', item = item)
        except:
            flash('Ошибка при отображении данных', 'danger')
            return redirect(url_for('index'))
          
@bp.route('/delete/<int:item_id>', methods=['POST'])
@login_required
@check_rights('delete_item')
def delete(item_id):
    # try:
        item = db.session.execute(db.select(Item).filter(Item.id == item_id)).scalar()
        
        if db.session.query(Item).filter(Item.image_id == item.image_id).count() < 2:
            image = db.session.execute(db.select(Image).filter(Image.id == item.image_id)).scalar()
            os.remove(
            os.path.join(app.config['UPLOAD_FOLDER'],
                            image.storage_filename))
            db.session.query(Image).filter(Image.id == item.image_id).delete()
        db.session.query(Comment).filter(Comment.item_id == item_id).delete()
        db.session.query(Item).filter(Item.id == item_id).delete()

        db.session.commit()
        flash('Информация удалена', 'success')
        return redirect(url_for('index'))
    # except:
    #     db.session.rollback()
    #     flash('Ошибка при удалении', 'danger')
    #     return redirect(url_for('index'))

        



