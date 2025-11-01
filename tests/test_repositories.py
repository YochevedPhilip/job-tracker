from app.repositories.user_repository import UserRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.process_repository import ProcessRepository
from app.repositories.changelog_repository import ChangelogRepository

from app.models.user_model import User
from app.models.company_model import Company
from app.models.process_model import Process, StatusEnum
from app.models.changelog_model import Changelog


# -------------------------------------------------------------------------
# USER REPOSITORY
# -------------------------------------------------------------------------
def test_user_repository_crud(session):
    repo = UserRepository(session)
    user = User(name="RepoUser", email="repo@example.com", password="1234")

    # Create
    created = repo.create(user)
    assert created.id is not None

    # Read
    fetched = repo.get_by_id(created.id)
    assert fetched.email == "repo@example.com"

    # Update
    updated = repo.update(created.id, name="UpdatedRepoUser")
    assert updated.name == "UpdatedRepoUser"

    # Delete
    deleted = repo.delete(created.id)
    assert deleted is True
    assert repo.get_by_id(created.id) is None


# -------------------------------------------------------------------------
# COMPANY REPOSITORY
# -------------------------------------------------------------------------
def test_company_repository_crud(session, user_fixture):
    repo = CompanyRepository(session)
    company = Company(name="RepoCompany", user_id=user_fixture.id)

    created = repo.create(company)
    assert created.id is not None

    fetched = repo.get_by_id(created.id)
    assert fetched.name == "RepoCompany"

    updated = repo.update(created.id, name="UpdatedCo")
    assert updated.name == "UpdatedCo"

    deleted = repo.delete(created.id)
    assert deleted is True


# -------------------------------------------------------------------------
# PROCESS REPOSITORY
# -------------------------------------------------------------------------
def test_process_repository_crud(session, user_fixture, company_fixture):
    repo = ProcessRepository(session)
    process = Process(
        job_number="RepoJob",
        user_id=user_fixture.id,
        company_id=company_fixture.id,
        status=StatusEnum.CV_SENT
    )

    created = repo.create(process)
    assert created.id is not None
    assert created.status == StatusEnum.CV_SENT

    fetched = repo.get_by_id(created.id)
    assert fetched.job_number == "RepoJob"

    updated = repo.update(created.id, status=StatusEnum.REJECTED)
    assert updated.status == StatusEnum.REJECTED

    deleted = repo.delete(created.id)
    assert deleted is True


# -------------------------------------------------------------------------
# CHANGELOG REPOSITORY
# -------------------------------------------------------------------------
def test_changelog_repository_crud(session, process_fixture):
    repo = ChangelogRepository(session)
    change = Changelog(changed_to=StatusEnum.OFFER_RECEIVED, process_id=process_fixture.id)

    created = repo.create(change)
    assert created.id is not None

    fetched = repo.get_by_id(created.id)
    assert fetched.changed_to == StatusEnum.OFFER_RECEIVED

    deleted = repo.delete(created.id)
    assert deleted is True
