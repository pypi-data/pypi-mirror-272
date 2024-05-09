import configparser
import os

config_file = ".gptvm.conf"

default_configs = {
    'user': 'none',
    'token': 'none',
    'space_id': 0,
    'group_id': 0,
}

server_configs = {
    'host': 'api.gptvm.ai',
    'port': 80,
}

class Config(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        self.file = os.path.expanduser(f'~/{config_file}')
        self.load()
    
    def load(self):
        self['default'] = default_configs
        self['server'] = server_configs
        self.read(self.file)

    def save(self):
        with open(self.file, 'w') as f:
            self.write(f)

    def remove(self):
        if os.path.exists(self.file):
            os.remove(self.file)

if __name__ == "__main__":
    cfg = Config()
    cfg['default']['user'] = 'user'
    cfg.save()
