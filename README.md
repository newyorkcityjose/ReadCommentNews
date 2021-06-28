# Read Comment News

This is for people who likes to read the news and leave their thoughts. The user would read a news article then bookmark it. After the user would leave their comments and other users can leave their comment, creating a form. Any user can see what you bookmark and comment on, and if you like the user thoughts and news interest then the user can follow them. Also, the user can message anyone he or she is following. 
App runs Python, Flask, PostgreSQL, javascript, jQuery

# Database 

Create local setting example looking for the name local_settings_example.txt

# API Key

Create an account on [newsapi.org](https://newsapi.org/) to get API key.
Example look at local_settings_example.txt


# Installation

## Installing virtualenv

Windows

```
py -m pip install --user virtualenv
```

Mac OS Linux

```
python3 -m pip install --user virtualenv

```
## Creating a virtual environment

Windows
```
py -m venv env
```
Mac OS Linux
```
python3 -m venv env
```

## Activating a virtual environment

Windows
```
.\env\Scripts\activate
```

or cd into env directory then
```
scripts\activate
```
Mac OS Linux

```
source env/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip install -r requirements.txt
```

Create and apply changes into the databse

```
flask db init
flask db migrate -m "First migrate"
flask db upgrade
```

Run flask app

```
flask run
```
# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

