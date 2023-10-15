import random
from typing import Union
from http import HTTPStatus

import requests
from requests import Response

from core.utils import logger


class RepositoryCreator:

    def __init__(self, git_url: str, headers: dict) -> None:
        self.git_url = git_url
        self.headers = headers

    def create_repository_mirror(self, github_url: str, group_id: str, auth_token: str) -> None:
        """
        Base action for one thread. Creates repository, add mirror url and triggers pull at te end

        :param github_url: GitGub url which will be mirrored
        :param group_id: Gitlab group id which contains created repository
        :param auth_token: GitGub token to access private repositories
        """

        self.__create_new_project(github_url, group_id, auth_token)

    def __git_request(self, method: str, url: str, data: dict = None) -> Union[Response, None]:
        """
        Create request to gitlab

        :param method: Request method can be changed
        :param url: Url to request
        :param data: Provide request data
        :return: Response object on None
        """

        try:
            request = requests.request(method, url, headers=self.headers, json=data, verify=False)
            return request
        except Exception as err:
            logger.error(f'Connection not established. \n{err}')

    def __create_new_project(self, url: str, group_name: str = None, auth_token: str = None) -> None:
        """
        Create new project in gitlab with name based on provided url

        :param url: GitHub url to mirror with:
        :param group_name: namespace in gitlab to combine repos
        :param auth_token: GitHub token to access private repositories
        :return: repo_id as string or None if any error
        """

        # name of repository will generate automatically from link
        name = url.split('/')[-1].replace('.git', '')
        update_time = random.randint(120, 580)  # prevent update all repos at the same time
        git_data = {'repo_name': name, "wiki": True, "private": False, 'mirror_interval': f'{update_time}h0m0s',
                    "mirror": True, "lfs": True, "clone_addr": url}
        if group_name:
            git_data['repo_owner'] = group_name
        if auth_token:
            git_data['auth_token'] = auth_token

        request = self.__git_request('POST', f'{self.git_url}/api/v1/repos/migrate', git_data)
        try:
            if request.status_code == HTTPStatus.CREATED:
                response = request.json()
                name_with_namespace = response.get('full_name', None)
                if name_with_namespace:
                    logger.info(f'Repository {name_with_namespace} has been created')
                else:
                    logger.info(f'Repository {response["name"]} has been created')
            else:
                logger.error(f'Cant create {name} project. Status code: {request.status_code}. Reason: {request.text}')
        except AttributeError:
            pass
