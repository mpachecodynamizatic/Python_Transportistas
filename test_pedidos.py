from database.db_manager import get_db_manager
from models.models import Pedido

db = get_db_manager()

with db.get_session() as session:
    pedidos = session.query(Pedido).all()
    print(f'\nTotal pedidos en BD: {len(pedidos)}\n')
    for p in pedidos:
        print(f'{p.numero_pedido} - {p.provincia_entrega} - {p.tipo_entrega.value}')
