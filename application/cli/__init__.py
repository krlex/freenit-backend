import click
from flask.cli import AppGroup
from peewee_migrate import Router


def register_migration(app):
    migration = AppGroup('migration', short_help='Migration operations')
    router = Router(app.db.database)

    @migration.command()
    def list():
        for migration in router.done:
            print(migration)

    @migration.command()
    @click.argument('name')
    def create(name):
        router.create(name, 'application.models')

    @migration.command()
    def run():
        router.run()

    app.cli.add_command(migration)


def register_admin(app):
    admin_group = AppGroup('admin', short_help='Manage admin users')

    @admin_group.command()
    def create():
        from ..models.auth import User
        admin, created = User.get_or_create(
            email='admin@example.com',
            password='Sekrit',
        )
        if created:
            admin.admin = True
            admin.active = True
            admin.save()

    app.cli.add_command(admin_group)


def register(app):
    register_migration(app)
    register_admin(app)
