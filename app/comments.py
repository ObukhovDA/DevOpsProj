from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from models import Item, Comment
from flask_login import login_required, current_user

import bleach

bp = Blueprint('comments', __name__, url_prefix='/comments')

REVIEW_PARAMS = [
    'text', 'rating'
]

def params():
    return { p: request.form.get(p) for p in REVIEW_PARAMS }

@bp.route('/create/<int:item_id>', methods=['GET', 'POST'])
@login_required
def create(item_id):
    if request.method == 'GET':
        # try:
            if current_user.can_write_comment(item_id):
                item = Item.query.filter_by(id=item_id).scalar()
                return render_template('comments/add.html', item=item)
            else:
                flash('Вы уже писали отзыв на данный товар', 'warning')
                return redirect(url_for('index'))
        # # except:
        #     flash('Ошибка при отображении данных', 'danger')
        #     return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            params_from_form = params()
            for param in params_from_form:
                param = bleach.clean(param)
            print(params_from_form)
            comment = Comment(
                item_id = item_id,
                user_id = current_user.id,
                text = params_from_form['text'],
                rating = params_from_form['rating'],
            )
            db.session.add(comment)
            db.session.commit()
            flash('Отзыв добавлен', 'success')
            return redirect(url_for('items.info', item_id=item_id))
        except:
            flash('Ошибка при сохранении', 'danger')
            return redirect(url_for('index'))
        


