from argparse import ArgumentParser

GITLAB_URL = 'https://git.do.x5.ru'

USAGE = '''github_mirror [-h] [-g GROUP] (-u URLS [URLS ...] | -f FILE) -t TOKEN
--------------------------------------------------

python3 github_mirror -u "https://github.com/s3rius/FastAPI-template.git" -g 2059 -t "git-QwertY1245kde"

python3 github_mirror -u "https://github.com/s3rius/FastAPI-template.git" "https://github.com/sqlalchemy/sqlalchemy.git" -t "git-QwertY1245kde"

python3 github_mirror -f github_mirrors.txt -g 59563 -t "git-QwertY1245kde"

python3 github_mirror -f github_mirrors.txt -u "https://github.com/s3rius/FastAPI-template.git" -t "git-QwertY1245kde"

python3 github_mirror.py --gitlab "https://gitlab.company.ru" -t "git-QwertY1245kde" -g 2059


--------------------------------------------------
'''


def create_parser() -> ArgumentParser:
    """
    Create argparse parser

    :return: command parser
    """
    parser = ArgumentParser(
        prog='github_mirror',
        description='''Script to add mirror repo into gitlab''',
        epilog='''the developer is not responsible for the operation of the script :)''',
        add_help=True,
        usage=USAGE
    )

    parser.add_argument('-g', '--group', required=False, type=int,
                        help='Add group id it can be found under group name. Id must be integer')

    parser.add_argument('-u', '--urls', nargs='+',
                        help='Provide url or urls to mirror with it in format: '
                             'https://github.com/s3rius/FastAPI-template.git. You can provide multiple urls '
                             'separated by space. Names will generate automatically from links')

    parser.add_argument('-f', '--file', help='Add file with urls. Each url on new line. Can be combined with '
                                             '--url option. Names will generate automatically from links')

    parser.add_argument('-t', '--token', required=True,
                        help='Access token to gitlab API. More information: https://docs.gitlab.com/ee/user/profile/'
                             'personal_access_tokens.html#create-a-personal-access-token')

    parser.add_argument('-l', '--gitlab', required=False, default=GITLAB_URL,
                        help=f'Provide gitlab url. Default link {GITLAB_URL}')

    return parser
