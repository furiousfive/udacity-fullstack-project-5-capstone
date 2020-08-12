from flask.cli import FlaskGroup

from src.castingagency import create_app, db
from flask_migrate import Migrate, MigrateCommand

app = create_app()
cli = FlaskGroup(create_app=create_app)
migrate = Migrate(app, db)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()