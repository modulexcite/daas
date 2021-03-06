# Needed for 'eval':
from .decompiler import *
from .csharp_decompiler import CSharpDecompiler


class DecompilerCreator:
    def create(self, config):
        self.sample_type = config['sample_type']
        self.decompiler_name = config['decompiler_name']
        self.version = config.get('version', 0)
        if config['requires_library']:
            return self.create_library_based_decompiler(config)
        else:
            return self.create_subprocess_based_decompiler(config)

    def create_subprocess_based_decompiler(self, config):
        nice = config.get('nice', 0)
        timeout = config.get('timeout', 120)
        creates_windows = config.get('creates_windows', False)
        processes_to_kill = config.get('processes_to_kill', [])
        custom_current_working_directory = config.get('custom_current_working_directory', None)
        class_name = eval(config.get('class_name', 'SubprocessBasedDecompiler'))
        return decompiler_class(self.decompiler_name, self.sample_type, nice, timeout,
                                creates_windows, config['decompiler_command'], processes_to_kill,
                                custom_current_working_directory, self.version)

    def create_library_based_decompiler(self, config):
        class_name = config['identifier'][0].upper() + config['identifier'][1:] + 'Decompiler'
        decompiler_class = eval(class_name)
        return decompiler_class(self.decompiler_name, self.sample_type, self.version)
