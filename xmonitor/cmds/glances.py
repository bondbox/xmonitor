# coding:utf-8

from typing import List

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

try:
    from xmanage import systemd_path
    default_systemd_system_dir: str = systemd_path.systemd_system_conf_dir
    allowed_systemd_system_dirs: List[str] = systemd_path.systemd_system_dirs
except Exception:
    default_systemd_system_dir: str = "/etc/systemd/system/"
    allowed_systemd_system_dirs: List[str] = [default_systemd_system_dir]


@add_command("create", help="create systemd system unit")
def add_cmd_sd_create(_arg: argp):
    pass


@run_command(add_cmd_sd_create)
def run_cmd_sd_create(cmds: commands) -> int:
    return 0


@add_command("systemd", help="start glances through systemd")
def add_cmd_systemd(_arg: argp):
    pass


@run_command(add_cmd_systemd, add_cmd_sd_create)
def run_cmd_systemd(cmds: commands) -> int:
    return 0


@add_command("glances", help="glances is an an cross-platform monitoring tool")
def add_cmd_glances(_arg: argp):
    pass


@run_command(add_cmd_glances, add_cmd_systemd)
def run_cmd_glances(cmds: commands) -> int:
    return 0
