from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .models import (Caixa, Cardapio, Categoria, Cliente, Conta, Cozinha,
                     Garcom, Gerente, ItemCardapio, ItemPedido, Mesa,
                     Pagamento, PagamentoCartao, PagamentoCheque,
                     PagamentoDinheiro, Pedido, Restaurante, Usuario)
from .serializers import (CaixaSerializer, CardapioSerializer,
                          CategoriaSerializer, ClienteSerializer,
                          ContaSerializer, CozinhaSerializer, GarcomSerializer,
                          GerenteSerializer, ItemCardapioSerializer,
                          ItemPedidoSerializer, MesaSerializer,
                          PagamentoCartaoSerializer, PagamentoChequeSerializer,
                          PagamentoDinheiroSerializer, PagamentoSerializer,
                          PedidoSerializer, RestauranteSerializer,
                          UsuarioSerializer)


# ------------------------
# ViewSets de Usuários
# ------------------------
@extend_schema_view(
    list=extend_schema(description='Lista todos os usuários'),
    retrieve=extend_schema(description='Retorna um usuário específico'),
    create=extend_schema(description='Cria um novo usuário'),
    update=extend_schema(description='Atualiza um usuário'),
    destroy=extend_schema(description='Remove um usuário'),
)
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'login']
    search_fields = ['nome', 'login']
    ordering_fields = ['id', 'nome']


@extend_schema_view(
    list=extend_schema(description='Lista todos os restaurantes'),
    retrieve=extend_schema(description='Retorna um restaurante específico'),
    create=extend_schema(description='Cria um novo restaurante'),
    update=extend_schema(description='Atualiza um restaurante'),
    destroy=extend_schema(description='Remove um restaurante'),
)
class RestauranteViewSet(viewsets.ModelViewSet):
    queryset = Restaurante.objects.all()
    serializer_class = RestauranteSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome']
    search_fields = ['nome']
    ordering_fields = ['id', 'nome']


@extend_schema_view(
    list=extend_schema(description='Lista todos os garçons'),
    retrieve=extend_schema(description='Retorna um garçom específico'),
    create=extend_schema(description='Cria um novo garçom'),
    update=extend_schema(description='Atualiza um garçom'),
    destroy=extend_schema(description='Remove um garçom'),
)
class GarcomViewSet(viewsets.ModelViewSet):
    queryset = Garcom.objects.select_related('restaurante').all()
    serializer_class = GarcomSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'restaurante']
    search_fields = ['nome', 'login']
    ordering_fields = ['id', 'nome']

    @extend_schema(description='Lista as mesas atendidas pelo garçom')
    @action(detail=True, methods=['get'])
    def mesas(self, request, pk=None):
        garcom = self.get_object()
        mesas = garcom.mesas.all()
        serializer = MesaSerializer(mesas, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description='Lista todos os caixas'),
    retrieve=extend_schema(description='Retorna um caixa específico'),
    create=extend_schema(description='Cria um novo caixa'),
    update=extend_schema(description='Atualiza um caixa'),
    destroy=extend_schema(description='Remove um caixa'),
)
class CaixaViewSet(viewsets.ModelViewSet):
    queryset = Caixa.objects.all()
    serializer_class = CaixaSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome']
    search_fields = ['nome', 'login']
    ordering_fields = ['id', 'nome']


@extend_schema_view(
    list=extend_schema(description='Lista todas as cozinhas'),
    retrieve=extend_schema(description='Retorna uma cozinha específica'),
    create=extend_schema(description='Cria uma nova cozinha'),
    update=extend_schema(description='Atualiza uma cozinha'),
    destroy=extend_schema(description='Remove uma cozinha'),
)
class CozinhaViewSet(viewsets.ModelViewSet):
    queryset = Cozinha.objects.all()
    serializer_class = CozinhaSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome']
    search_fields = ['nome', 'login']
    ordering_fields = ['id', 'nome']


@extend_schema_view(
    list=extend_schema(description='Lista todos os gerentes'),
    retrieve=extend_schema(description='Retorna um gerente específico'),
    create=extend_schema(description='Cria um novo gerente'),
    update=extend_schema(description='Atualiza um gerente'),
    destroy=extend_schema(description='Remove um gerente'),
)
class GerenteViewSet(viewsets.ModelViewSet):
    queryset = Gerente.objects.all()
    serializer_class = GerenteSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome']
    search_fields = ['nome', 'login']
    ordering_fields = ['id', 'nome']


