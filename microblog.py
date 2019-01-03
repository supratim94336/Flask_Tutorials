from app import create_app, db, cli
from app.models import User, Post


app = create_app()
cli.register(app)


# to pre-import stuff you need every time in $ flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}