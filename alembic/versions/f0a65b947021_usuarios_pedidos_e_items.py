"""usuarios, pedidos e items

Revision ID: f0a65b947021
Revises: 
Create Date: 2026-09-07 09:01:49.849945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0a65b947021'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: crea las cuatro tablas del modelo e-commerce."""
    # Tabla: usuarios
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('rol', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_index(op.f('ix_usuarios_id'), 'usuarios', ['id'], unique=False)

    # Tabla: productos
    op.create_table(
        'productos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('precio_final', sa.Float(), nullable=False),
        sa.Column('cuotas_cantidad', sa.Integer(), nullable=False),
        sa.Column('cuotas_valor', sa.Float(), nullable=False),
        sa.Column('garantia_meses', sa.Integer(), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_productos_id'), 'productos', ['id'], unique=False)

    # Tabla: pedidos (depende de usuarios)
    op.create_table(
        'pedidos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('estado', sa.String(), nullable=True),
        sa.Column('total', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_pedidos_id'), 'pedidos', ['id'], unique=False)

    # Tabla: items_pedido (depende de pedidos y productos)
    op.create_table(
        'items_pedido',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('producto_id', sa.Integer(), nullable=False),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.Column('precio_unitario', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['pedido_id'], ['pedidos.id']),
        sa.ForeignKeyConstraint(['producto_id'], ['productos.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_items_pedido_id'), 'items_pedido', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema: elimina las cuatro tablas."""
    op.drop_index(op.f('ix_items_pedido_id'), table_name='items_pedido')
    op.drop_table('items_pedido')
    op.drop_index(op.f('ix_pedidos_id'), table_name='pedidos')
    op.drop_table('pedidos')
    op.drop_index(op.f('ix_productos_id'), table_name='productos')
    op.drop_table('productos')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_id'), table_name='usuarios')
    op.drop_table('usuarios')
