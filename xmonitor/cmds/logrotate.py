# coding:utf-8

from tabulate import tabulate
from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

try:
    from ..utils import logrotate_files
    from ..utils import logrotate_status

    @add_command("files")
    def add_cmd_files(_arg: argp):
        pass

    @run_command(add_cmd_files)
    def run_cmd_files(cmds: commands) -> int:
        table = tabulate([(f.path, f.desc) for f in logrotate_files],
                         headers=["file", "description"], floatfmt=".1f")
        cmds.stdout(table)
        return 0

    @add_command("version")
    def add_cmd_status_version(_arg: argp):
        _arg.add_opt_off("-v", "--verbose", dest="lr_state_version_verbose",
                         help="turn on verbose mode")

    @run_command(add_cmd_status_version)
    def run_cmd_status_version(cmds: commands) -> int:
        lr_status: logrotate_status = cmds.args.lr_status
        version: str = lr_status.version
        if not cmds.args.lr_state_version_verbose:
            cmds.stdout(f"logrotate state file version: {version}")
        else:
            cmds.stdout(version)
        return 0

    @add_command("status")
    def add_cmd_status(_arg: argp):
        default_status = logrotate_files.status
        _arg.add_argument("-s", "--state", type=str, dest="lr_state_file",
                          nargs=1, default=[default_status], metavar="FILE",
                          help="use an alternate state file, "
                          f"default state file is {default_status}")

    @run_command(add_cmd_status, add_cmd_status_version)
    def run_cmd_status(cmds: commands) -> int:
        state_file: str = cmds.args.lr_state_file[0]
        lr_status = logrotate_status(state_file)
        cmds.args.lr_status = lr_status
        if not cmds.has_sub(add_cmd_status):
            table = tabulate([(i.path, i.time) for i in lr_status],
                             headers=["path", "time"])
            cmds.stdout(table)
        return 0

    @add_command("logrotate")
    def add_cmd_logrotate(_arg: argp):
        pass

    @run_command(add_cmd_logrotate, add_cmd_files, add_cmd_status)
    def run_cmd_logrotate(cmds: commands) -> int:
        return 0
except Exception:
    pass
