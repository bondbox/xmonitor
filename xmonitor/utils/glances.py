# coding:utf-8

from collections import namedtuple
from configparser import ConfigParser
from enum import Enum
from typing import List
from typing import Optional

from xmanage import systemd_service

try:
    from xmanage import systemd_path
    conf_dir: str = systemd_path.systemd_system_conf_dir
except Exception:
    conf_dir: str = "/etc/systemd/system/"

service_example = namedtuple("glances_service_example",
                             ("path", "unit", "value"))


class glances_sd_service(systemd_service):

    class examples(Enum):
        '''glances systemd service unit examples
        https://github.com/nicolargo/glances/wiki/Start-Glances-through-Systemd
        '''

        server = service_example(conf_dir, "glances-server", """
[Unit]
Description=Glances XML-RPC server (server mode)
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
Description=Glances RESTful server and Web interface
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
Description=Glances export stats to a InfluxDB server
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

        @classmethod
        def names(cls) -> List[str]:
            return [i.name for i in cls]

        @classmethod
        def get_value(cls, name: str) -> service_example:
            return {i.name: i.value for i in cls}[name]

    def __init__(self, path: str, unit: str, config: ConfigParser):
        assert isinstance(path, str), f"unexpected type: {type(path)}"
        assert isinstance(unit, str), f"unexpected type: {type(unit)}"
        assert isinstance(config, ConfigParser), \
            f"unexpected type: {type(config)}"
        self.__path: str = path
        self.__unit: str = unit
        super().__init__(config)

    @property
    def path(self) -> str:
        return self.__path

    @property
    def unit(self) -> str:
        return self.__unit

    @classmethod
    def from_example_name(cls, name: str, path: Optional[str] = None,
                          unit: Optional[str] = None) -> "glances_sd_service":
        example = cls.examples.get_value(name)
        _path: str = example.path if path is None else path
        _unit: str = example.unit if unit is None else unit
        _conf: ConfigParser = cls.read_string(example.value)
        return glances_sd_service(_path, _unit, _conf)

    def create(self, force_update: bool = False) -> None:
        super().create_unit(path=self.path, unit=self.unit,
                            allow_update=force_update)
