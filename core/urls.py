from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

# Usuários
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'restaurantes', views.RestauranteViewSet)
router.register(r'garcons', views.GarcomViewSet)
router.register(r'caixas', views.CaixaViewSet)
router.register(r'cozinhas', views.CozinhaViewSet)
router.register(r'gerentes', views.GerenteViewSet)

# Mesas e Clientes
router.register(r'mesas', views.MesaViewSet)
router.register(r'clientes', views.ClienteViewSet)

# Cardápio
router.register(r'cardapios', views.CardapioViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'itens-cardapio', views.ItemCardapioViewSet)

# Contas e Pedidos
router.register(r'contas', views.ContaViewSet)
router.register(r'pedidos', views.PedidoViewSet)
router.register(r'itens-pedido', views.ItemPedidoViewSet)

# Pagamentos
router.register(r'pagamentos', views.PagamentoViewSet)
router.register(r'pagamentos-dinheiro', views.PagamentoDinheiroViewSet)
router.register(r'pagamentos-cartao', views.PagamentoCartaoViewSet)
router.register(r'pagamentos-cheque', views.PagamentoChequeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
