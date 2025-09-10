import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlmodel import Session
from unittest.mock import AsyncMock

@pytest.fixture
def mock_session():
    session = AsyncMock(spec=Session)
    return session

@pytest.fixture
def mock_rack_repository(mock_session):
    repository = AsyncMock()
    repository.session = mock_session
    return repository

@pytest.fixture
def mock_device_repository(mock_session):
    repository = AsyncMock()
    repository.session = mock_session
    return repository

@pytest.fixture
def rack_service(mock_rack_repository, mock_device_repository):
    from app.services import RackService
    return RackService(
        rack_repository=mock_rack_repository,
        device_repository=mock_device_repository
    )