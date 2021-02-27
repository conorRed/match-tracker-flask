# Deployment

(venv) $ git pull # download the new version
(venv) $ sudo supervisorctl stop microblog # stop the current server
(venv) $ flask db upgrade # upgrade the database
(venv) $ flask translate compile # upgrade the translations
(venv) $ sudo supervisorctl start microblog
