from dcim.forms import DeviceFilterForm
from dcim.models import RackRole
from django.utils.translation import gettext_lazy as _
from utilities.forms.fields import DynamicModelMultipleChoiceField
from utilities.forms.rendering import FieldSet

class SPDeviceFilterForm(DeviceFilterForm):
    fieldsets = (
        FieldSet('q', 'filter_id', 'tag'),
        FieldSet('region_id', 'site_group_id', 'site_id', 'location_id', 'rack_role', 'rack_id', name=_('Location')),
        FieldSet('status', 'role_id', 'airflow', 'serial', 'asset_tag', 'mac_address', name=_('Operation')),
        FieldSet('manufacturer_id', 'device_type_id', 'platform_id', name=_('Hardware')),
        FieldSet('tenant_group_id', 'tenant_id', name=_('Tenant')),
        FieldSet('contact', 'contact_role', 'contact_group', name=_('Contacts')),
        FieldSet(
            'console_ports', 'console_server_ports', 'power_ports', 'power_outlets', 'interfaces', 'pass_through_ports',
            name=_('Components')
        ),
        FieldSet(
            'has_primary_ip', 'has_oob_ip', 'virtual_chassis_member', 'config_template_id', 'local_context_data',
            name=_('Miscellaneous')
        )
    )

    rack_role = DynamicModelMultipleChoiceField(
        queryset=RackRole.objects.all(),
        required=False,
        label="Rack role",
    )
