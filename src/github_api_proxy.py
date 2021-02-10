import os
import requests

github_base_api_url = 'https://api.github.com/'


def has_internet_connection() -> bool:
    try:
        with requests.get(url=github_base_api_url, timeout=5):
            pass
        return True
    except requests.exceptions.ConnectionError:
        return False


class GitError(ValueError):
    pass


class GitUserAccountError(GitError):
    pass


class InternetConnectionError(Exception):
    pass


def get_language_and_repo_usage_count(user_account: str, log: bool = False) -> list:
    """
    Gets the Language and usage count per repository.
    :param user_account Github User Account name reference
    :param log print result
    :raises GitUserAccountError when either provided with a None, Empty, or Non-existing user_account.
    :raises GitError internal GitHub Error as a response to request.
    :raises InternetConnectionError when not connected to the internet
    :returns a list containing dictionaries -> { 'language': '', 'count': 0 }
    """
    # region guard condition for user_account
    if user_account is None or len(user_account.strip()) == 0:
        raise GitUserAccountError(user_account, 'Provided either a None or Empty, Github User Account name reference!')

    if not has_internet_connection():
        raise InternetConnectionError("[Error] No Internet Connection!")
    # endregion guard condition for github_user_account

    # region when: composing a search query
    search_query = f'search/repositories?q=user:{user_account}'
    url_request = os.path.join(github_base_api_url, search_query)
    #  endregion

    with requests.get(url=url_request) as response:
        if not (response.status_code in range(200, 300)):
            if response.status_code == 404:
                raise GitUserAccountError(
                    user_account,
                    "Provided either a Non-existing, Github User Account name reference!"
                    f"State: {response.status_code} , {response.content}"
                )
            else:
                raise GitError(
                    user_account,
                    f'Response, for request is... not found!'
                    f"State: {response.status_code} , {response.content}"
                )

        json_response = response.json()

    stats_holder = []

    def index_of(lang):
        for x, reg_lang in enumerate(stats_holder):
            if lang == reg_lang.get('language'):
                return x
        else:
            return -1

    for item in json_response.get("items"):

        language = item.get('language')

        if not (index_of(language) > -1):
            stats_holder.append({
                'language': language,
                "count": 1
            })
        else:
            stats_holder[index] = {
                'language': language,
                "count": stats_holder[(index := index_of(language))].get("count") + 1
            }

    print(f"get_language_and_repo_usage_count: {stats_holder}" if log else "\r")

    return stats_holder

