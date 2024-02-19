import textwrap


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Transacao:
    def registrar(self, conta):
        pass


class Conta:
    def __init__(self, cliente, numero, agencia):
        self.cliente = cliente
        self.numero = numero
        self.agencia = agencia
        self.saldo = 0
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        self.saldo += valor
        return True


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite, limite_saque):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        if valor <= self.saldo + self.limite and len(self.historico.transacoes) < self.limite_saque:
            self.saldo -= valor
            return True
        else:
            print("\n@@@ Operação falhou! Saldo insuficiente ou limite de saques excedido. @@@")
            return False


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)
        conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"Depósito: R$ {self.valor:.2f}"


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"Saque: R$ {self.valor:.2f}"


class Cliente:
    def __init__(self, nome, endereco):
        self.nome = nome
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, endereco, cpf, data_nascimento):
        super().__init__(nome, endereco)
        self.cpf = cpf
        self.data_nascimento = data_nascimento


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.LIMITE_SAQUES = 3
        self.AGENCIA = "0001"

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente números): ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        novo_usuario = PessoaFisica(nome, endereco, cpf, data_nascimento)
        self.usuarios.append(novo_usuario)
        print("=== Usuário criado com sucesso! ===")

    def filtrar_usuario(self, cpf):
        usuarios_filtrados = [usuario for usuario in self.usuarios if isinstance(usuario, PessoaFisica) and usuario.cpf == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)

        if not usuario:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
            return

        numero_conta = len(self.contas) + 1
        nova_conta = ContaCorrente(usuario, numero_conta, self.AGENCIA, limite=500, limite_saque=self.LIMITE_SAQUES)
        usuario.adicionar_conta(nova_conta)
        self.contas.append(nova_conta)
        print("\n=== Conta criada com sucesso! ===")

    def listar_contas(self):
        for conta in self.contas:
            print("=" * 100)
            print(f"Agência:\t{conta.agencia}")
            print(f"C/C:\t\t{conta.numero}")
            print(f"Titular:\t{conta.cliente.nome}")

    def exibir_extrato(self):
        numero_conta = int(input("Informe o número da conta: "))
        for conta in self.contas:
            if conta.numero == numero_conta:
                print("\n================ EXTRATO ================")
                for transacao in conta.historico.transacoes:
                    print(transacao)
                print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
                print("==========================================")


def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text))


def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            numero_conta = int(input("Informe o número da conta: "))
            conta_encontrada = False
            for conta in banco.contas:
                if conta.numero == numero_conta:
                    transacao = Deposito(valor)
                    transacao.registrar(conta)
                    conta_encontrada = True
                    break
            if not conta_encontrada:
                print("\n@@@ Número de conta não existe! @@@")

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            numero_conta = int(input("Informe o número da conta: "))
            conta_encontrada = False
            for conta in banco.contas:
                if conta.numero == numero_conta:
                    transacao = Saque(valor)
                    transacao.registrar(conta)
                    conta_encontrada = True
                    break
            if not conta_encontrada:
                print("\n@@@ Número de conta não existe! @@@")
        
        elif opcao == "e":
            banco.exibir_extrato()

        elif opcao == "nu":
            banco.criar_usuario()

        elif opcao == "nc":
            banco.criar_conta()

        elif opcao == "lc":
            banco.listar_contas()

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
