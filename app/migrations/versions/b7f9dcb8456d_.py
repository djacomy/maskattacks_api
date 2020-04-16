"""empty message

Revision ID: b7f9dcb8456d
Revises: 4ddf2ddee3a
Create Date: 2020-04-16 13:57:22.590601

"""

# revision identifiers, used by Alembic.
revision = 'b7f9dcb8456d'
down_revision = '4ddf2ddee3a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_deliveryitem_batch')
    op.add_column('product_batch', sa.Column('deliveritem_id', sa.Integer(), nullable=False))
    op.add_column('product_batch', sa.Column('reference', sa.String(length=40), nullable=False))
    op.create_foreign_key(None, 'product_batch', 'product_deliveryitem', ['deliveritem_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product_batch', type_='foreignkey')
    op.drop_column('product_batch', 'reference')
    op.drop_column('product_batch', 'deliveritem_id')
    op.create_table('product_deliveryitem_batch',
    sa.Column('batch_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('deliveryitem_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['batch_id'], ['product_batch.id'], name='product_deliveryitem_batch_batch_id_fkey'),
    sa.ForeignKeyConstraint(['deliveryitem_id'], ['product_deliveryitem.id'], name='product_deliveryitem_batch_deliveryitem_id_fkey'),
    sa.PrimaryKeyConstraint('batch_id', 'deliveryitem_id', name='product_deliveryitem_batch_pkey')
    )
    # ### end Alembic commands ###
