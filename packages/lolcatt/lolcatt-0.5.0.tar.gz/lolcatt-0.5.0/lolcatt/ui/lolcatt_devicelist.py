#!/usr/bin/env python3
from catt.cli import get_config_as_dict
from textual import on
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Button
from textual.widgets import Label
from textual.widgets import ListItem
from textual.widgets import ListView
from textual.widgets import Static


class LolCattDeviceListView(ListView):
    def on_list_view_selected(self, selected):
        try:
            self.app.caster.change_device(selected.item.devicename)
            self.app.pop_screen()
        except AttributeError:
            pass


class LolCattDevicelist(Static):

    devices = reactive([])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listview = LolCattDeviceListView(
            ListItem(Label('Scanning...')),
            id="devicelist",
            initial_index=None,
        )
        self.available_devices = list(get_config_as_dict().get("aliases", {}).values())
        self.active_device = None
        self.close_btn = Button("X", id="devicelist_close_btn")

    def compose(self):
        yield Vertical(self.listview, self.close_btn, id="devicelist_box")

    def update_list(self):
        new_device_name = self.app.caster.get_device_name()
        if self.active_device == new_device_name:
            return
        self.active_device = new_device_name
        self.listview.clear()
        active_idx = None
        for i, device in enumerate(self.available_devices):
            if device == new_device_name:
                id = "active_device_listitem"
                active_idx = i
            else:
                id = f"device_listitem_{i}"
            li_obj = ListItem(Label(device), id=id)
            li_obj.devicename = device
            self.listview.append(li_obj)
        self.listview.index = active_idx

    async def on_mount(self):
        self.set_interval(1, self.update_list)

    @on(Button.Pressed, "#devicelist_close_btn")
    def on_close_btn(self):
        self.app.pop_screen()
