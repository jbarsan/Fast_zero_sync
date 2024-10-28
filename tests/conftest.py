from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


"""
Essa fixture está configurando e limpando um banco de dados de teste para
cada teste que o solicita, assegurando que cada teste seja isolado
e tenha seu próprio ambiente limpo para trabalhar. Isso é uma boa prática em
testes de unidade, já que queremos que cada teste seja independente e não
afete os demais.

create_engine('sqlite:///:memory:'):
cria um mecanismo de banco de dados SQLite em memória usando SQLAlchemy.
Este mecanismo será usado para criar uma sessão de banco de dados para
nossos testes.

table_registry.metadata.create_all(engine): cria todas as tabelas no
banco de dados de teste antes de cada teste que usa a fixture session.

Session(engine): cria uma sessão Session para que os testes possam se
comunicar com o banco de dadosvia engine.

yield session: fornece uma instância de Session que será injetada
em cada teste que solicita a fixture session. Essa sessão será
usada para interagir com o banco de dados de teste.

table_registry.metadata.drop_all(engine): após cada teste que usa a fixture
session, todas as tabelas do banco de dados de teste são eliminadas,
garantindo que cada teste seja executado contra um banco de dados limpo.
"""


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    # with significa 'gerenciamento de contexto' (live 43)
    with Session(engine) as session:
        # yield define o que será executado antes ('arruma' pra rodar o teste)
        # yield é um gerador (TODO: Estudar sobre geradores em python.
        # Live 151)
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