# ------------------------
# ViewSets de Mesas e Clientes
# ------------------------
@extend_schema_view(
    list=extend_schema(description='Lista todas as mesas'),
    retrieve=extend_schema(description='Retorna uma mesa específica'),
    create=extend_schema(description='Cria uma nova mesa'),
    update=extend_schema(description='Atualiza uma mesa'),
    destroy=extend_schema(description='Remove uma mesa'),
)
class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.select_related('restaurante', 'garcom').all()
    serializer_class = MesaSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['numero', 'disponivel', 'restaurante', 'garcom']
    search_fields = ['numero']
    ordering_fields = ['id', 'numero']

    @extend_schema(description='Lista mesas disponíveis')
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        mesas = self.queryset.filter(disponivel=True)
        serializer = self.get_serializer(mesas, many=True)
        return Response(serializer.data)

    @extend_schema(description='Lista as contas da mesa')
    @action(detail=True, methods=['get'])
    def contas(self, request, pk=None):
        mesa = self.get_object()
        contas = mesa.contas.all()
        serializer = ContaSerializer(contas, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description='Lista todos os clientes'),
    retrieve=extend_schema(description='Retorna um cliente específico'),
    create=extend_schema(description='Cria um novo cliente'),
    update=extend_schema(description='Atualiza um cliente'),
    destroy=extend_schema(description='Remove um cliente'),
)
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome']
    search_fields = ['nome']
    ordering_fields = ['id', 'nome', 'hora_chegada']

    @extend_schema(description='Lista os pedidos do cliente')
    @action(detail=True, methods=['get'])
    def pedidos(self, request, pk=None):
        cliente = self.get_object()
        pedidos = cliente.pedidos.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)


# ------------------------
# ViewSets de Cardápio
# ------------------------
@extend_schema_view(
    list=extend_schema(description='Lista todos os cardápios'),
    retrieve=extend_schema(description='Retorna um cardápio específico'),
    create=extend_schema(description='Cria um novo cardápio'),
    update=extend_schema(description='Atualiza um cardápio'),
    destroy=extend_schema(description='Remove um cardápio'),
)
class CardapioViewSet(viewsets.ModelViewSet):
    queryset = Cardapio.objects.select_related('gerente').all()
    serializer_class = CardapioSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['gerente']
    ordering_fields = ['id']

    @extend_schema(description='Lista os itens do cardápio')
    @action(detail=True, methods=['get'])
    def itens(self, request, pk=None):
        cardapio = self.get_object()
        itens = cardapio.itens.all()
        serializer = ItemCardapioSerializer(itens, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description='Lista todas as categorias'),
    retrieve=extend_schema(description='Retorna uma categoria específica'),
    create=extend_schema(description='Cria uma nova categoria'),
    update=extend_schema(description='Atualiza uma categoria'),
    destroy=extend_schema(description='Remove uma categoria'),
)
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'categoria_pai']
    search_fields = ['nome']
    ordering_fields = ['id', 'nome']

    @extend_schema(description='Lista categorias raiz (sem categoria pai)')
    @action(detail=False, methods=['get'])
    def raiz(self, request):
        categorias = self.queryset.filter(categoria_pai__isnull=True)
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description='Lista todos os itens do cardápio'),
    retrieve=extend_schema(
        description='Retorna um item do cardápio específico'),
    create=extend_schema(description='Cria um novo item no cardápio'),
    update=extend_schema(description='Atualiza um item do cardápio'),
    destroy=extend_schema(description='Remove um item do cardápio'),
)
class ItemCardapioViewSet(viewsets.ModelViewSet):
    queryset = ItemCardapio.objects.select_related(
        'cardapio', 'categoria').all()
    serializer_class = ItemCardapioSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'cardapio',
                        'categoria', 'disponivel_na_cozinha']
    search_fields = ['nome', 'ingredientes']
    ordering_fields = ['id', 'nome', 'preco']

    @extend_schema(description='Lista itens disponíveis na cozinha')
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        itens = self.queryset.filter(disponivel_na_cozinha=True)
        serializer = self.get_serializer(itens, many=True)
        return Response(serializer.data)


# ------------------------
# ViewSets de Conta e Pedido
# ------------------------
@extend_schema_view(
    list=extend_schema(description='Lista todas as contas'),
    retrieve=extend_schema(description='Retorna uma conta específica'),
    create=extend_schema(description='Cria uma nova conta'),
    update=extend_schema(description='Atualiza uma conta'),
    destroy=extend_schema(description='Remove uma conta'),
)
class ContaViewSet(viewsets.ModelViewSet):
    queryset = Conta.objects.select_related(
        'mesa').prefetch_related('caixas').all()
    serializer_class = ContaSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nome', 'mesa']
    search_fields = ['nome']
    ordering_fields = ['id', 'nome']

    @extend_schema(description='Lista os pedidos da conta')
    @action(detail=True, methods=['get'])
    def pedidos(self, request, pk=None):
        conta = self.get_object()
        pedidos = conta.pedidos.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

    @extend_schema(description='Retorna o total da conta')
    @action(detail=True, methods=['get'])
    def total(self, request, pk=None):
        conta = self.get_object()
        total = sum(
            item.quantidade * item.item_cardapio.preco
            for pedido in conta.pedidos.all()
            for item in pedido.itens.all()
        )
        return Response({'total': total})


