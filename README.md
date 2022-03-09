# Github mirror creator

Use python version > 3.8


## Argumetns:

- -h, --help -> ```Show help message and exit```


- -g GROUP, --group GROUP -> ```Add GROUP id it can be found under group name. Id must be integer```


- -u URL [URL ...], --urls URL [URL ...] 
```Provide url or urls to mirror with it in format: https://github.com/s3rius/FastAPI-template.git You can provide multiple urls separated by space. Names will generate automatically from links```


- -f FILE, --file FILE
```Add file with urls. Each url on new line. Can be combined with --url option. Names will generate automatically from links```

- -t TOKEN, --token TOKEN
```Access token to gitlab API. More information:``` [gitlab docs](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#create-a-personal-access-token)

- -l GITLAB, --gitlab GITLAB ```Provide gitlab url. Default link``` https://git.do.x5.ru


## Usage 

```python
python3 github_mirror.py [-h] [-g GROUP] (-u URLS [URLS ...] | -f FILE) -t TOKEN
```


## Examples:

    python3 github_mirror -u "https://github.com/s3rius/FastAPI-template.git" -g 2059
    
    python3 github_mirror -u "https://github.com/s3rius/FastAPI-template.git" "https://github.com/sqlalchemy/sqlalchemy.git"
    
    python3 github_mirror -f github_mirrors.txt -g 59563
    
    python3 github_mirror -f github_mirrors.txt -u "https://github.com/s3rius/FastAPI-template.git"
    
    python3 gitlab_mirror.py --gitlab "https://gitlab.company.ru" -t "git-QwertY1245kde" -g 2059