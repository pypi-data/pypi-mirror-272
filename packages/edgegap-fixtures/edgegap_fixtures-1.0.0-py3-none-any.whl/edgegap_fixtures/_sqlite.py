import pytest
from sqlmodel import Session, SQLModel, StaticPool, create_engine

SQLALCHEMY_DATABASE_URL = 'sqlite://'


@pytest.fixture(scope='session')
def mock_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(bind=engine)

    return engine


@pytest.fixture(scope='function')
def mock_sqlite(mock_engine):
    connection = mock_engine.connect()
    transaction = connection.begin()

    try:
        yield Session(bind=connection)
    finally:
        transaction.rollback()

        for tbl in reversed(SQLModel.metadata.sorted_tables):
            connection.execute(tbl.delete())

        connection.commit()
        connection.close()


@pytest.fixture(scope='function')
def mock_session(mock_engine):
    db = Session(bind=mock_engine)
    try:
        yield db
    finally:
        db.close()
