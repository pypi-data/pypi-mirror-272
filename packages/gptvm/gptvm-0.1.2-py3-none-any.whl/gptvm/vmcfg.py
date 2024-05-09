# vm_env define the virtual execution environment for the program

_DEFAULT_SETTINGS = {
    "server_url": "localhost:5000",
}

class VMCfg(object):
    def __init__(
        self,
        name: str = None,
        model_id: str = None,
        model_dir: str = None,
        pips: list = None,
        num_gpus: int = 1,
        num_cpus: int = 4,
    ):
        self.settings = _DEFAULT_SETTINGS
        self.name = name
        self.model_id = model_id
        if model_dir is None:
            self.model_dir = "/model"
        else:
            self.model_dir = model_dir
        self.pips = pips
        self.num_gpus = num_gpus
        self.num_cpus = num_cpus
        self.setup()

    def __str__(self):
        return f"VMCfg(name={self.name}, model_id={self.model_id}, model_dir={self.model_dir}, pips={self.pips}, num_gpus={self.num_gpus}, num_cpus={self.num_cpus})"

    def __repr__(self):
        return self.__str__()

    def get(self, key, use_env=True):
        # TODO: support use_env
        return self.settings.get(key)

    def to_dict(self):
        return {key: self.settings.get(key) for key in self.settings.keys()}

    # function to setup the runtime environment
    def setup(self):
        pass
