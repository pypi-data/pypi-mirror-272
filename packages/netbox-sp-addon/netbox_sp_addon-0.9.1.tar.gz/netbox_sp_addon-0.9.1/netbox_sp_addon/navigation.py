from netbox.plugins import PluginMenuItem


# Declare a list of menu items to be added to NetBox's built-in naivgation menu
menu_items = (
    PluginMenuItem(
        link="plugins:netbox_sp_addon:sp_device_list",
        link_text="Devices (additional filters)",
    ),
)