@extend_schema_view(
    list=extend_schema(description='Lista todos os pedidos'),
    retrieve=extend_schema(description='Retorna um pedido específico'),
    create=extend_schema(description='Cria um novo pedido'),
    update=extend_schema(description='Atualiza um pedido'),
    destroy=extend_schema(description='Remove um pedido'),
)
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related(
        'conta', 'cliente', 'cozinha').prefetch_related('itens').all()
    serializer_class = PedidoSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['numero', 'conta', 'cliente', 'cozinha']
    search_fields = ['numero']
    ordering_fields = ['id', 'numero', 'horario_pedido']

    @extend_schema(description='Lista pedidos pendentes (sem horário de entrega)')
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        pedidos = self.queryset.filter(horario_entrega__isnull=True)
        serializer = self.get_serializer(pedidos, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description='Lista todos os itens de pedido'),
    retrieve=extend_schema(description='Retorna um item de pedido específico'),
    create=extend_schema(description='Adiciona um item ao pedido'),
    update=extend_schema(description='Atualiza um item do pedido'),
    destroy=extend_schema(description='Remove um item do pedido'),
)
class ItemPedidoViewSet(viewsets.ModelViewSet):
    queryset = ItemPedido.objects.select_related(
        'pedido', 'item_cardapio').all()
    serializer_class = ItemPedidoSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['pedido', 'item_cardapio']
    ordering_fields = ['id', 'quantidade']


# ------------------------
# ViewSets de Pagamentos
# ------------------------
@extend_schema_view(
    list=extend_schema(description='Lista todos os pagamentos'),
    retrieve=extend_schema(description='Retorna um pagamento específico'),
    create=extend_schema(description='Cria um novo pagamento'),
    update=extend_schema(description='Atualiza um pagamento'),
    destroy=extend_schema(description='Remove um pagamento'),
)
class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.select_related('conta').all()
    serializer_class = PagamentoSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['conta']
    ordering_fields = ['id', 'valor', 'data']


@extend_schema_view(
    list=extend_schema(description='Lista todos os pagamentos em dinheiro'),
    retrieve=extend_schema(
        description='Retorna um pagamento em dinheiro específico'),
    create=extend_schema(description='Cria um novo pagamento em dinheiro'),
    update=extend_schema(description='Atualiza um pagamento em dinheiro'),
    destroy=extend_schema(description='Remove um pagamento em dinheiro'),
)
class PagamentoDinheiroViewSet(viewsets.ModelViewSet):
    queryset = PagamentoDinheiro.objects.select_related('conta').all()
    serializer_class = PagamentoDinheiroSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['conta']
    ordering_fields = ['id', 'valor', 'data']


@extend_schema_view(
    list=extend_schema(description='Lista todos os pagamentos em cartão'),
    retrieve=extend_schema(
        description='Retorna um pagamento em cartão específico'),
    create=extend_schema(description='Cria um novo pagamento em cartão'),
    update=extend_schema(description='Atualiza um pagamento em cartão'),
    destroy=extend_schema(description='Remove um pagamento em cartão'),
)
class PagamentoCartaoViewSet(viewsets.ModelViewSet):
    queryset = PagamentoCartao.objects.select_related('conta').all()
    serializer_class = PagamentoCartaoSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['conta', 'nro_transacao']
    ordering_fields = ['id', 'valor', 'data']


@extend_schema_view(
    list=extend_schema(description='Lista todos os pagamentos em cheque'),
    retrieve=extend_schema(
        description='Retorna um pagamento em cheque específico'),
    create=extend_schema(description='Cria um novo pagamento em cheque'),
    update=extend_schema(description='Atualiza um pagamento em cheque'),
    destroy=extend_schema(description='Remove um pagamento em cheque'),
)
class PagamentoChequeViewSet(viewsets.ModelViewSet):
    queryset = PagamentoCheque.objects.select_related('conta').all()
    serializer_class = PagamentoChequeSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['conta', 'numero']
    ordering_fields = ['id', 'valor', 'data']
