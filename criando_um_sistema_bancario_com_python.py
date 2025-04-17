from abc import ABC, abstractmethod
from datetime import date, datetime

AGENCIA = "0001"

def menu_atual(nome_menu: str):
    print("\n", nome_menu.center(50, "="))

# Gerador automático de número de contas
def gerador_contas():
    numero_conta = 1
    while True:
        yield numero_conta
        numero_conta += 1

# variável para armazenar o gerador
proxima_conta = gerador_contas()

class Historico:
    def __init__(self, transacoes: list["Transacao"] | None = None):
        self._transacoes = transacoes if transacoes is not None else []
    
    def adicionar_transacao(self, transacao: "Transacao"):
        self._transacoes.append(transacao)

    # Conta a quantidade de saques efetuados no histórico
    def conta_saques(self) -> int:
        numero_saques = 0
        for transacao in self._transacoes:
            if type(transacao) == Saque:
                numero_saques += 1
        return numero_saques
    
    def emitir_extrato(self) -> str:
        extrato = ""
        
        if self._transacoes:
            for transacao in self._transacoes:
                extrato += f"{transacao.__class__.__name__}: R${transacao._valor:.2f}\n"
        else:
            extrato = "Nenhuma transação registrada..."
        return extrato


class Conta:
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: "Cliente"):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    def saldo(self) -> float:
        return f"Saldo atual - R${self._saldo:.2f}"
    
    def extrato(self) -> str:
        menu_atual("Extrato")
        print(self._historico.emitir_extrato())
        print(self.saldo())

    def get_agencia(self) -> str:
        return self._agencia
    
    def get_numero(self) -> int:
        return self._numero
    
    @classmethod
    def nova_conta(cls, cliente: "Cliente", numero: int) -> "Conta":
        conta_criada = cls(saldo=0, numero=numero, agencia=AGENCIA, cliente=cliente)
        print("Conta criada com sucesso!")
        print(f"Agência: {conta_criada._agencia} - Conta: {conta_criada._numero}")
        print("Utilize o menu [a] Acessar para fazer login")
        return conta_criada
    
    def sacar(self, valor: float) -> bool:
        if valor < 0:
            print("O valor informado deve ser positivo...")
            return False
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False
        self._saldo -= valor
        print(f"Saque de R${valor:.2f} efetuado com sucesso.")
        return True
        
    def depositar(self, valor: float) -> bool:
        menu_atual("Depósito")
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R${valor:.2f} efetuado com sucesso.")
            return True
        print("Valor inválido.")
        return False

class ContaCorrente(Conta):
    def __init__(self, limite: float = 500., limite_saques: int = 3, **kwargs):
        super().__init__(**kwargs)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        menu_atual("Saque")
        if self._historico.conta_saques() >= self._limite_saques:
            print("Limites de saques diários excedido.")
            return False
        if valor > self._limite:
            print(f"O valor informado deve ser menor que R${self._limite:.2f}.")
            return False
        return super().sacar(valor)        

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(conta: Conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        conta._historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta: Conta):
        conta._historico.adicionar_transacao(self)

class Cliente:
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao | None = None):
        if type(transacao) == Saque:
            # Se o saque ocorrer com sucesso, há o registro no histórico
            if conta.sacar(transacao._valor):
                transacao.registrar(conta)
        elif type(transacao) == Deposito:
            # Se o depósito ocorrer com sucesso, há o registro no histórico
            if conta.depositar(transacao._valor):
                transacao.registrar(conta)
        elif transacao is None:
            conta.extrato()
        else:
            print("Transação inexistente.")

    def adicionar_conta(self, conta: Conta | None = None):
        menu_atual("Adicionar conta")
        if conta is None:
            self._contas.append(ContaCorrente.nova_conta(self, next(proxima_conta)))
        else:
            print("Conta adicionada!")
            self._contas.append(conta)

    def listar_contas(self):
        menu_atual("Lista de contas")
        if self._contas:
            for conta in self._contas:
                print(f"Agencia: {conta._agencia} Conta: {conta._numero}")
        else:
            print("O cliente ainda não possui contas cadastradas...")

    def get_conta(self, agencia: str, numero: int) -> Conta | None:
        for conta in self._contas:
            if conta._agencia == agencia and conta._numero == numero:
                return conta


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, **kwargs):
        super().__init__(**kwargs)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    def get_nome(self):
        return self._nome
    
    def get_cpf(self):
        return self._cpf


