# Api Exchange
***

Nota: use of limiter and authorizer are for demonstration purposes only, use in production is not recommended 

## Run Locally
To run the commands you must be on the root of the repository


### Local execution
NOTE: You must be having installed python3.7 or higher in your local machine
### LINUX:
``python -m venv venv``

``./venv/bin/activate``

``pip install --no-cache-dir -r requirements.txt``

``uvicorn app.app:app --reload --port [port number]``
### WINDOWS
``python -m venv venv``

``.\venv\Scripts\activate``

``pip install --no-cache-dir -r requirements.txt``

``uvicorn app.app:app --reload --port [port number]``

this will start the server to the default host: localhost:[port number]

you can see the swagger documentations in: localhost:[port number]/docs

### Local execution on docker

To run on docker you must run the next lines:

``docker build -t [image name] .``

``docker run -d --name [container name] -p 80:80 [image name]``


NOTE: if you don´t specify the port number docker won't expose the image to a host (in this case locally)


## Try the api

[token]: you can find the token in ./app/properties file

``
curl -X 'GET' 
  'http://127.0.0.1:[port number]/exchange' 
  -H 'accept: application/json' 
  -H 'Authorization: Bearer [token]'
``

## For unittest
To run the unittest and coverage run the next lines:

``coverage run -m unittest discover``

`` coverage html -d coverage_html``

after run the las command you can find a coverage_html dir open the index.html and filter by **app/** for show only the app coverage 
