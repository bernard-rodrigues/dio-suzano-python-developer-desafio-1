from datetime import datetime

menu = f"""

{'BANCO PYTHON'.center(30, "-")}

[nu] Criar novo usuário
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

def deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R${valor:.2f}\n"
        print(f"Depósito de R${valor:.2f} efetuado com sucesso.")
    else:
        print("Valor inválido")

    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print("Limites de saques diários excedido")
    elif valor < 0 or valor > limite:
        print(f"Valor inválido. Seu saque deve ser um valor positivo e menor que R${limite:.2f}")
    elif valor > saldo:
        print("Saldo insuficiente.")
    else:
        saldo -= valor
        extrato += f"Saque: R${valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R${valor:.2f} efetuado com sucesso.")
    
    return saldo, extrato, numero_saques

def emitir_extrato(saldo, /, *, extrato):
    print("Extrato".center(30, "-"), end="\n\n")

    if(extrato):
        print(extrato, end="\n")
    
    print(f"Saldo atual: R${saldo:.2f}")

def novo_usuario(usuarios, id_atual, nome, data_nascimento, cpf, endereco):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Já existe usuário cadastrado com o CPF informado.")
            return usuarios, id_atual
    
    usuarios.append({
        "agencia": "0001",
        "conta": id_atual,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    id_atual += 1
    print(f"Olá, {nome}! Bem-vindo ao BANCO PYTHON!")

    return usuarios, id_atual

usuarios = []
id_atual = 1

saldo = 0
extrato = ""
numero_saques = 0
LIMITE = 500
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)

    if opcao == "nu":
        nome = input("Digite seu nome: ")
        data_nascimento = datetime.strptime(input("Digite sua data de nascimento (dd/mm/aaaa): "), "%d/%m/%Y").date()
        cpf = input("Digite seu CPF (apenas números): ")
        
        print("\nEndereço:")
        logradouro = input("Digite seu logradouro (sem número): ")
        numero = input("Digite o número de sua residência (e complemento, se houver): ")
        bairro = input("Digite seu bairro: ")
        cidade = input("Digite o nome de sua cidade: ")
        uf = input("Digite a sigla de seu estado:" ).upper()
        endereco = {
            "logradouro": logradouro,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "uf": uf,
        }

        novo_usuario(usuarios, id_atual, nome, data_nascimento, cpf, endereco)


    elif opcao == "d":
        print("Depósito".center(30, "-"), end="\n\n")
        
        # Previne exibição de erro de conversão de caractere não numérico
        try:
            valor = float(input("Digite o valor do depósito: R$"))
            saldo, extrato = deposito(saldo, valor, extrato)
        
        # Mensagem exibida em caso de entrada de caractere não numérico
        except:
            print("Valor inválido")

    elif opcao == "s":
        print("Saque".center(30, "-"), end="\n\n")

        # Previne exibição de erro de conversão de caractere não numérico
        try:
            valor = float(input("Digite o valor do saque: R$"))
            saldo, extrato, numero_saques = saque(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato, 
                limite=LIMITE, 
                numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES
            )

        # Mensagem exibida em caso de entrada de caractere não numérico
        except:
            print("Valor inválido")

    elif opcao == "e":
        emitir_extrato(saldo, extrato=extrato)

    elif opcao == "q":
        print("Obrigado por utilizar o BANCO PYTHON")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")