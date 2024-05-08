from typing import Any
from urllib import request

headers = {'User-Agent': 'mkrp'}


def get_template_list() -> list[str]:
    """Returns a list of all available templates from gitignore.io.

    Returns:
        list[str]: A list of all available templates from gitignore.io.
    """
    response = (
        request.urlopen(
            request.Request(
                'https://www.gitignore.io/api/list', headers=headers
            )
        )
        .read()
        .decode('utf-8')
    )

    template_list = []
    for line in map(str, response.split('\n')):
        template_list.extend(line.split(','))

    return template_list


# stack is a list of strings of names of tech to include
# Ex. ['sass', 'node', 'macos']
def get_gitignore(stack: list[str]) -> Any:
    """Generates a .gitignore file based on the stack of technologies.

    Args:
        stack (list[str]): A list of strings of names of tech to include.

    Returns:
        Any: The generated .gitignore file.
    """
    template_list = get_template_list()

    for tech in stack:
        if tech.lower() not in template_list:
            raise ValueError(tech)  # Reports iffy item in the list

    comma_delimited = ','.join(stack)
    response = (
        request.urlopen(
            request.Request(
                'https://www.gitignore.io/api/' + comma_delimited,
                headers=headers,
            )
        )
        .read()
        .decode('utf-8')
    )

    return response
