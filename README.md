# Read Comment News

This is for people who likes to read the news and leave their thoughts.
App runs Python, Flask, PostgreSQL, javascript, jQuery

# Database 

Create local setting example looking for the name local_settings_example.txt

# API Key

Create an account on newsapi.org for api example look at local_settings_example.txt


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
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

