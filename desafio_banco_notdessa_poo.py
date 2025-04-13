from datetime import datetime
from abc import ABC, abstractmethod

#definindo constantes 
LIMITE_SAQUES = 3
AGENCIA = "0001"
banco_name = "Banco NotDessa"
contato = "Git: notdessa"
#definindo listas
usuarios = []
contas = []

#classes

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"Nome: {self.nome} | CPF: {self.cpf} | Data de Nascimento: {self.data_nascimento} | Endereço: {self.endereco}"


class Conta:
    def __init__(self, numero_conta, cliente):
        self.numero_conta = numero_conta
        self.agencia = AGENCIA
        self.cliente = cliente
        self.saldo = 0
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(f"Depósito: R$ {valor:.2f}")
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!".center(40))
            return True
        else:
            print("Valor inválido para depósito.".center(40))
            return False

    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido.".center(40))
        elif valor > self.saldo:
            print("Saldo insuficiente.".center(40))
        else:
            self.saldo -= valor
            self.historico.adicionar_transacao(f"Saque: R$ {valor:.2f}")
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!".center(40))
            return True
        return False

    def __str__(self):
        return f"Conta: {self.numero_conta} | Agência: {self.agencia} | Cliente: {self.cliente.nome}"


class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("Limite de saques atingido.".center(40))
        elif valor > self.limite:
            print("Limite de saque excedido.".center(40))
        else:
            sucesso = super().sacar(valor)
            if sucesso:
                self.numero_saques += 1
            return sucesso
        return False


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, descricao):
        self.transacoes.append(descricao)

    def imprimir(self):
        print("\n========== EXTRATO ==========".center(40))
        if not self.transacoes:
            print("Não foram realizadas movimentações.".center(40))
        else:
            for transacao in self.transacoes:
                print(transacao.center(40))
        print("=============================".center(40))


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)


#funcoes utilitarias

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ").strip()
    usuario_existente = any(u.cpf == cpf for u in usuarios)
    if usuario_existente:
        print("Usuário já existente com esse CPF.".center(40))
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    try:
        datetime.strptime(data_nascimento, "%d-%m-%Y")
    except ValueError:
        print("Data de nascimento inválida.".center(40))
        return
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    novo_usuario = Cliente(nome, cpf, data_nascimento, endereco)
    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso!".center(40))


def criar_conta(numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = next((u for u in usuarios if u.cpf == cpf), None)

    if usuario:
        nova_conta = ContaCorrente(numero_conta, usuario)
        usuario.adicionar_conta(nova_conta)
        contas.append(nova_conta)
        print("Conta criada com sucesso!".center(40))
        print(nova_conta)
    else:
        print("Usuário não encontrado.".center(40))


#menu

menu = f"""
==============================
 Bem-vindo ao {banco_name}!
==============================
Escolha uma operação:

[d] Depositar
[s] Sacar
[e] Extrato
[l] Limite de Saque Diário
[n] Novo Usuário
[cc] Criar Conta Corrente
[lc] Listar Contas
[c] Contato
[q] Sair
==============================
=> """

#loop do menu

while True:
    opcao = input(menu)

    if opcao == "d":
        cpf = input("Informe o CPF do titular: ").strip()
        cliente = next((u for u in usuarios if u.cpf == cpf), None)
        if cliente and cliente.contas:
            valor = float(input("Informe o valor do depósito: "))
            transacao = Deposito(valor)
            cliente.realizar_transacao(cliente.contas[0], transacao)
        else:
            print("Cliente ou conta não encontrado.".center(40))

    elif opcao == "s":
        cpf = input("Informe o CPF do titular: ").strip()
        cliente = next((u for u in usuarios if u.cpf == cpf), None)
        if cliente and cliente.contas:
            valor = float(input("Informe o valor do saque: "))
            transacao = Saque(valor)
            cliente.realizar_transacao(cliente.contas[0], transacao)
        else:
            print("Cliente ou conta não encontrado.".center(40))

    elif opcao == "e":
        cpf = input("Informe o CPF do titular: ").strip()
        cliente = next((u for u in usuarios if u.cpf == cpf), None)
        if cliente and cliente.contas:
            cliente.contas[0].historico.imprimir()
            print(f"\nSaldo: R$ {cliente.contas[0].saldo:.2f}".center(40))
        else:
            print("Cliente ou conta não encontrado.".center(40))

    elif opcao == "l":
        print(f"\nLimite diário de saque: R$ 500.00".center(40))

    elif opcao == "c":
        print(" Contato ".center(40, "="))
        print("\nContato: suporte@notdessabank.com")
        print("Telefone: 0800-123-456")
        print(f"{contato}")
        print("\n")
        print("Caso tenha alguma dúvida,".center(40))
        print("entre em contato conosco.".center(40))
        print("\n")
        print("Volte Sempre!".center(40))
        print("=".center(40, "="))

    elif opcao == "n":
        criar_usuario(usuarios)

    elif opcao == "cc":
        numero_conta = len(contas) + 1
        criar_conta(numero_conta, usuarios)

    elif opcao == "lc":
        for conta in contas:
            print("=" * 40)
            print(str(conta).center(40))

    elif opcao == "q":
        print(" Sair ".center(40, "="))
        print(f"Obrigado por usar {banco_name}!".center(40))
        print("Tenha um bom dia!".center(40))
        print("=".center(40, "="))
        break

    else:
        print("Operação inválida...".center(40))
