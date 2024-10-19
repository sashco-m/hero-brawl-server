import click

@click.command('init-db')
def init_db_command():
    pass
    # TBD

def init_app(app):
    pass
    #app.teardown_appcontext(close_db)
    #app.cli.add_command(init_db_command)