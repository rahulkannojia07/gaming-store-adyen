# Gaming Store with Adyen Integration

A demo shopping web application that uses Adyen Web dropin payment integration to complete a fast, reliable and secure payments.

## Requirements

- Python 3.8 or greater
- Frameworks:
  - Django v3.2
- SQLite3 Db (included with Django)

## Installation

The first thing to do is to clone the repository

Then, create a virtual environment to install dependencies in and activate it:

```sh
$ python -m venv env
$ env/Scripts/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Once `pip` has finished downloading the dependencies, run server to initiate application:

```sh
(env)$ python manage.py runserver 5000
```
And navigate to `http://127.0.0.1:5000/home/`.

## Usage

Visit http://127.0.0.1:5000/home/ and follow the workflow!

## License

MIT
