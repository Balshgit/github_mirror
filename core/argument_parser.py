from argparse import ArgumentParser

GIT_URL = 'https://git.mywistr.ru'

USAGE = '''github_mirror [-h] [-g GROUP] (-u URLS [URLS ...] | -f FILE) -t TOKEN [-T GitHubTOKEN]
--------------------------------------------------

python3 github_mirror.py -u "https://github.com/s3rius/FastAPI-template.git" -g "GitHub" -t "gtb-QwertY1245kde"

python3 github_mirror.py -u "https://github.com/s3rius/FastAPI-template.git" "https://github.com/sqlalchemy/sqlalchemy.git" -t "gtb-QwertY1245kde"

python3 github_mirror.py -f github_mirrors.txt -g "Public" -t "gtb-QwertY1245kde"

python3 github_mirror.py -f github_mirrors.txt -u "https://github.com/s3rius/FastAPI-template.git" -t "gtb-QwertY125kde"

python3 github_mirror.py --giturl "https://gitea.company.ru" -t "gtb-QwertY1245kde" -u "https://github.com/Balshgit/sonar-scanner.git" -g "Personal" -T "ghb-Qwerty321ldf"


--------------------------------------------------
'''


def create_parser() -> ArgumentParser:
    """
    Create argparse parser

    :return: command parser
    """
    parser = ArgumentParser(
        prog='github_mirror',
        description='''Script to add mirror repo into gitea''',
        epilog='''the developer is not responsible for the operation of the script :)''',
        add_help=True,
        usage=USAGE
    )

    parser.add_argument('-g', '--group', required=False, type=str,
                        help='Add repository to GROUP name. It also named Organisation')

    parser.add_argument('-u', '--urls', nargs='+',
                        help='Provide url or urls to mirror with it in format: '
                             'https://github.com/s3rius/FastAPI-template.git. You can provide multiple urls '
                             'separated by space. Names will generate automatically from links')

    parser.add_argument('-f', '--file', help='Add file with urls. Each url on new line. Can be combined with '
                                             '--url option. Names will generate automatically from links')

    parser.add_argument('-t', '--token', required=True,
                        help='Access token to gitea API. More information: https://docs.gitea.io/en-us/api-usage/'
                             '#authentication')

    parser.add_argument('-T', '--githubtoken', required=False, help='Please provide github token to get access '
                                                                    'to private repositories')

    parser.add_argument('-l', '--giturl', required=False, default=GIT_URL,
                        help=f'Provide git url where you want store your repositories. Default link {GIT_URL}')

    return parser
