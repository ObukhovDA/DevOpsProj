"""empty message

Revision ID: ccb269e2568a
Revises: ef2c890c1fc0
Create Date: 2024-02-23 14:28:16.152613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccb269e2568a'
down_revision = 'ef2c890c1fc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_id', sa.String(length=250), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_items_image_id_images'), 'images', ['image_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_items_image_id_images'), type_='foreignkey')
        batch_op.drop_column('image_id')

    # ### end Alembic commands ###