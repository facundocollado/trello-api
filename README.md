## Requirements:
* Ubuntu 20.04
* Python 3.9
*  [Docker](https://docs.docker.com/)  
* python3-pip (`sudo apt install python3-pip`)
* Pipenv (`sudo apt install pipenv`)
* Personal [Api Key and Token] (https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#actions)
    * Replace the keys in credentials.txt with your personal ones

## Virtual environment setup
Navigate to the project folder and type:
* (Optional, removes any previously created environment)`rm -rf venv`
* Create a new environment using python 3.9 `pipenv --python 3.9`
* Navigate to the newly created virtual environment `source $(pipenv --venv)/bin/activate`
* (Optional, leave the virtual environment) `exit`

## Install all pipenv libraries
`pipenv install`

### Freeze requirement libraries (optional, only after upgrades, if needed)
`pip3 freeze | grep Flask >> requirements.txt`

### Start up the docker environment 
(optional, set dev environment) export FLASK_ENV=development
`python3 -m flask run`

Server will be running at [Localhost](http://localhost:5000)

### Once the server is running, curl request can be made

#### Setting up local variables:
This will populate the credentials.txt file with the ids from the labels (issue, bug, task) required for the newly created cards.
Simply call `curl http://localhost:5000/set-up`, that's all.


* From console, using curl command: `curl -H '<header>' --data '<query parameters>' http://localhost:5000`
    * Examples:
        * `curl -H 'Content-Type: application/json' --data '{"type": "issue", "title": "send message", "description": "Let pilots send messages to Central"}' http://localhost:5000`
        * `curl -H 'Content-Type: application/json' --data '{"type": "bug", "title": "bug", "description": "Cockpit is not pressuring correctly"}' -X POST  http://localhost:5000`
* Using your browser
* curl through Postman


### Upon execution the program will:
* Search for your last board in you boards list
* Obtain the first list from said board, by default, is the "To do" list
* Create the default labels ("issue", "bug", "task")
* Add a few cards for those labels

That's it, enjoy!