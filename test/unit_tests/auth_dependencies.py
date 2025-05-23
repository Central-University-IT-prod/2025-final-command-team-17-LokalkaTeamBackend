import pytest
import jwt
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException
from uuid import uuid4

from server.dependencies.auth_dependencies import get_current_user_from_cookie
from server.repositories.user import UserRepository


@pytest.fixture
def mock_db():
    """Create a mock AsyncSession"""
    db = AsyncMock()
    return db


@pytest.fixture
def mock_user():
    """Create a mock User object"""
    user = MagicMock()
    user.id = uuid4()
    user.email = "test@example.com"
    user.first_name = "Test User"
    user.role = "user"
    return user


@pytest.fixture
def mock_request():
    """Create a mock Request object"""
    request = MagicMock()
    request.cookies = {}
    request.headers = {}
    return request


@pytest.mark.asyncio
@patch("server.dependencies.auth_dependencies.UserRepository")
@patch("server.dependencies.auth_dependencies.jwt.decode")
async def test_get_current_user_from_cookie(mock_jwt_decode, MockUserRepo, mock_db, mock_user, mock_request):
    """Test retrieving current user from cookie"""
    # Setup
    user_id = str(mock_user.id)
    mock_jwt_decode.return_value = {"sub": user_id}
    
    mock_user_repo = MagicMock()
    mock_user_repo.get_by_id = AsyncMock(return_value=mock_user)
    MockUserRepo.return_value = mock_user_repo
    
    # Set token in cookie
    mock_request.cookies["access_token"] = "valid_token"
    
    # Execute
    result = await get_current_user_from_cookie(request=mock_request, db=mock_db)
    
    # Assert
    mock_jwt_decode.assert_called_once()
    MockUserRepo.assert_called_once_with(mock_db)
    mock_user_repo.get_by_id.assert_called_once_with(user_id)
    assert result == mock_user


@pytest.mark.asyncio
@patch("server.dependencies.auth_dependencies.UserRepository")
@patch("server.dependencies.auth_dependencies.jwt.decode")
async def test_get_current_user_from_header(mock_jwt_decode, MockUserRepo, mock_db, mock_user, mock_request):
    """Test retrieving current user from Authorization header"""
    # Setup
    user_id = str(mock_user.id)
    mock_jwt_decode.return_value = {"sub": user_id}
    
    mock_user_repo = MagicMock()
    mock_user_repo.get_by_id = AsyncMock(return_value=mock_user)
    MockUserRepo.return_value = mock_user_repo
    
    # Set token in Authorization header
    mock_request.cookies = {}  # No cookie
    mock_request.headers["Authorization"] = "Bearer valid_token"
    
    # Execute
    result = await get_current_user_from_cookie(request=mock_request, db=mock_db)
    
    # Assert
    mock_jwt_decode.assert_called_once()
    MockUserRepo.assert_called_once_with(mock_db)
    mock_user_repo.get_by_id.assert_called_once_with(user_id)
    assert result == mock_user


@pytest.mark.asyncio
async def test_no_token_provided(mock_db, mock_request):
    """Test when no token is provided"""
    # Setup - empty cookies and headers
    mock_request.cookies = {}
    mock_request.headers = {}
    
    # Execute and Assert
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user_from_cookie(request=mock_request, db=mock_db)
    
    assert excinfo.value.status_code == 401
    assert "Not authenticated" in excinfo.value.detail


@pytest.mark.asyncio
@patch("server.dependencies.auth_dependencies.jwt.decode")
async def test_invalid_token_payload(mock_jwt_decode, mock_db, mock_request):
    """Test when token payload is invalid (missing sub claim)"""
    # Setup
    mock_jwt_decode.return_value = {}  # No sub claim
    
    # Set token in cookie
    mock_request.cookies["access_token"] = "invalid_token"
    
    # Execute and Assert
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user_from_cookie(request=mock_request, db=mock_db)
    
    assert excinfo.value.status_code == 401
    assert "Invalid token payload" in excinfo.value.detail


@pytest.mark.asyncio
@patch("server.dependencies.auth_dependencies.jwt.decode")
async def test_jwt_decode_error(mock_jwt_decode, mock_db, mock_request):
    """Test when JWT token decoding fails"""
    # Setup
    mock_jwt_decode.side_effect = jwt.PyJWTError("Invalid token")
    
    # Set token in cookie
    mock_request.cookies["access_token"] = "corrupted_token"
    
    # Execute and Assert
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user_from_cookie(request=mock_request, db=mock_db)
    
    assert excinfo.value.status_code == 401
    assert "Invalid authentication credentials" in excinfo.value.detail


@pytest.mark.asyncio
@patch("server.dependencies.auth_dependencies.UserRepository")
@patch("server.dependencies.auth_dependencies.jwt.decode")
async def test_user_not_found(mock_jwt_decode, MockUserRepo, mock_db, mock_request):
    """Test when user ID from token doesn't match any user"""
    # Setup
    user_id = str(uuid4())
    mock_jwt_decode.return_value = {"sub": user_id}
    
    mock_user_repo = MagicMock()
    mock_user_repo.get_by_id = AsyncMock(return_value=None)  # User not found
    MockUserRepo.return_value = mock_user_repo
    
    # Set token in cookie
    mock_request.cookies["access_token"] = "valid_token_but_no_user"
    
    # Execute and Assert
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user_from_cookie(request=mock_request, db=mock_db)
    
    assert excinfo.value.status_code == 404
    assert "User not found" in excinfo.value.detail
    mock_user_repo.get_by_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
@patch("server.dependencies.auth_dependencies.UserRepository")
@patch("server.dependencies.auth_dependencies.jwt.decode")
@patch("server.dependencies.auth_dependencies.JWT_SECRET", "test_secret")
@patch("server.dependencies.auth_dependencies.JWT_ALGORITHM", "HS256")
async def test_jwt_environment_variables(mock_jwt_decode, MockUserRepo, mock_db, mock_user, mock_request):
    """Test JWT environment variables are used correctly"""
    # Setup
    user_id = str(mock_user.id)
    mock_jwt_decode.return_value = {"sub": user_id}
    
    mock_user_repo = MagicMock()
    mock_user_repo.get_by_id = AsyncMock(return_value=mock_user)
    MockUserRepo.return_value = mock_user_repo
    
    # Set token in cookie
    mock_request.cookies["access_token"] = "valid_token"
    
    # Execute
    await get_current_user_from_cookie(request=mock_request, db=mock_db)
    
    # Assert
    mock_jwt_decode.assert_called_once_with("valid_token", "test_secret", algorithms=["HS256"])
