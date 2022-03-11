from app import create_app
from seed_cli import register_seed
from flask_security import (
    Security,
    SQLAlchemyUserDatastore,
    auth_required,
    current_user,
    hash_password,
    permissions_accepted,
    permissions_required,
    roles_accepted,
)

app = create_app()
register_seed(app)
