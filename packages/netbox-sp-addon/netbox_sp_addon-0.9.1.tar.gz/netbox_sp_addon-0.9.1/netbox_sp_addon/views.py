from dcim.views import DeviceListView

from .filters import SPDeviceFilterSet
from .forms import SPDeviceFilterForm


class SPDeviceListView(DeviceListView):
    filterset = SPDeviceFilterSet
    filterset_form = SPDeviceFilterForm
