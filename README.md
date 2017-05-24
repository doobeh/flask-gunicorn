# Flask-Gunicorn

Flask-Gunicorn lets you simply run your Flask Application using the 
gunicorn application server easily from the command line.

Unfortunately Gunicorn doesn't work on Windows machines, so you may
want to look into alternative solutions for serving your application. 

## Installation

Install the extension with pip:

```sh
$ pip install flask-gunicorn
```

## Usage

Once installed, Flask-Gunicorn automatically overides the `run` 
command in the `flask` command line tool.

To use, simply let `flask` know where your application is by setting 
an environment variable:

```sh
export FLASK_APP=myapp.py
```

Then run the server:

```sh
flask run
```

By default Flask-Gunicorn will make a sensible guess at how many 
workers to allocate to the application server based the number of
CPU cores on your machine, but this can be specified using the 
`--workers x` argument or `WORKERS` environment variable.


the `flask run` command also takes serveral optional arguments to 
help you customize your gunicorn server.

| Argument          | Description|
| -------------     | ------------- |
| `--workers`       | How many workers should Gunicorn spawn  |
| `--worker_class`  | Should Gunicorn use a specific class of worker? E.g. gevent |
| `--debugger`      | Run the server with the interactive debugger |
| `--no-debugger`   | Turn off the debugger mode |
| `--host`          | What address should the server bind to (e.g. `127.0.0.1`)
| `--port`          | What port should be used (e.g. `5000`) |
| `--reload`        | Turn on the reloader (gunicorn will notice changes to code and restart if noticed) This is on by default in debug mode.|
| `--noreload`      | Turn off the reloader |


## Contributing

Contributions will be gleefully received! Check out the current issues, or feel
free to crate new issues for any problems you've encountered and we'll push this
little project forwards.

Thanks to [Flask-Common](https://github.com/kennethreitz/flask-common) and the 
[Gunicorn Docs on Custom Applications](http://docs.gunicorn.org/en/stable/custom.html)
for hints on getting this all working.


