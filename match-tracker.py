from app import create_app
from seed_cli import register_seed

app = create_app()
register_seed(app)
