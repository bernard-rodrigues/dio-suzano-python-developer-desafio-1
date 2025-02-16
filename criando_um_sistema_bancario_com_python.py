menu = f"""

{'BANCO PYTHON'.center(30, "-")}

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        print("Depósito".center(30, "-"), end="\n\n")
        
        # Previne exibição de erro de conversão de caractere não numérico
        try:
            valor = float(input("Digite o valor do depósito: R$"))
            
            if valor > 0:
                saldo += valor
                extrato += f"Depósito: R${valor:.2f}\n"
                print(f"Depósito de R${valor:.2f} efetuado com sucesso.")
            else:
                print("Valor inválido")
        
        # Mensagem exibida em caso de entrada de caractere não numérico
        except:
            print("Valor inválido")

    elif opcao == "s":
        print("Saque".center(30, "-"), end="\n\n")

        if numero_saques < 3:
            
            # Previne exibição de erro de conversão de caractere não numérico
            try:
                valor = float(input("Digite o valor do saque: R$"))

                if 0 < valor <= 500:
                    if valor < saldo:
                        saldo -= valor
                        extrato += f"Saque: R${valor:.2f}\n"
                        numero_saques += 1
                        print(f"Saque de R${valor:.2f} efetuado com sucesso.")
                    else:
                        print("Saldo insuficiente.")
                else:
                    print("Valor inválido. Seu saque deve ser um valor positivo e menor que R$500.00")
            
            # Mensagem exibida em caso de entrada de caractere não numérico
            except:
                print("Valor inválido")
        else:
            print("Limite de saques diários excedido.")

    elif opcao == "e":
        print("Extrato".center(30, "-"), end="\n\n")

        if(extrato):
            print(extrato, end="\n")
        
        print(f"Saldo atual: R${saldo:.2f}")

    elif opcao == "q":
        print("Obrigado por utilizar o BANCO PYTHON")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")