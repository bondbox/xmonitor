# coding:utf-8

from typing import List
from typing import Optional
from typing import Sequence

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from ..utils import __description__
from ..utils import __name__
from ..utils import __url_home__
from ..utils import __version__

subs: List[add_command] = list()

try:
    from .logrotate import add_cmd_logrotate
    subs.append(add_cmd_logrotate)
except Exception:
    pass


@add_command(__name__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, *subs)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description=__description__,
        epilog=f"For more, please visit {__url_home__}.")
