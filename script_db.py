from core.models import Restaurante, Garcom, Mesa, Caixa, Cozinha, Gerente, Cardapio, Categoria, ItemCardapio, Cliente, Conta, Pedido, ItemPedido
from datetime import datetime

# Restaurante
rest = Restaurante.objects.create(nome="Restaurante Central")

# Usuários
gerente = Gerente.objects.create(nome="Carlos Gerente", login="carlos", senha="123")
garcom1 = Garcom.objects.create(nome="João Garçom", login="joao", senha="123", restaurante=rest)
garcom2 = Garcom.objects.create(nome="Maria Garçonete", login="maria", senha="123", restaurante=rest)
caixa = Caixa.objects.create(nome="Pedro Caixa", login="pedro", senha="123")
cozinha = Cozinha.objects.create(nome="Cozinha Principal", login="cozinha", senha="123")

# Cardápio e categorias
cardapio = Cardapio.objects.create(gerente=gerente)
cat_bebidas = Categoria.objects.create(nome="Bebidas")
cat_pratos = Categoria.objects.create(nome="Pratos")

# Itens do cardápio
refri = ItemCardapio.objects.create(nome="Refrigerante", ingredientes="Refrigerante gelado", preco=6.0, cardapio=cardapio, categoria=cat_bebidas)
pizza = ItemCardapio.objects.create(nome="Pizza", ingredientes="Mussarela", preco=30.0, cardapio=cardapio, categoria=cat_pratos)
pastel = ItemCardapio.objects.create(nome="Pastel", ingredientes="Carne", preco=10.0, cardapio=cardapio, categoria=cat_pratos)

# Mesas
mesa1 = Mesa.objects.create(numero=1, disponivel=True, restaurante=rest, garcom=garcom1)
mesa2 = Mesa.objects.create(numero=2, disponivel=True, restaurante=rest, garcom=garcom2)
mesa3 = Mesa.objects.create(numero=3, disponivel=True, restaurante=rest, garcom=garcom1)

# Clientes
cli1 = Cliente.objects.create(nome="Cliente 1", hora_chegada=datetime.now())
cli2 = Cliente.objects.create(nome="Cliente 2", hora_chegada=datetime.now())

# Contas
conta1 = Conta.objects.create(nome="Conta Mesa 1", mesa=mesa1)
conta2 = Conta.objects.create(nome="Conta Mesa 2", mesa=mesa2)

# Pedidos
pedido1 = Pedido.objects.create(numero=101, horario_pedido=datetime.now(), conta=conta1, cliente=cli1, cozinha=cozinha)
pedido2 = Pedido.objects.create(numero=102, horario_pedido=datetime.now(), conta=conta2, cliente=cli2, cozinha=cozinha)
pedido3 = Pedido.objects.create(numero=103, horario_pedido=datetime.now(), conta=conta1, cliente=cli1, cozinha=cozinha)

# Itens de pedidos
ItemPedido.objects.create(pedido=pedido1, item_cardapio=refri, quantidade=2)
ItemPedido.objects.create(pedido=pedido1, item_cardapio=pizza, quantidade=1)
ItemPedido.objects.create(pedido=pedido2, item_cardapio=pastel, quantidade=3)
ItemPedido.objects.create(pedido=pedido3, item_cardapio=refri, quantidade=1)
