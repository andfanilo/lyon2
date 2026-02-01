import datetime

def on_config(config):
    year = datetime.date.today().year
    config['copyright'] = f"Copyright &copy; {year} Fanilo ANDRIANASOLO"
    return config
