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

* Create a virtual environment if one does not already exists (need to sync up Python versions).
* `python3.7 -m venv <name>(lir3.7)`
* `pip install -r requirements.txt`
* `flask db upgrade` make sure that any new migrations are caught
* `sudo supervisorctl start matchtracker` 

# Accessing Database on server 

* If you forget the password (which I know you will)
* `sudo -u postgres`
* `psql`
* `postgres=# ALTER USER postgres PASSWORD 'mynewpassword';`

* `psql -d match-tracker -h localhost -U match-tracker-flask`

