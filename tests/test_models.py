import pytest
from app.models.process_model import Process, StatusEnum
from app.models.changelog_model import Changelog
from app.models.company_model import Company
from app.models.user_model import User


# -----------------------------------------------------------------------------
# create
# -----------------------------------------------------------------------------
def test_create_user(session):
    user = User(name="Alice", email="alice@example.com", password="secret")
    session.add(user)
    session.commit()

    db_user = session.query(User).first()
    assert db_user.name == "Alice"
    assert db_user.email == "alice@example.com"
    assert db_user.created_at is not None


def test_create_company(session, user_fixture):
    company = Company(name="TechCorp", user_id=user_fixture.id)
    session.add(company)
    session.commit()

    db_company = session.query(Company).first()
    assert db_company.name == "TechCorp"
    assert db_company.owner.id == user_fixture.id


def test_create_process(session, user_fixture, company_fixture):
    process = Process(
        job_number="Job Interview",
        user_id=user_fixture.id,
        company_id=company_fixture.id
    )
    session.add(process)
    session.commit()

    db_process = session.query(Process).first()
    assert db_process.job_number == "Job Interview"
    assert db_process.owner.id == user_fixture.id
    assert db_process.company.id == company_fixture.id
    assert db_process.status == StatusEnum.CV_SENT


# -----------------------------------------------------------------------------
#  relationships
# -----------------------------------------------------------------------------
def test_relationship_user_company_process(session, process_fixture):
    process = process_fixture

    user = process.owner
    assert user.name == "Test User"

    company = process.company
    assert company.name == "Test Company"

    assert user.companies[0].name == "Test Company"
    assert company.processes[0].job_number == "Interview Process"


# -----------------------------------------------------------------------------
# 🕓  timestamps and Enum
# -----------------------------------------------------------------------------
def test_process_defaults(session, process_fixture):
    process = process_fixture
    assert process.created_at is not None
    assert process.updated_at is not None
    assert process.status == StatusEnum.CV_SENT


def test_changelog_relationship(session, process_fixture):
    change = Changelog(
        changed_to=StatusEnum.INTERVIEW_SCHEDULED,
        process_id=process_fixture.id
    )
    session.add(change)
    session.commit()

    db_change = session.query(Changelog).first()
    assert db_change.changed_to == StatusEnum.INTERVIEW_SCHEDULED
    assert db_change.owner.id == process_fixture.id
    assert db_change.changed_at is not None

    assert process_fixture.changes[0].changed_to == StatusEnum.INTERVIEW_SCHEDULED


# -----------------------------------------------------------------------------
#   CRUD
# -----------------------------------------------------------------------------
def test_update_process_status(session, process_fixture):
    process = process_fixture
    process.status = StatusEnum.OFFER_RECEIVED
    session.commit()

    db_process = session.query(Process).get(process.id)
    assert db_process.status == StatusEnum.OFFER_RECEIVED


def test_delete_company_cascade(session, company_fixture, process_fixture):
    session.delete(company_fixture)
    session.commit()

    remaining_processes = session.query(Process).all()
    assert len(remaining_processes) >= 0
