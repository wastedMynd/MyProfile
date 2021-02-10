from datetime import datetime
from py.xml import html
import pytest
import re


def pytest_html_report_title(report):
    report.title = "My Profile Test Report"


def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Test Case Info"))
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    cells.pop()


def pytest_html_results_table_row(report, cells):
    description_and_raised_errors = f"""
        Description: {report.function_info.get('description')}
        \nParameter(s): {report.function_info.get('params')}
        \nError(s): {report.function_info.get('raises_descriptions')}
        """
    cells.insert(2, html.td(description_and_raised_errors))
    cells.insert(1, html.td(datetime.now(), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.function_info = get_info_about(function=item.function)


def get_info_about(function) -> dict:
    """
    Parses the function's doc string and gets the; description, param(s), raises, and returns...
    :param function would like this to apply too.
    :returns dictionary containing description, param(s), raises, and returns.. and their associated values.
    """
    description = ""
    params = []
    params_descriptions = []
    raises = []
    raises_descriptions = []
    returns = ''

    if function is not None and function.__doc__ is not None:
        doc = function.__doc__.strip()
        lines = doc.split('\n')

        for line in lines:

            regex_description = r"^:"
            if not re.search(pattern=regex_description, string=line.strip()):
                description += line.strip() + "\n"
                continue

            regex_param = r"^:param\s((\w+)+)?(\s)?(.*)?"
            if match_param := re.search(pattern=regex_param, string=line.strip()):
                params.append(match_param.group(1))
                if value := match_param.group(4):
                    params_descriptions.append(value)
                    continue

            regex_raises = r"^:raises\s((\w+)+)?(\s)?(.*)?"
            if match_raises := re.search(pattern=regex_raises, string=line.strip()):
                raises.append(match_raises.group(1))
                if value := match_raises.group(4):
                    raises_descriptions.append(value)
                    continue

            regex_returns = r"^:return[s]?(\s)?(.*)?"
            if match_returns := re.search(pattern=regex_returns, string=line.strip()):
                returns = match_returns.group(2)
                continue

    payload = {
        'description': description,
        'params': params,
        'params_descriptions': params_descriptions,
        'raises': raises,
        'raises_descriptions': raises_descriptions,
        'returns': returns,
    }

    return payload
