import pytest
from src.instagram_api_proxy import InstagramUserAccountError, InstagramError, \
    InternetConnectionError, has_internet_connection

# function(s) under test:
from src.instagram_api_proxy import scrape_instagram_user_payload
from src.instagram_api_proxy import get_instagram_user_data


# region test scrape_instagram_user_payload() with invalid user_account:
# given
@pytest.mark.parametrize(
    # of
    "instagram_user_account, error",
    # when: they are...
    [
        pytest.param(None, InstagramUserAccountError),
        pytest.param('', InstagramUserAccountError),
        pytest.param('   ', InstagramUserAccountError),
        pytest.param(
            'testingInvalidUser[internet]', InstagramError,
            marks=pytest.mark.skipif(not has_internet_connection(), reason="Tested when theirs, Internet Connection")
        ),
        pytest.param(
            'testingInvalidUser[no-internet]', InternetConnectionError,
            marks=pytest.mark.skipif(has_internet_connection(), reason="Tested when theirs, No Internet Connection")
        ),
    ]
)
#   then:
def test_scrape_instagram_user_payload_with_invalid_instagram_user_account(instagram_user_account, error):
    # and, then: if scrape_instagram_user_payload(), executes; catch the raised Exception...
    with pytest.raises(error):
        scrape_instagram_user_payload(user_account=instagram_user_account)
    pass
# endregion


# region test scrape_instagram_user_payload() with valid user_account:
# given
@pytest.mark.parametrize(
    # of
    "instagram_user_account",
    # when: they are...
    [
        pytest.param('wastedmynds'),
    ]
)
#   then:
def test_scrape_instagram_user_payload_with_valid_instagram_user_account(instagram_user_account):
    # and then:
    if not has_internet_connection():
        # if scrape_instagram_user_payload(), executes; assert that the raised Exception is InternetConnectionError
        with pytest.raises(InternetConnectionError):
            scrape_instagram_user_payload(user_account=instagram_user_account)
    else:
        # if scrape_instagram_user_payload(), executes; assert content is greater then 0
        assert len(scrape_instagram_user_payload(user_account=instagram_user_account)) > 0
    pass
# endregion


# region test get_instagram_user_data() with invalid user_account:
# given
@pytest.mark.parametrize(
    # of
    "instagram_user_account, error",
    # when: they are...
    [
        pytest.param(None, InstagramUserAccountError),
        pytest.param('', InstagramUserAccountError),
        pytest.param('   ', InstagramUserAccountError),
        pytest.param(
            'testingInvalidUser[internet]', InstagramError,
            marks=pytest.mark.skipif(not has_internet_connection(), reason="Tested when theirs, Internet Connection")
        ),
        pytest.param(
            'testingInvalidUser[no-internet]', InternetConnectionError,
            marks=pytest.mark.skipif(has_internet_connection(), reason="Tested when theirs, No Internet Connection")
        ),
    ]
)
#   then:
def test_get_instagram_user_data_with_invalid_instagram_user_account(instagram_user_account, error):
    """
    test get instagram user_ account data; with invalid instagram user account name reference.
    :param instagram_user_account parameterized user account name
    :param error parameterized error that may occur
    """
    # and, then: if get_instagram_user_data(), executes; catch the raised Exception...
    with pytest.raises(error):
        get_instagram_user_data(user_account=instagram_user_account)
    pass
# endregion


# region test get_instagram_user_data() with valid user_account:
# given
@pytest.mark.parametrize(
    # of
    "instagram_user_account",
    # when: they are...
    [
        pytest.param('wastedmynds'),
    ]
)
#   then:
def test_get_instagram_user_data_with_valid_instagram_user_account(instagram_user_account):
    # and then:
    if not has_internet_connection():
        # if get_instagram_user_data(), executes; assert that the raised Exception is InternetConnectionError
        with pytest.raises(InternetConnectionError):
            get_instagram_user_data(user_account=instagram_user_account)
    else:
        # if get_instagram_user_data(), executes; assert content is greater then 0
        assert len(get_instagram_user_data(user_account=instagram_user_account)) > 0
    pass
# endregion
