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

    gitlab_url = args.gitlab  # if not provided used default value https://git.do.x5.ru
    headers = {'PRIVATE-TOKEN': args.token}  # gitlab users token must be provided

    repository_creator = RepositoryCreator(gitlab_url=gitlab_url, headers=headers)

    threads = []
    if mirror_urls:
        for url in set(mirror_urls):  # github urls must be unique
            thread = Thread(target=repository_creator.create_repository_mirror,
                            kwargs={'url': url, 'group_id': group_id, })
            threads.append(thread)

        for thread in threads:
            with Semaphore(50):
                thread.start()

        threads_ready_statistic(threads)  # add threads ready status to log output

    else:
        logger.info('You must provide urls to mirror')
        sys.exit(1)


if __name__ == '__main__':
    main()
