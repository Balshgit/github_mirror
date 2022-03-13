import sys
from threading import Thread, Semaphore

from core.argument_parser import create_parser
from core.repo_creator import RepositoryCreator
from core.utils import logger, threads_ready_statistic


def main():

    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    mirror_urls = []

    # parse urls
    if args.file:
        with open(f'{args.file}', mode='r') as file:
            lines = [repo.strip() for repo in file]
        mirror_urls.extend(lines)
    if args.urls:
        mirror_urls.extend(args.urls)

    # parse gitlab group of repositories if it exists
    group_id = args.group if args.group else None

    git_url = args.giturl  # if not provided used default value https://git.mywistr.com
    headers = {'Authorization': f'token {args.token}'}  # git user token must be provided

    repository_creator = RepositoryCreator(gitlab_url=git_url, headers=headers)

    github_token = args.githubtoken if args.githubtoken else None  # used for access to personal GitHub repositories

    threads = []
    if mirror_urls:
        for url in set(mirror_urls):  # github urls must be unique
            thread = Thread(target=repository_creator.create_repository_mirror,
                            kwargs={'github_url': url, 'group_id': group_id, 'auth_token': github_token, }
                            )

            threads.append(thread)
        with Semaphore(10):
            for thread in threads:
                thread.start()

        threads_ready_statistic(threads)  # add threads ready status to log output
    else:
        logger.info('You must provide at least one github url for mirror')
        sys.exit(1)


if __name__ == '__main__':
    main()
