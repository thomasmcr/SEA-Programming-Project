from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.database.core import base, get_db
from src.dependencies.auth_dependencies import check_auth
from src.main import app
from src.database.models import User

DATABASE_URL = "sqlite:///test_tickets.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base.metadata.create_all(bind=engine)

@pytest.fixture()
def clear_db():
    base.metadata.create_all(bind=engine)
    yield
    base.metadata.drop_all(bind=engine)

def override_get_db():
    try: 
        db = session()
        yield db
    finally: 
        db.close()

async def override_check_auth():
    test_user = User(id=0, username="test_admin", password="test", is_admin=True)
    return test_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[check_auth] = override_check_auth
test_client = TestClient(app) 