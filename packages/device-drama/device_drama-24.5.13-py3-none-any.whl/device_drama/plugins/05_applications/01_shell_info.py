import os
from typing import Dict, List

from device_drama.classes.base_plugin import BasePlugin  # type: ignore
from device_drama.classes.logger import Logger  # type: ignore
from device_drama.misc import application_exists, run_command  # type: ignore


class DDPlugin(BasePlugin):
    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger(__name__)
        self.info.author = 'Tadeusz Miszczyk'
        self.info.description = 'Return Shell info'
        self.info.name = 'Shell-info'
        self.info.plugin_version = '24.5.13'
        self.info.compatible_version = '23.9.16'

    @staticmethod
    def get_shell_info() -> str:
        shell_path = os.environ.get('SHELL', None)
        shell_info = '<Unknown>'

        if shell_path is not None:
            shell_version_output = run_command(f'{shell_path} --version').output
            shell_version = '<Unknown Version>'
            if 'elvish' in shell_path:
                shell_version = shell_version_output
            elif shell_version_output.split():
                shell_version = shell_version_output.split()[3].split('(')[0]
            shell_info = f'{os.path.basename(shell_path).title()} {shell_version}'
        return shell_info

    def run(self) -> List[Dict[str, str]]:
        return [
            {
                'type': 'row',
                'title': '       Shell: ',
                'text': self.get_shell_info(),
            }
        ]
