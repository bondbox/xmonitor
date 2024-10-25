# coding:utf-8

from .attribute import __author__  # noqa:F401
from .attribute import __author_email__  # noqa:F401
from .attribute import __description__  # noqa:F401
from .attribute import __project__  # noqa:F401
from .attribute import __urlbugs__  # noqa:F401
from .attribute import __urlcode__  # noqa:F401
from .attribute import __urldocs__  # noqa:F401
from .attribute import __urlhome__  # noqa:F401
from .attribute import __version__  # noqa:F401
from .glances import glances_sd_service as glances_systemd_service  # noqa:F401

try:
    from .logrotate import lr_files as logrotate_files  # noqa:F401
    from .logrotate import lr_state as logrotate_state  # noqa:F401
    from .logrotate import lr_status as logrotate_status  # noqa:F401
except Exception:
    pass
