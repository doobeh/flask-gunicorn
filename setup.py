from setuptools import setup

setup(
    name='Flask-Gunicorn',
    version=0.1,
    license='MIT',
    url='https://github.com/doobeh/flask-gunicorn',
    entry_points='''
        [flask.commands]
        run=flask_gunicorn:cli
    ''',
    author='Anthony Plunkett',
    py_modules=['flask_gunicorn'],
    requires=[
        'Flask',
        'gunicorn',
    ]
)

