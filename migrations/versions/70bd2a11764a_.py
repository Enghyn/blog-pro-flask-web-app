"""empty message

Revision ID: 70bd2a11764a
Revises: 9bdc2cd6caf5
Create Date: 2025-04-28 13:21:31.485056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70bd2a11764a'
down_revision = '9bdc2cd6caf5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('codigo_verificacion', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('creado_en', sa.DateTime(), nullable=True))
        batch_op.alter_column('usuario',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('contraseña',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('contraseña',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=30),
               existing_nullable=True)
        batch_op.alter_column('usuario',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=30),
               existing_nullable=True)
        batch_op.drop_column('creado_en')
        batch_op.drop_column('is_verified')
        batch_op.drop_column('codigo_verificacion')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
