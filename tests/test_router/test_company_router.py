import pytest
from fastapi import status
from app.models.company_model import Company
from app.schemas.company_schema import CompanyCreate
from app.services.company_service import CompanyService
from app.repositories.company_repository import CompanyRepository


# ---------------------------------------------------------------------
# REPOSITORY TESTS
# ---------------------------------------------------------------------
def test_get_by_user_returns_companies(session, user_fixture, company_fixture):
    repo = CompanyRepository(session)
    companies = repo.get_by_user(user_fixture.id)

    assert len(companies) > 0
    assert any(c.name == company_fixture.name for c in companies)
    assert all(isinstance(c, Company) for c in companies)


def test_get_by_user_no_companies(session, user_fixture):
    repo = CompanyRepository(session)
    companies = repo.get_by_user(9999)
    assert companies == []


def test_get_by_name_returns_company(session, company_fixture):
    repo = CompanyRepository(session)
    result = repo.get_by_name_and_user(company_fixture.name, company_fixture.user_id)
    assert result is not None
    assert result.name == company_fixture.name


def test_get_by_name_not_found(session):
    repo = CompanyRepository(session)
    result = repo.get_by_name_and_user("NonExistingCompany", 1)
    assert result is None


# ---------------------------------------------------------------------
# SERVICE TESTS
# ---------------------------------------------------------------------
def test_get_or_create_returns_existing_company(session, user_fixture, company_fixture):
    service = CompanyService(session)
    company_in = Company(name=company_fixture.name, user_id=user_fixture.id)

    company = service.get_or_create(company_in)
    assert company is not None


def test_get_or_create_creates_new_company(session, user_fixture):
    service = CompanyService(session)
    company_in = Company(name="BrandNewCo", user_id=user_fixture.id)

    company = service.get_or_create(company_in)

    assert company is not None
    assert company_in.name == "BrandNewCo"


# ---------------------------------------------------------------------
# ROUTER TESTS
# ---------------------------------------------------------------------
def test_read_companies_by_user_returns_list(client, user_fixture, company_fixture):
    response = client.get(f"/companies/{user_fixture.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(c["name"] == company_fixture.name for c in data)


def test_read_companies_by_user_empty_list(client, user_fixture):
    response = client.get("/companies/9999")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == []


# ---------------------------------------------------------------------
# INTEGRATION-LIKE TEST (repo + service + route)
# ---------------------------------------------------------------------
def test_full_company_flow(session, client, user_fixture):
    service = CompanyService(session)
    company_in = Company(name="FlowCompany", user_id=user_fixture.id)
    created_company = service.get_or_create(company_in)
    session.commit()

    response = client.get(f"/companies/{user_fixture.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert any(c["name"] == "FlowCompany" for c in data)
