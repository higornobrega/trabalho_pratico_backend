from django.db import models


# ------------------------
# Domínio de usuários
# ------------------------
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    login = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return self.nome


class Restaurante(models.Model):
    # O diagrama não mostra atributos, mas um nome ajuda no domínio
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Garcom(Usuario):
    """
    Especialização de Usuário.
    Um garçom trabalha em exatamente um restaurante.
    Um restaurante emprega vários garçons.
    """
    restaurante = models.ForeignKey(
        Restaurante,
        related_name='garcons',
        on_delete=models.PROTECT,
    )


class Caixa(Usuario):
    """Especialização de Usuário que atua no caixa."""
    pass


class Cozinha(Usuario):
    """Especialização de Usuário que representa a cozinha."""
    pass


class Gerente(Usuario):
    """Especialização de Usuário responsável pelo cardápio."""
    pass


# ------------------------
# Restaurante / Mesas / Clientes
# ------------------------
class Mesa(models.Model):
    """
    Uma mesa pertence a exatamente um restaurante
    e é atendida por exatamente um garçom.
    """
    numero = models.IntegerField()
    disponivel = models.BooleanField(default=True)

    restaurante = models.ForeignKey(
        Restaurante,
        related_name='mesas',
        on_delete=models.CASCADE,
    )
    garcom = models.ForeignKey(
        Garcom,
        related_name='mesas',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Mesa {self.numero} - {self.restaurante.nome}"


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    hora_chegada = models.DateTimeField()
    hora_saida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nome


# ------------------------
# Cardápio / Categorias / Itens de Cardápio
# ------------------------
class Cardapio(models.Model):
    """
    Cada gerente define exatamente um cardápio (1:1).
    """
    gerente = models.OneToOneField(
        Gerente,
        related_name='cardapio',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Cardápio do gerente {self.gerente.nome}"


class Categoria(models.Model):
    """
    Categoria de itens do cardápio.
    Pode ter subcategorias (auto-relacionamento).
    """
    nome = models.CharField(max_length=100)
    # cardapio = models.ForeignKey(
    #     Cardapio,
    #     related_name='categorias',
    #     on_delete=models.CASCADE,
    # )
    categoria_pai = models.ForeignKey(
        'self',
        related_name='subcategorias',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nome


class ItemCardapio(models.Model):
    """
    Item do cardápio, vinculado a uma categoria e a um cardápio.
    """
    nome = models.CharField(max_length=100)
    ingredientes = models.TextField()
    preco = models.FloatField()
    disponivel_na_cozinha = models.BooleanField(default=True)

    cardapio = models.ForeignKey(
        Cardapio,
        related_name='itens',
        on_delete=models.CASCADE,
    )
    categoria = models.ForeignKey(
        Categoria,
        related_name='itens',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nome


# ------------------------
# Conta / Pedido / Itens
# ------------------------
class Conta(models.Model):
    """
    Cada mesa pode ter várias contas (1..*).
    Uma conta é enviada para uma cozinha (1),
    e pode ser gerenciada por vários caixas (N:N).
    """
    nome = models.CharField(max_length=100)

    mesa = models.ForeignKey(
        Mesa,
        related_name='contas',
        on_delete=models.PROTECT,
    )

    caixas = models.ManyToManyField(
        Caixa,
        related_name='contas',
        blank=True,
    )

    def __str__(self):
        return f"Conta {self.id} - {self.nome}"


class Pedido(models.Model):
    """
    Uma conta gera vários pedidos (1..*).
    Um cliente faz vários pedidos; cada pedido é de um único cliente.
    """
    numero = models.IntegerField()
    horario_pedido = models.DateTimeField()
    horario_entrega = models.DateTimeField(null=True, blank=True)

    conta = models.ForeignKey(
        Conta,
        related_name='pedidos',
        on_delete=models.CASCADE,
    )
    cliente = models.ForeignKey(
        Cliente,
        related_name='pedidos',
        on_delete=models.PROTECT,
    )
    cozinha = models.ForeignKey(
        Cozinha,
        related_name='contas',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"Pedido {self.numero}"


class ItemPedido(models.Model):
    """
    Itens de um pedido. Cada item referencia um ItemCardapio.
    """
    quantidade = models.FloatField()

    pedido = models.ForeignKey(
        Pedido,
        related_name='itens',
        on_delete=models.CASCADE,
    )
    item_cardapio = models.ForeignKey(
        ItemCardapio,
        related_name='itens_pedido',
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return f"{self.quantidade}x {self.item_cardapio.nome}"


# ------------------------
# Pagamentos
# ------------------------
class Pagamento(models.Model):
    """
    Pagamento genérico.
    Pelo diagrama, a relação com Conta é 1:1
    (uma conta é paga por um único pagamento).
    """
    conta = models.OneToOneField(
        Conta,
        related_name='pagamento',
        on_delete=models.CASCADE,
    )
    valor = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pagamento {self.id} - R$ {self.valor:.2f}"


class PagamentoDinheiro(Pagamento):
    """Pagamento em dinheiro (sem atributos extras no diagrama)."""
    pass


class PagamentoCartao(Pagamento):
    """Pagamento em cartão, com número de transação."""
    nro_transacao = models.IntegerField()


class PagamentoCheque(Pagamento):
    """Pagamento em cheque, com número do cheque."""
    numero = models.IntegerField()
