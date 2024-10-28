from dataclasses import asdict

# create_engine utilizado no teste com engine
from sqlalchemy import select

# from sqlalchemy.orm.session import Session
# table_registry utilizado no teste com engine
from fast_zero.models import User

"""
Este teste adiciona um novo usuário ao banco de dados, faz commit das mudanças,
e depois verifica se o usuário foi devidamente criado consultando-o pelo nome
de usuário. Se o usuário foi criado corretamente, o teste passa.
Caso contrário, o teste falha, indicando que há algo errado com nossa função
de criação de usuário."""


# Teste usando Session em uma fixture (o recomendado para se envitar repetição
# de código)
def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='alice', password='secret', email='teste@test'
        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == {
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'email': 'teste@test',
        'created_at': time,
        'updated_at': time,  # Exercício
    }


"""
# Engine e Session
from sqlalchemy import create_engine

def test_create_user_engine():
    # banco 'físico local'
    # engine = create_engine('sqlite:///test_database.db')

    # banco em memória que é apagado sempre que o teste termina (so funciona no
    # sqlite)
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(
            username='marilia',
            email='marilia@bolo.com',
            password='mar123ili@',
        )

        session.add(user)
        session.commit()
        session.refresh(user)

    # assert user.username == 'marilia'
    assert user.id == 1
"""
