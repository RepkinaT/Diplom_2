import pytest

from helpers import UserCreationHelper, UserDeletionHelper, Data


@pytest.fixture()
def create_user_get_data_and_delete_user():
    get_the_user_data = Data.get_the_user_data()
    response = UserCreationHelper.user_creation_request(get_the_user_data)
    yield response, get_the_user_data
    UserDeletionHelper.user_deletion_requests(response.json()['accessToken'])
