# coding:utf-8

from .attribute import __author__
from .attribute import __author_email__
from .attribute import __description__
from .attribute import __name__
from .attribute import __url_bugs__
from .attribute import __url_code__
from .attribute import __url_docs__
from .attribute import __url_home__
from .attribute import __version__
from .glances import systemd_service as glances_systemd_service

try:
    from .logrotate import lr_files as logrotate_files
    from .logrotate import lr_state as logrotate_state
    from .logrotate import lr_status as logrotate_status
except Exception:
    pass
