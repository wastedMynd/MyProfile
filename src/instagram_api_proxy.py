import os
import requests
from bs4 import BeautifulSoup
from json import loads

instagram_base_api_url = 'https://instagram.com/'


def has_internet_connection() -> bool:
    try:
        with requests.get(url=instagram_base_api_url, timeout=5):
            pass
        return True
    except requests.exceptions.ConnectionError:
        return False


class InstagramError(ValueError):
    pass


class InstagramUserAccountError(InstagramError):
    pass


class InternetConnectionError(Exception):
    pass



def scrape_instagram_user_payload(user_account: str) -> dict:
    """
    Connects to user_account Instagram account, and scrapes for data payload;
     returns an unfriendly dictionary, payload format.
    :param user_account Instagram User Account name reference
    :raises InstagramUserAccountError when either provided with a None, Empty, or Non-existing user_account.
    :raises InstagramError internal GitHub Error as a response to request.
    :raises InternetConnectionError when not connected to the internet
    :returns dictionary containing instagram user_account payload.
    """

    # region guard condition for user_account
    if user_account is None or len(user_account.strip()) == 0:
        raise InstagramUserAccountError(
            user_account,
            'Provided either a None or Empty, Instagram User Account name reference!'
        )

    if not has_internet_connection():
        raise InternetConnectionError("[Error] No Internet Connection!")
    # endregion guard condition for github_user_account

    # compose request url
    user_account_request_url = os.path.join(instagram_base_api_url, user_account)

    with requests.get(url=user_account_request_url) as response:
        if not (response.status_code in range(200, 300)):
            if response.status_code == 404:
                raise InstagramUserAccountError(
                    user_account,
                    "Provided either a Non-existing, Instagram User Account name reference!"
                    f"State: {response.status_code} , {response.content}"
                )
            else:
                raise InstagramError(
                    user_account,
                    f'Response, for request is... not found!'
                    f"State: {response.status_code} , {response.content}"
                )

        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')

        data_script = scripts[4]
        content = data_script.contents[0]
        data_object = content[content.find('{"config"'): -1]
        data = loads(data_object)
        payload = data['entry_data']['ProfilePage'][0]['graphql']['user']

    if payload is None:
        raise InstagramError(user_account, 'payload is None')

    return payload


def get_instagram_user_data(user_account: str, log: bool = False) -> dict:
    """
    Gets unfriendly user_account payload, parses it into a user friendly dictionary format.
    :param: user_account Instagram User Account name reference
    :param: log print result
    :raises: InstagramUserAccountError when either provided with a None, Empty, or Non-existing user_account.
    :raises: InstagramError internal GitHub Error as a response to request.
    :raises: InternetConnectionError when not connected to the internet
    :returns: dictionary containing instagram user_account data.
    """

    payload = scrape_instagram_user_payload(user_account)

    data = {
        'biography': payload['biography'],
        'external_url': payload['external_url'],
        'followers_count': payload['edge_followed_by']['count'],
        'following_count': payload['edge_follow']['count'],
        'full_name': payload['full_name'],
        'is_private': payload['is_private'],
        'username': payload['username'],
        'total_posts': payload['edge_owner_to_timeline_media']['count'],
    }

    print(data if log else '\r')

    return data


if __name__ == '__main__':
    get_instagram_user_data(user_account='wastedmynds', log=True)
