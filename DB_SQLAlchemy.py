from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///banco.db')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Conta(Base):
    __tablename__ = 'conta'

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey('cliente.id'))
    saldo = Column(Numeric)

    cliente = relationship("Cliente", back_populates="contas")

class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String)

    contas = relationship("Conta", back_populates="cliente")

Base.metadata.create_all(engine)

cliente1 = Cliente(nome='Fulano', cpf='123456789', endereco='Rua A')
cliente2 = Cliente(nome='Ciclano', cpf='987654321', endereco='Rua B')

session.add(cliente1)
session.add(cliente2)

session.commit()

conta1_cliente1 = Conta(tipo='Corrente', agencia='001', num=123, saldo=1000.00)
conta2_cliente1 = Conta(tipo='Poupança', agencia='002', num=456, saldo=500.00)
conta1_cliente2 = Conta(tipo='Corrente', agencia='003', num=789, saldo=2000.00)

cliente1.contas.append(conta1_cliente1)
cliente1.contas.append(conta2_cliente1)
cliente2.contas.append(conta1_cliente2)

session.add_all([conta1_cliente1, conta2_cliente1, conta1_cliente2])
session.commit()

clientes = session.query(Cliente).all()
for cliente in clientes:
    print(f'Cliente: {cliente.nome}, Contas:')
    for conta in cliente.contas:
        print(f'Tipo: {conta.tipo}, Agência: {conta.agencia}, Número: {conta.num}, Saldo: {conta.saldo}')
    print()

cliente = session.query(Cliente).filter_by(cpf='123456789').first()

if cliente:
    print(f'Contas do cliente {cliente.nome} (CPF: {cliente.cpf}):')
    for conta in cliente.contas:
        print(f'Tipo: {conta.tipo}, Agência: {conta.agencia}, Número: {conta.num}, Saldo: {conta.saldo}')
else:
    print('Cliente não encontrado.')

cliente_total = session.query(Cliente).filter_by(nome='Fulano').first()

if cliente_total:
    saldo_total = sum(conta.saldo for conta in cliente_total.contas)
    print(f'Saldo total do cliente {cliente_total.nome}: {saldo_total}')
else:
    print('Cliente Fulano não encontrado.')
