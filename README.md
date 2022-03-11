# Set up

* Install Python 3 and pip
* Setup up the virtual environment in the code directory with `python3 -m venv lir`
* Source the new virtual environment with `source lir/bin/activate`
* Run `pip install -r requirements.txt`
 
# Development

* To run the development server `FLASK_ENV=development flask run`
 
# Testing

* `pip install pytest`
* `python -m pytest`

# Database/Migrations

* To run a migration and make a schema change run `flask db migrate -m <message-detailing-changes>`
* Then to push those to the database run `flask db upgrade`

# Deploying

* `git pull` inside the directory on the server
* `sudo supervisorctl stop matchtracker` 
* `flask db upgrade` make sure that any new migrations are caught
* `sudo supervisorctl start matchtracker` 

