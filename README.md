# n2diskui
[user-guide](https://shop.firstlight.net/wp-content/uploads/2014/05/n2disk-UsersGuide.pdf)

python 3.10

sudo apt install python3-poetry 

# to get started with development

add these lines to your .bashrc 

export PATH="$HOME/.poetry/bin:$PATH" 

FOR ROCKY LINUX
export PATH="/root/.local/bin:$PATH"

export FLASK_APP=run.py
export FLASK_ENV="development"

restart terminal 

curl -sSL https://install.python-poetry.org | python3 -

> poetry install 

to work on it 

> poetry shell


sudo apt update 
sudo apt install postgresql postgresql-contrib 

to run the app, in project home directory

> python run.py

example output

```
(dev-n2disk-ui-515YVC9v-py3.10) jstreet@f150:~/work/n2diskui$ python run.py
 * Serving Flask app 'n2diskui'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 476-421-282
```
# For VSCODE
Sonar Lint extension for code Quality

in your settings.json add these lines
```
"python.languageServer": "Pylance",
"python.autoComplete.extraPaths": [
    "./n2diskui"
]
```

Example file structure for reference
```
my_flask_app/
│
├── n2diskui/
│   ├── __init__.py
│   ├── routes.py
│   ├── api.py
│   ├── models.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   └── static/
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── scripts.js
│       └── images/
│
├── config.py
├── run.py
├── wsgi.py
├── requirements.txt
└── tests/
    ├── __init__.py
    ├── test_routes.py
    ├── test_models.py
    └── ...

```

running n2disk 

sudo n2disk -i enp3s0 -o /home/storage -b 1024 -p 512 --disk-limit 50% -I -A /home/storage

- make sure there is write access all the way to storage.
- also dont delete the files and try and move them, they symlink.
- best to run this and then get the files from /home/storage, or wherever you saved it.
