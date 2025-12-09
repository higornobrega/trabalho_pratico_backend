from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from django.db.models import Count, Sum
from rest_framework.views import APIView
from django.db.models.functions import ExtractHour

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

class RankGarconAtendimentoAPIView(APIView):
    """
    Endpoint: GET /rank-garcon-atendimento/
    Rank de garçons por número de mesas atendidas.
    """

    @extend_schema(description='Rank de garçons por quantidade de mesas atendidas')
    def get(self, request):
        # Anota em cada garçom:
        # - total_mesas: quantas mesas estão vinculadas a ele
        # - total_pedidos: quantos pedidos passaram por essas mesas
        queryset = (
            Garcom.objects
            .annotate(
                total_mesas=Count('mesas', distinct=True),
                total_pedidos=Count('mesas__contas__pedidos', distinct=True),
            )
            .order_by('-total_mesas', '-total_pedidos', 'nome')
        )

        resultado = [
            {
                "garcom_id": garcom.id,
                "garcom_nome": garcom.nome,
                "restaurante": garcom.restaurante.nome if garcom.restaurante else None,
                "total_mesas": garcom.total_mesas,
                "total_pedidos": garcom.total_pedidos,
            }
            for garcom in queryset
        ]

        return Response(resultado, status=status.HTTP_200_OK)

class ItemMaisPedidoAPIView(APIView):
    """
    Endpoint: GET /item-mais-pedido/
    Retorna o item de cardápio mais pedido.

    Lógica geral:
    - Parte do modelo ItemPedido, que representa cada item lançado em um pedido,
      contendo a quantidade e a referência para um ItemCardapio.
    - A consulta agrupa todos os registros de ItemPedido por item de cardápio,
      usando o método .values('item_cardapio', 'item_cardapio__nome', 'item_cardapio__preco').
      Isso faz com que cada linha do resultado represente um item do cardápio,
      e não um ItemPedido isolado.
    - Em seguida, é usado .annotate(total_quantidade=Sum('quantidade')) para somar
      a quantidade de cada ItemPedido daquele item de cardápio. Assim, obtemos
      a quantidade total pedida de cada produto.
    - A lista resultante é ordenada em ordem decrescente por total_quantidade
      (.order_by('-total_quantidade')), de forma que o item mais pedido aparece
      na primeira posição.
    - Se não houver nenhum ItemPedido cadastrado, o endpoint retorna uma mensagem
      informando que não há dados.
    - Caso contrário, é selecionado o primeiro registro (o “campeão” de pedidos),
      e montada uma resposta com:
        * id do item de cardápio,
        * nome,
        * preço,
        * quantidade total pedida.
    """

    @extend_schema(description='Retorna o item de cardápio mais pedido')
    def get(self, request):
        # Agrupa os itens de pedido por item_cardapio
        agregados = (
            ItemPedido.objects
            .values('item_cardapio', 'item_cardapio__nome', 'item_cardapio__preco')
            .annotate(total_quantidade=Sum('quantidade'))
            .order_by('-total_quantidade')
        )

        if not agregados:
            return Response(
                {"detail": "Nenhum item de pedido encontrado."},
                status=status.HTTP_200_OK,
            )

        top = agregados[0]

        data = {
            "item_cardapio_id": top["item_cardapio"],
            "nome": top["item_cardapio__nome"],
            "preco": top["item_cardapio__preco"],
            "total_quantidade": top["total_quantidade"],
        }

        return Response(data, status=status.HTTP_200_OK)

class TipoPagamentoMaisUsadoAPIView(APIView):
    """
    Endpoint: GET /tipo-pagamente-mais-usado/

    Retorna qual tipo de pagamento (dinheiro, cartão ou cheque)
    foi utilizado mais vezes, com o total de usos de cada um.
    """

    @extend_schema(description='Retorna o tipo de pagamento mais usado')
    def get(self, request):
        stats = [
            {"tipo": "dinheiro", "total": PagamentoDinheiro.objects.count()},
            {"tipo": "cartao", "total": PagamentoCartao.objects.count()},
            {"tipo": "cheque", "total": PagamentoCheque.objects.count()},
        ]

        # Se não houver nenhum pagamento ainda
        if all(item["total"] == 0 for item in stats):
            return Response(
                {
                    "detail": "Nenhum pagamento registrado.",
                    "tipos": {item["tipo"]: item["total"] for item in stats},
                },
                status=status.HTTP_200_OK,
            )

        # Pega o tipo com maior quantidade
        top = max(stats, key=lambda item: item["total"])

        data = {
            "tipo_mais_usado": top["tipo"],
            "total": top["total"],
            "detalhes": {item["tipo"]: item["total"] for item in stats},
        }

        return Response(data, status=status.HTTP_200_OK)

class ValorMedioPedidosAPIView(APIView):
    """
    Endpoint: GET /valor-medio-pedidos/

    Calcula o valor médio dos pedidos.
    Para cada pedido, soma (quantidade * preço) de cada ItemPedido
    e, em seguida, faz a média entre todos os pedidos.
    """

    @extend_schema(description='Retorna o valor médio dos pedidos')
    def get(self, request):
        pedidos = Pedido.objects.prefetch_related('itens__item_cardapio').all()

        if not pedidos.exists():
            return Response(
                {
                    "detail": "Nenhum pedido encontrado.",
                    "quantidade_pedidos": 0,
                    "valor_medio": 0.0,
                },
                status=status.HTTP_200_OK,
            )

        totais = []

        for pedido in pedidos:
            total_pedido = 0.0
            for item in pedido.itens.all():
                total_pedido += item.quantidade * item.item_cardapio.preco
            totais.append(total_pedido)

        valor_medio = sum(totais) / len(totais)

        data = {
            "quantidade_pedidos": len(totais),
            "valor_medio": round(valor_medio, 2),
        }

        return Response(data, status=status.HTTP_200_OK)

