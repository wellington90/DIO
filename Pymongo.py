import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['banco']
clientes_collection = db['clientes']
contas_collection = db['contas']


documento1 = {
    'id': 1,
    'nome': 'Fulano',
    'cpf': '123456789',
    'endereco': 'Rua A'
}

documento2 = {
    'id': 2,
    'nome': 'Ciclano',
    'cpf': '987654321',
    'endereco': 'Rua B'
}


cliente1_id = clientes_collection.insert_one(documento1).inserted_id
cliente2_id = clientes_collection.insert_one(documento2).inserted_id


conta1_cliente1 = {
    'tipo': 'corrente',
    'agencia': '001',
    'num': 123,
    'saldo': 1000.00,
    'cliente_id': cliente1_id
}

conta2_cliente1 = {
    'tipo': 'poupanca',
    'agencia': '001',
    'num': 456,
    'saldo': 500.00,
    'cliente_id': cliente1_id
}

conta1_cliente2 = {
    'tipo': 'corrente',
    'agencia': '002',
    'num': 789,
    'saldo': 2000.00,
    'cliente_id': cliente2_id
}

contas_collection.insert_many([conta1_cliente1, conta2_cliente1, conta1_cliente2])

#cpf_procurado = '123456789'
cpf_procurado = '987654321'


cliente = clientes_collection.find_one({'cpf': cpf_procurado})

if cliente:
    print(f"Informações do cliente com CPF {cpf_procurado}:")
    print(f"Nome: {cliente['nome']}")
    print(f"CPF: {cliente['cpf']}")
    print(f"Endereço: {cliente['endereco']}")

    # client CPF
    contas_cliente = contas_collection.find({'cliente_id': cliente['_id']})
    print(f"Contas do cliente {cliente['nome']}:")
    saldo_contas = []  
    
    for conta in contas_cliente:
        print(f"Tipo: {conta['tipo']}, Agência: {conta['agencia']}, Número: {conta['num']}, Saldo: {conta['saldo']}")
        saldo_contas.append(conta['saldo'])  

    #total accounts client
    saldo_total = sum(saldo_contas)  
    print(f"Saldo total do cliente {cliente['nome']}: {saldo_total}")

else:
    print('Cliente não encontrado.')
