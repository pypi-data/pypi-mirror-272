from typing import Dict

from textual.app import App
from textual.containers import Container
from textual.screen import Screen

from lolcatt.casting.caster import Caster
from lolcatt.ui.lolcatt_controls import LolCattControls
from lolcatt.ui.lolcatt_device_info import LolCattDeviceInfo
from lolcatt.ui.lolcatt_devicelist import LolCattDevicelist
from lolcatt.ui.lolcatt_playback_info import LolCattPlaybackInfo
from lolcatt.ui.lolcatt_playlist import LolCattPlaylist
from lolcatt.ui.lolcatt_progress import LolCattProgress
from lolcatt.ui.lolcatt_url_input import LolCattUrlInput


class RemoteScreen(Screen):
    """A screen for the remote control UI."""

    def compose(self):
        yield Container(
            LolCattDeviceInfo(),
            LolCattPlaybackInfo(),
            LolCattProgress(),
            LolCattControls(),
            LolCattUrlInput(),
            id='app',
        )


class PlaylistScreen(Screen):
    """A screen for the playlist UI."""

    def compose(self):
        yield LolCattPlaylist()


class DeviceScreen(Screen):
    """A screen for the device info UI."""

    def compose(self):
        yield LolCattDevicelist()


class LolCatt(App):
    """The main application class for lolcatt."""

    CSS_PATH = 'ui/lolcatt.tcss'

    def __init__(self, device_name: str = None, config: Dict = None, *args, **kwargs):
        self.config = config
        self.caster = Caster(device_name, config=config)
        self.remote_screen = None
        self.playlist_screen = None
        self.device_screen = None
        super().__init__(*args, **kwargs)

    def on_mount(self):
        self.remote_screen = RemoteScreen()
        self.playlist_screen = PlaylistScreen()
        self.device_screen = DeviceScreen()
        self.install_screen(self.remote_screen, name='remote')
        self.install_screen(self.playlist_screen, name='playlist')
        self.install_screen(self.device_screen, name='device')
        self.push_screen('remote')


if __name__ == '__main__':
    app = LolCatt('default')
    app.run()
