# Github mirror creator

Use python version > 3.8

## Build

```bash
pyinstaller -F github_mirror.py
```


## Argumetns:

- -h, --help -> ```Show help message and exit```


- -g GROUP, --group GROUP -> ```Add repository to GROUP name. It also named Organisation```


- -u URL [URL ...], --urls URL [URL ...] 
```Provide url or urls to mirror with it in format: https://github.com/s3rius/FastAPI-template.git You can provide multiple urls separated by space. Names will generate automatically from links```


- -f FILE, --file FILE
```Add file with urls. Each url on new line. Can be combined with --url option. Names will generate automatically from links```

- -t TOKEN, --token TOKEN
```Access token to gitea API. More information:``` [gitea docs](https://docs.gitea.io/en-us/api-usage/#authentication)

- T GITHUBTOKEN, --githubtoken GITHUBTOKEN 
- ```Please provide github token to get access to private repositories``` [github tokens](https://github.com/settings/tokens)


- -l GITURL, --giturl GITURL ```Provide git url. Default link``` https://git.mywistr.ru


## Usage 

```python
python3 github_mirror.py [-h] [-g GROUP] (-u URLS [URLS ...] | -f FILE) -t TOKEN
```


## Examples:

    python3 github_mirror.py -u "https://github.com/s3rius/FastAPI-template.git" -g "GitHub" -t "gtb-QwertY1245kde"
    
    python3 github_mirror.py -u "https://github.com/s3rius/FastAPI-template.git" "https://github.com/sqlalchemy/sqlalchemy.git" -t "gtb-QwertY1245kde"
    
    python3 github_mirror.py -f github_mirrors.txt -g "Public" -t "gtb-QwertY1245kde"
    
    python3 github_mirror.py -f github_mirrors.txt -u "https://github.com/s3rius/FastAPI-template.git" -t "gtb-QwertY125kde"
    
    python3 github_mirror.py --giturl "https://gitea.company.ru" -t "gtb-QwertY1245kde" -u "https://github.com/Balshgit/sonar-scanner.git" -g "Personal" -T "ghb-Qwerty321ldf"
