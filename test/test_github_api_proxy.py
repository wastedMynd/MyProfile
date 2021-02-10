import pytest
from src.github_api_proxy import GitUserAccountError, GitError, InternetConnectionError, has_internet_connection

# function(s) under test:
from src.github_api_proxy import get_language_and_repo_usage_count


# region test get_language_and_repo_usage_count() with invalid user_account:
# given
@pytest.mark.parametrize(
    # of
    "github_user_account, error",
    # when: they are...
    [
        pytest.param(None, GitUserAccountError),
        pytest.param('', GitUserAccountError),
        pytest.param('   ', GitUserAccountError),
        pytest.param(
            'testingInvalidUser[internet]', GitError,
            marks=pytest.mark.skipif(not has_internet_connection(), reason="Tested when theirs, Internet Connection")
        ),
        pytest.param(
            'testingInvalidUser[no-internet]', InternetConnectionError,
            marks=pytest.mark.skipif(has_internet_connection(), reason="Tested when theirs, No Internet Connection")
        ),
    ]
)
#   then:
def test_get_language_and_repo_usage_count_with_invalid_github_user_account(github_user_account, error):
    # and, then: if get_language_and_repo_usage_count(), executes; catch the raised Exception...
    with pytest.raises(error):
        get_language_and_repo_usage_count(user_account=github_user_account)
    pass
# endregion


# region test get_language_and_repo_usage_count() with valid user_account:
# given
@pytest.mark.parametrize(
    # of
    "github_user_account",
    # when: they are...
    [
        pytest.param('wastedMynd'),
    ]
)
#   then:
def test_get_language_and_repo_usage_count_with_valid_github_user_account(github_user_account):
    # and then:
    if not has_internet_connection():
        # if get_language_and_repo_usage_count(), executes; assert that the raised Exception is InternetConnectionError
        with pytest.raises(InternetConnectionError):
            get_language_and_repo_usage_count(user_account=github_user_account)
    else:
        # if get_language_and_repo_usage_count(), executes; assert content is great then 0
        assert len(get_language_and_repo_usage_count(user_account=github_user_account)) > 0
    pass
# endregion
