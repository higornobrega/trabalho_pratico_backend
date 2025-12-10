from rest_framework import serializers

from .models import (Caixa, Cardapio, Categoria, Cliente, Conta, Cozinha,
                     Garcom, Gerente, ItemCardapio, ItemPedido, Mesa,
                     Pagamento, PagamentoCartao, PagamentoCheque,
                     PagamentoDinheiro, Pedido, Restaurante, Usuario)


# ------------------------
# Serializers de Usuários
# ------------------------
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'login', 'senha']
        extra_kwargs = {'senha': {'write_only': True}}


class RestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurante
        fields = ['id', 'nome']
    


class GarcomSerializer(serializers.ModelSerializer):
    restaurante_nome = serializers.CharField(
        source='restaurante.nome', read_only=True)

    class Meta:
        model = Garcom
        fields = ['id', 'nome', 'login', 'senha',
                  'restaurante', 'restaurante_nome']
        extra_kwargs = {'senha': {'write_only': True}}


class CaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caixa
        fields = ['id', 'nome', 'login', 'senha']
        extra_kwargs = {'senha': {'write_only': True}}


class CozinhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cozinha
        fields = ['id', 'nome', 'login', 'senha']
        extra_kwargs = {'senha': {'write_only': True}}


class GerenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gerente
        fields = ['id', 'nome', 'login', 'senha']
        extra_kwargs = {'senha': {'write_only': True}}


# ------------------------
# Serializers de Restaurante / Mesas / Clientes
# ------------------------
class MesaSerializer(serializers.ModelSerializer):
    restaurante_nome = serializers.CharField(
        source='restaurante.nome', read_only=True)
    garcom_nome = serializers.CharField(source='garcom.nome', read_only=True)

    class Meta:
        model = Mesa
        fields = ['id', 'numero', 'disponivel', 'restaurante',
                  'restaurante_nome', 'garcom', 'garcom_nome']
    def validate(self, attrs):
        # validações
        return super().validate(attrs)
    def create(self, validated_data):
        
        return super().create(validated_data)


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'hora_chegada', 'hora_saida']


# ------------------------
# Serializers de Cardápio
# ------------------------
class CardapioSerializer(serializers.ModelSerializer):
    gerente_nome = serializers.CharField(source='gerente.nome', read_only=True)

    class Meta:
        model = Cardapio
        fields = ['id', 'gerente', 'gerente_nome']


class CategoriaSerializer(serializers.ModelSerializer):
    categoria_pai_nome = serializers.CharField(
        source='categoria_pai.nome', read_only=True)
    subcategorias = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'categoria_pai',
                  'categoria_pai_nome', 'subcategorias']

    def get_subcategorias(self, obj):
        subcategorias = obj.subcategorias.all()
        return CategoriaSerializer(subcategorias, many=True).data


class ItemCardapioSerializer(serializers.ModelSerializer):
    cardapio_id = serializers.IntegerField(
        source='cardapio.id', read_only=True)
    categoria_nome = serializers.CharField(
        source='categoria.nome', read_only=True)

    class Meta:
        model = ItemCardapio
        fields = [
            'id', 'nome', 'ingredientes', 'preco', 'disponivel_na_cozinha',
            'cardapio', 'cardapio_id', 'categoria', 'categoria_nome'
        ]


# ------------------------
# Serializers de Conta / Pedido
# ------------------------
class ContaSerializer(serializers.ModelSerializer):
    mesa_numero = serializers.IntegerField(
        source='mesa.numero', read_only=True)

    class Meta:
        model = Conta
        fields = ['id', 'nome', 'mesa', 'mesa_numero', 'caixas']


class ItemPedidoSerializer(serializers.ModelSerializer):
    item_cardapio_nome = serializers.CharField(
        source='item_cardapio.nome', read_only=True)
    item_cardapio_preco = serializers.FloatField(
        source='item_cardapio.preco', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = ItemPedido
        fields = ['id', 'quantidade', 'pedido', 'item_cardapio',
                  'item_cardapio_nome', 'item_cardapio_preco', 'subtotal']

    def get_subtotal(self, obj):
        return obj.quantidade * obj.item_cardapio.preco


class PedidoSerializer(serializers.ModelSerializer):
    conta_nome = serializers.CharField(source='conta.nome', read_only=True)
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    itens = ItemPedidoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = [
            'id', 'numero', 'horario_pedido', 'horario_entrega',
            'conta', 'conta_nome', 'cliente', 'cliente_nome', 'cozinha',
            'itens', 'total'
        ]

    def get_total(self, obj):
        return sum(item.quantidade * item.item_cardapio.preco for item in obj.itens.all())


# ------------------------
# Serializers de Pagamentos
# ------------------------
class PagamentoSerializer(serializers.ModelSerializer):
    conta_nome = serializers.CharField(source='conta.nome', read_only=True)

    class Meta:
        model = Pagamento
        fields = ['id', 'conta', 'conta_nome', 'valor', 'data']


class PagamentoDinheiroSerializer(serializers.ModelSerializer):
    conta_nome = serializers.CharField(source='conta.nome', read_only=True)

    class Meta:
        model = PagamentoDinheiro
        fields = ['id', 'conta', 'conta_nome', 'valor', 'data']


class PagamentoCartaoSerializer(serializers.ModelSerializer):
    conta_nome = serializers.CharField(source='conta.nome', read_only=True)

    class Meta:
        model = PagamentoCartao
        fields = ['id', 'conta', 'conta_nome',
                  'valor', 'data', 'nro_transacao']


class PagamentoChequeSerializer(serializers.ModelSerializer):
    conta_nome = serializers.CharField(source='conta.nome', read_only=True)

    class Meta:
        model = PagamentoCheque
        fields = ['id', 'conta', 'conta_nome', 'valor', 'data', 'numero']
