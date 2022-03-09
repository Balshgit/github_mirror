from typing import Union

import requests
from requests import Response

from core.utils import logger


class RepositoryCreator:

    def __init__(self, gitlab_url: str, headers: dict):
        self.gitlab_url = gitlab_url
        self.headers = headers
        self.HTTP_201_CREATED = 201
        self.HTTP_200_OK = 200

    def __gitlab_request(self, method: str, url: str, data: dict = None) -> Union[Response, None]:
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
            logger.error(f'Connection not established. Check vpn is connected! \n{err}')

    def __create_new_project(self, url: str, group_id: int = None) -> Union[str, None]:
        """
        Create new project in gitlab with name based on provided url

        :param url: github url to mirror with:
        :param group_id: namespace in gitlab to combine repos
        :return: repo_id as string or None if any error
        """

        # name of repository will generate automatically from link
        name = url.split('/')[-1].replace('.git', '')
        git_data = {'name': name}
        if group_id:
            git_data['namespace_id'] = group_id

        request = self.__gitlab_request('POST', f'{self.gitlab_url}/api/v4/projects', git_data)
        try:
            if request.status_code == self.HTTP_201_CREATED:
                repo_data = request.json()
                name_with_namespace = repo_data.get('name_with_namespace', None)
                if name_with_namespace:
                    logger.info(f'Repository {name_with_namespace} has been created')
                else:
                    logger.info(f'Repository {repo_data["name"]} has been created')
                return repo_data['id']
            else:
                logger.error(f'Cant create new project. Status code: {request.status_code}. Reason: {request.text}')
        except AttributeError:
            pass

    def __add_pull_mirror(self, url: str, repo_id: str) -> Union[str, None]:
        """
        Add pull mirror to Settings -> Repository -> Mirroring repositories

        :param url: github url to mirror with
        :param repo_id: id of repository which will be updated
        :return: github url which will be mirrored
        """

        if repo_id:
            git_data = {"mirror": True, "import_url": url}
            request = self.__gitlab_request('PUT', f'{self.gitlab_url}/api/v4/projects/{repo_id}', git_data)
            if request and request.status_code == self.HTTP_200_OK:
                return url
            elif request.status_code != self.HTTP_200_OK:
                logger.error(f'Cant add mirror url to project. Status code: {request.status_code}. '
                             f'Reason: {request.text}')

    def __pull_github_repo(self, url: str, repo_id: str):
        """
        Initiate pull request for gitlab repository

        :param url: github url to mirror with
        :param repo_id: id of repository which will be updated
        """

        if repo_id:
            request = self.__gitlab_request('POST', f'{self.gitlab_url}/api/v4/projects/{repo_id}/mirror/pull')
            if request and request.status_code == self.HTTP_200_OK:
                logger.info(f'Repository: {url} has been pulled')
            elif request.status_code != self.HTTP_200_OK:
                logger.error(f'Error pull repository. Status code: {request.status_code}. Reason: {request.text}')

    def create_repository_mirror(self, github_url: str, group_id: int):
        """
        Base action for one thread. Creates repository, add mirror url and triggers pull at te end

        :param github_url: Github url which will be mirrored
        :param group_id: Gitlab group id which contains created repository
        """
        repo_id = self.__create_new_project(github_url, group_id)
        url = self.__add_pull_mirror(github_url, repo_id)
        if url:
            self.__pull_github_repo(url, repo_id)
