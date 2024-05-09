from extras.plugins import PluginConfig
from .version import __version__

class NetboxDataConfig(PluginConfig):
    name = 'netbox_data'
    verbose_name = 'Netbox Data'
    description = 'Get Netbox Data'
    version = __version__
    base_url = 'netbox-data'
    min_version = '3.4.0'

config = NetboxDataConfig
