# coding:utf-8

import shutil
from typing import Tuple

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

try:
    from xmanage import systemd_path
    default_systemd_system_dir: str = systemd_path.systemd_system_conf_dir
    allowed_systemd_system_dirs: Tuple[str, ...]\
        = systemd_path.systemd_system_dirs
except Exception:
    default_systemd_system_dir: str = "/etc/systemd/system/"
    allowed_systemd_system_dirs: Tuple[str, ...]\
        = (default_systemd_system_dir,)

from ..utils import glances_systemd_service as glances_service


@add_command("create", help="create systemd system unit")
def add_cmd_sd_create(_arg: argp):
    _arg.add_opt_on("--force-update", dest="glances_sd_force_update",
                    help="allow force update")
    allowed_names = glances_service.examples.names()
    _arg.add_argument(dest="glances_sd_names", metavar="NAME", nargs="+",
                      choices=allowed_names, help="service unit name")


@run_command(add_cmd_sd_create)
def run_cmd_sd_create(cmds: commands) -> int:
    where = shutil.which("glances")
    assert isinstance(where, str), "glances not found"
    force_update = cmds.args.glances_sd_force_update
    for name in cmds.args.glances_sd_names:
        service = glances_service.from_example_name(name)
        options = [where] + glances_service.examples.get_value(name).options
        service.service_section.ExecStart = chr(32).join(options)
        service.create(force_update)
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
