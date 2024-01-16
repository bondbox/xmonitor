# coding:utf-8

from collections import namedtuple
from enum import Enum

from xmanage import systemd_service

try:
    from xmanage import systemd_path
    conf_dir: str = systemd_path.systemd_system_conf_dir
except Exception:
    conf_dir: str = "/etc/systemd/system/"

service_example = namedtuple("glances_service_example",
                             ("path", "unit", "value"))


class glances_systemd_service(systemd_service):

    class examples(Enum):
        '''glances systemd service unit examples
        https://github.com/nicolargo/glances/wiki/Start-Glances-through-Systemd
        '''

        server = service_example(conf_dir, "glances-server", """
[Unit]
Description=Glances
After=network.target

[Service]
ExecStart=/usr/local/bin/glances -s
Restart=on-abort
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
""")
        webserver = service_example(conf_dir, "glances-webserver", """
[Unit]
Description=Glances
After=network.target

[Service]
ExecStart=/usr/local/bin/glances -w
Restart=on-abort
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
""")
        influxdb = service_example(conf_dir, "glances-influxdb", """
[Unit]
Description=Glances
After=network.target influxd.service

[Service]
ExecStart=/usr/local/bin/glances --quiet --export influxdb
Restart=on-failure
RemainAfterExit=yes
RestartSec=30s
TimeoutSec=30s

[Install]
WantedBy=multi-user.target
""")
