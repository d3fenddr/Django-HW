"""initial schema

Revision ID: 0001_init
Revises: 
Create Date: 2025-10-29 00:00:00

"""
from alembic import op
import sqlalchemy as sa


revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=150), nullable=False, unique=True, index=True),
        sa.Column('email', sa.String(length=254), nullable=True, unique=True, index=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('1')),
        sa.Column('is_staff', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.text('0')),
    )

    op.create_table('categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=60), nullable=False, unique=True),
        sa.Column('slug', sa.String(length=80), nullable=False, unique=True),
    )

    op.create_table('articles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('users.id'), index=True),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('slug', sa.String(length=220), nullable=False, unique=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'), nullable=True),
        sa.Column('image_url', sa.String(length=500), nullable=True),
        sa.Column('excerpt', sa.Text(), nullable=False, server_default=''),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=12), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table('reactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('article_id', sa.Integer(), sa.ForeignKey('articles.id')),
        sa.Column('value', sa.SmallInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('user_id', 'article_id', name='uix_reaction_user_article')
    )

    op.create_table('ratings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('article_id', sa.Integer(), sa.ForeignKey('articles.id')),
        sa.Column('score', sa.SmallInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('user_id', 'article_id', name='uix_rating_user_article')
    )

    op.create_table('bookmarks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('article_id', sa.Integer(), sa.ForeignKey('articles.id')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('user_id', 'article_id', name='uix_bookmark_user_article')
    )


def downgrade() -> None:
    op.drop_table('bookmarks')
    op.drop_table('ratings')
    op.drop_table('reactions')
    op.drop_table('articles')
    op.drop_table('categories')
    op.drop_table('users')


