"""empty message

Revision ID: 5fd1f8c48c6c
Revises: 496d7c563698
Create Date: 2022-09-26 19:24:01.387118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5fd1f8c48c6c'
down_revision = '496d7c563698'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('popular_game_id_fkey', 'popular', type_='foreignkey')
    op.create_foreign_key(None, 'popular', 'game', ['game_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'popular', type_='foreignkey')
    op.create_foreign_key('popular_game_id_fkey', 'popular', 'game', ['game_id'], ['id'])
    # ### end Alembic commands ###