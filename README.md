# The FnF Staff Sheet 

This is the goopy, goopy code! 

## Setup

In order to develop you need both Python and Node.js 

### Python Setup 

Create a virtual environment for the project and activate it. 

```console 
$ python3 -m venv venv-fnf 
$ . ./venv-fnf/bin/activate 
``` 

Install the development requirements: 

```console 
$ pip install -r requirements-dev.txt
``` 

### Node.js Setup 

Create a Node.js environment from the frozen lockfile:

```console 
$ npm ci 
```

## Run The Develpment Server 

Run the Django server:

```console 
$ DJANGO_DEBUG=True python3 ./manage.py runserver
```

The application will serve and the prompt won't return. If you want to do React development run the JSX translator: 

```console 
$ npx babel --watch src --out-dir static/js --presets react-app/prod 
```

Now you can edit the files in `src/`

