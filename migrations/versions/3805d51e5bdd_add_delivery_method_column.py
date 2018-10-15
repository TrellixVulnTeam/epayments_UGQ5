"""Add delivery_method column

Revision ID: 3805d51e5bdd
Revises: 175096050ecc
Create Date: 2018-10-02 17:04:57.491971

"""
from alembic import op
from sqlalchemy.dialects import postgresql

import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3805d51e5bdd'
down_revision = '175096050ecc'
branch_labels = None
depends_on = None


def upgrade():
    delivery_method = postgresql.ENUM('mail', 'email', 'pickup', name='delivery_method')
    delivery_method.create(op.get_bind())

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('birth_cert', sa.Column('delivery_method', sa.Enum('mail', 'email', 'pickup', name='delivery_method'),
                                          nullable=True))
    op.add_column('birth_search',
                  sa.Column('delivery_method', sa.Enum('mail', 'email', 'pickup', name='delivery_method'),
                            nullable=True))
    op.add_column('death_cert', sa.Column('delivery_method', sa.Enum('mail', 'email', 'pickup', name='delivery_method'),
                                          nullable=True))
    op.add_column('death_search',
                  sa.Column('delivery_method', sa.Enum('mail', 'email', 'pickup', name='delivery_method'),
                            nullable=True))
    op.add_column('marriage_cert',
                  sa.Column('delivery_method', sa.Enum('mail', 'email', 'pickup', name='delivery_method'),
                            nullable=True))
    op.add_column('marriage_search',
                  sa.Column('delivery_method', sa.Enum('mail', 'email', 'pickup', name='delivery_method'),
                            nullable=True))
    op.add_column('photo_gallery',
                  sa.Column('delivery_method', sa.Enum('mail', 'email', 'pickup', name='delivery_method'),
                            nullable=True))
    op.add_column('tax_photo', sa.Column('delivery_method', sa.Enum('mail', 'email', 'pickup', name='delivery_method'),
                                         nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tax_photo', 'delivery_method')
    op.drop_column('photo_gallery', 'delivery_method')
    op.drop_column('marriage_search', 'delivery_method')
    op.drop_column('marriage_cert', 'delivery_method')
    op.drop_column('death_search', 'delivery_method')
    op.drop_column('death_cert', 'delivery_method')
    op.drop_column('birth_search', 'delivery_method')
    op.drop_column('birth_cert', 'delivery_method')

    op.execute('DROP TYPE delivery_method;')
    # ### end Alembic commands ###
