import pytest

from data import Data
from helpers import UserCreationHelper, UserDeletionHelper


@pytest.fixture()
def get_the_user_data():
    data = {
        "email": Data.get_random_email(),
        "password": Data.get_random_password(),
        "name": Data.get_random_name()
    }
    return data


@pytest.fixture()
def create_user_get_data_and_delete_user(get_the_user_data):
    response = UserCreationHelper.user_creation_request(get_the_user_data)
    yield response, get_the_user_data
    UserDeletionHelper.user_deletion_requests(response.json()['accessToken'])
