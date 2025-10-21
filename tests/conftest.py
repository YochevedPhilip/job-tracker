import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from fastapi.testclient import TestClient
from app.main import app

# -----------------------------------------------------------------------------
# DATABASE FIXTURES
# -----------------------------------------------------------------------------

@pytest.fixture(scope="session")
def engine():

    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def session(engine):

    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection, autoflush=False, autocommit=False)
    session = SessionLocal()

    yield session
    session.close()
    transaction.rollback()
    connection.close()


# -----------------------------------------------------------------------------
# TEST CLIENT FIXTURE
# -----------------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():

    with TestClient(app) as client:
        yield client


# -----------------------------------------------------------------------------
# SAMPLE DATA FIXTURES
# -----------------------------------------------------------------------------

@pytest.fixture
def user_fixture(session):

    from app.models.user_model import UserModel
    user = UserModel(name="Test User", email="user@example.com", password="pass123")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def company_fixture(session, user_fixture):

    from app.models.company_model import CompanyModel
    company = CompanyModel(name="Test Company", user_id=user_fixture.id)
    session.add(company)
    session.commit()
    return company


@pytest.fixture
def process_fixture(session, company_fixture, user_fixture):

    from app.models.process_model import ProcessModel
    process = ProcessModel(job_number="Interview Process", company_id=company_fixture.id, user_id=user_fixture.id)
    session.add(process)
    session.commit()
    return process
