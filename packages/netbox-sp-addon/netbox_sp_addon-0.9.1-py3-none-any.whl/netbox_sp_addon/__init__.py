from netbox.plugins import PluginConfig


class SPAddonConfig(PluginConfig):
    """
    This class defines attributes for the scanplus Addon plugin.
    """

    # Plugin package name
    name = "netbox_sp_addon"

    # Human-friendly name and description
    verbose_name = "qbeyond Addon"
    description = "Add functions used by qbeyond AG"

    # Plugin version
    version = "0.9.1"

    # Plugin author
    author = "Tobias Genannt"
    author_email = "tobias.genannt@qbeyond.de"

    # Configuration parameters that MUST be defined by the user (if any)
    required_settings = []

    # Default configuration parameter values, if not set by the user
    default_settings = {}

    # Base URL path. If not set, the plugin name will be used.
    base_url = "sp-addon"

    # Minimun Netbox version
    min_version = "4.0.0"


config = SPAddonConfig