class CategoriaPopularAPIView(APIView):
    """
    Endpoint: GET /categoria-popular/

    Retorna a categoria de cardápio mais popular, ou seja,
    aquela cujos itens somam a maior quantidade em todos os pedidos.
    """

    @extend_schema(description='Retorna a categoria de cardápio mais popular')
    def get(self, request):

        agregados = (
            ItemPedido.objects
            .values('item_cardapio__categoria', 'item_cardapio__categoria__nome')
            .annotate(total_quantidade=Sum('quantidade'))
            .order_by('-total_quantidade')
        )

        if not agregados:
            return Response(
                {
                    "detail": "Nenhum item de pedido encontrado.",
                },
                status=status.HTTP_200_OK,
            )

        top = agregados[0]

        total_qtd = top["total_quantidade"]
        total_qtd = int(total_qtd) if total_qtd is not None else 0

        data = {
            "categoria_id": top["item_cardapio__categoria"],
            "nome": top["item_cardapio__categoria__nome"],
            "total_itens_pedidos": total_qtd,
        }

        return Response(data, status=status.HTTP_200_OK)

class HorariosMaisPedidosAPIView(APIView):
    """
    Endpoint: GET /horarios-mais-pedidos/

    Agrupa os pedidos por hora do dia (0–23), com base no campo
    `horario_pedido` do modelo Pedido, e retorna um ranking dos
    horários com mais pedidos.

    Lógica:
    - Usa ExtractHour para extrair apenas a hora do campo datetime.
    - Agrupa por essa hora (.values('hora')).
    - Conta quantos pedidos existem em cada hora (Count('id')).
    - Ordena do horário com mais pedidos para o com menos.
    - Retorna também o horário de maior movimento destacado.
    """

    @extend_schema(
        description='Retorna um ranking de horários do dia com mais pedidos (baseado em horario_pedido)'
    )
    def get(self, request):
        agregados = (
            Pedido.objects
            .annotate(hora=ExtractHour('horario_pedido'))
            .values('hora')
            .annotate(total_pedidos=Count('id'))
            .order_by('-total_pedidos', 'hora')
        )

        if not agregados:
            return Response(
                {
                    "detail": "Nenhum pedido encontrado.",
                    "horarios": [],
                },
                status=status.HTTP_200_OK,
            )

        horarios = [
            {
                "hora": item["hora"],
                "total_pedidos": item["total_pedidos"],
            }
            for item in agregados
        ]

        data = {
            "hora_mais_movimento": horarios[0],
            "horarios": horarios,
        }

        return Response(data, status=status.HTTP_200_OK)

class CardapioMaisUsadoAPIView(APIView):
    """
    Endpoint: GET /cardapio-mais-usado/

    Retorna o cardápio mais usado, ou seja, aquele cujos itens de cardápio
    somam a maior quantidade em todos os itens de pedido.

    A agregação parte de ItemPedido -> item_cardapio -> cardapio.
    """

    @extend_schema(description='Retorna o cardápio mais usado nos pedidos')
    def get(self, request):
        agregados = (
            ItemPedido.objects
            .values(
                'item_cardapio__cardapio',
                'item_cardapio__cardapio__gerente__nome',
            )
            .annotate(total_quantidade=Sum('quantidade'))
            .order_by('-total_quantidade')
        )

        if not agregados:
            return Response(
                {
                    "detail": "Nenhum item de pedido encontrado.",
                },
                status=status.HTTP_200_OK,
            )

        top = agregados[0]

        total_qtd = top["total_quantidade"]
        total_qtd = int(total_qtd) if total_qtd is not None else 0

        data = {
            "cardapio_id": top["item_cardapio__cardapio"],
            "gerente_nome": top["item_cardapio__cardapio__gerente__nome"],
            "descricao": f"Cardápio do gerente {top['item_cardapio__cardapio__gerente__nome']}",
            "total_itens_pedidos": total_qtd,
        }

        return Response(data, status=status.HTTP_200_OK)

class CategoriaMaisItensCardapioAPIView(APIView):
    """
    Endpoint: GET /categoria-mais-itens_cardapio/

    Retorna a categoria que possui o maior número de itens de cardápio
    associados.

    Lógica:
    - Parte do modelo Categoria.
    - Usa o related_name='itens' definido em ItemCardapio.categoria para
      contar quantos itens cada categoria possui.
    - A consulta anota um campo calculado `total_itens` com Count('itens').
    - Ordena decrescentemente por `total_itens` para que a categoria com
      mais itens venha primeiro.
    - Se não houver categorias ou itens cadastrados, retorna uma mensagem
      informando que não há dados.
    - Caso contrário, retorna a categoria “campeã” e, opcionalmente, o
      ranking completo com id, nome e total de itens.
    """

    @extend_schema(
        description='Retorna a categoria com maior quantidade de itens de cardápio'
    )
    def get(self, request):
        categorias = (
            Categoria.objects
            .annotate(total_itens=Count('itens'))
            .order_by('-total_itens', 'nome')
        )

        if not categorias:
            return Response(
                {
                    "detail": "Nenhuma categoria encontrada.",
                    "categorias": [],
                },
                status=status.HTTP_200_OK,
            )

        ranking = [
            {
                "categoria_id": cat.id,
                "nome": cat.nome,
                "total_itens_cardapio": cat.total_itens,
            }
            for cat in categorias
        ]

        data = {
            "categoria_campea": ranking[0],
            "categorias": ranking,
        }

        return Response(data, status=status.HTTP_200_OK)