def menu(cliente: PessoaFisica | None = None, conta: ContaCorrente | None = None) -> str:
    menu_text = f"""

{'BANCO PYTHON'.center(50, "=")}
{'Bem-vindo, ' + cliente.get_nome() if cliente else ""}
{'Estamos na Agência: ' + conta.get_agencia() + ' - Conta: ' + str(conta.get_numero()) if conta else ""}

[a] Acessar
[nu] Criar novo usuário"""
    if cliente:
        menu_text += f"""
[nc] Criar nova conta
[lc] Listar contas"""
    if conta:
        menu_text += f"""
[d] Depositar
[s] Sacar
[e] Extrato"""
    menu_text += f"""
[q] Sair
    
=> """
    return input(menu_text)

def acessar(
    cliente_inicial: PessoaFisica | None, 
    conta_inicial: ContaCorrente | None, 
    clientes: list[PessoaFisica]
) -> tuple[PessoaFisica, None] | tuple[PessoaFisica | None, ContaCorrente | None] | tuple[PessoaFisica, Conta]:
    menu_atual("Acessar")
    opcao = input(f"""Escolha uma opção
          
[1] Acessar pelo CPF (loga o usuário)
[2] Acessar via Agencia e Conta (loga o usuário e carrega a conta)
[3] Voltar
                  
=> """)
    
    if opcao == "1":
        cpf = input("Digite seu CPF (apenas números): ")
        for cliente in clientes:
            if cliente.get_cpf() == cpf:
                # Quando dá certo, retorna apenas o cliente, sem conta
                return cliente, None
        print("Não foi encontrado cliente com o CPF informado.")
        return cliente_inicial, conta_inicial
    elif opcao == "2":
        agencia = input("Digite o número de sua agência (com zeros): ")
        numero_conta = input("Digite o número de sua conta: ")
        if numero_conta.isdigit():
            numero_conta = int(numero_conta)
        else:
            print("Número de conta inválido...")
            return cliente_inicial, conta_inicial
        for cliente in clientes:
            conta = cliente.get_conta(agencia, numero_conta)
            if conta:
                # Quando dá certo, retorna cliente e conta atualizados
                return cliente, conta
        print("Conta não encontrada...")
        return cliente_inicial, conta_inicial
    elif opcao == "3":
        return cliente_inicial, conta_inicial
    else:
        print("Opção inválida...")
        return cliente_inicial, conta_inicial


def novo_usuario(clientes: list[PessoaFisica]) -> tuple[PessoaFisica, list[PessoaFisica]] | tuple[None, None]:
    def checar_cpf(cpf: str):
        return len(cpf) == 11
    
    cpf = input("Digite seu CPF (apenas números): ")
    if not checar_cpf(cpf):
        print("CPF inválido...")
        return None, None
    nome = input("Digite seu nome completo: ")
    data_nascimento = input("Digite sua data de nascimento (dd/mm/yyyy): ")
    try:
        data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
    except:
        print("Data de nascimento inválida...")
        return None, None
    endereco = input("Digite seu endereço completo: ")
    cliente = PessoaFisica(cpf, nome, data_nascimento, endereco=endereco)
    clientes.append(cliente)
    return cliente, clientes

def nova_conta(cliente: PessoaFisica) -> PessoaFisica:
    cliente.adicionar_conta()
    return cliente

def deposito(cliente: Cliente, conta: Conta):
    valor = input("Digite o valor que pretende depositar: R$").replace(",", ".")
    try:
        valor = float(valor)
        cliente.realizar_transacao(conta, Deposito(valor))
    except:
        print("O valor informado é inválido...")

def saque(cliente: Cliente, conta: Conta):
    valor = input("Digite o valor que pretende sacar: ").replace(",", ".")
    try:
        valor = float(valor)
        cliente.realizar_transacao(conta, Saque(valor))
    except:
        print("O valor informado é inválido...")

def extrato(cliente: Cliente, conta: Conta):
    cliente.realizar_transacao(conta)


if __name__ == "__main__":
    clientes = []
    cliente_atual = None
    conta_atual = None

    while True:
        opcao = menu(cliente=cliente_atual, conta=conta_atual)

        if opcao == "a":
            cliente_atual, conta_atual = acessar(cliente_atual, conta_atual, clientes)
        elif opcao == "nu":
            cliente_atual, clientes = novo_usuario(clientes)
        elif opcao == "nc":
            cliente_atual = nova_conta(cliente_atual)
        elif opcao == "lc":
            cliente_atual.listar_contas()
        elif opcao == "d":
            deposito(cliente_atual, conta_atual)
        elif opcao == "s":
            saque(cliente_atual, conta_atual)
        elif opcao == "e":
            extrato(cliente_atual, conta_atual)
        elif opcao == "q":
            print("Obrigado por utilizar o BANCO PYTHON")
            break
        else:
            menu_atual("Erro")
            print("Operação inválida, por favor selecione novamente a operação desejada.")