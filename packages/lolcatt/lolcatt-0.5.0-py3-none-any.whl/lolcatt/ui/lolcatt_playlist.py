#!/usr/bin/env python3
from textual import on
from textual.containers import Vertical
from textual.widgets import Button
from textual.widgets import Label
from textual.widgets import ListItem
from textual.widgets import ListView
from textual.widgets import Static


class LolCattPlaybackListView(ListView):
    def on_list_view_selected(self, selected):
        try:
            self.app.caster.cast_at_idx(selected.item.idx)
        except AttributeError:
            pass


class LolCattPlaylist(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listview = LolCattPlaybackListView(
            ListItem(Label('Loading...')),
            id="playlist",
            initial_index=None,
        )
        self._current = None
        self._previous = []
        self._queue = []
        self._next = []
        self.close_btn = Button("X", id="playlist_close_btn")

    def compose(self):
        yield Vertical(self.listview, self.close_btn, id="playlist_box")

    def update_list(self):
        previous = self.app.caster.get_played_queue()
        current = self.app.caster.get_current_item()
        next = self.app.caster.get_queue()
        if self._previous == previous and self._current == current and self._next == next:
            return
        self._previous = previous[:]
        self._current = current
        self._next = next[:]
        self._items = previous + [current] + next
        self.listview.clear()
        zero_item = None
        for i, item in enumerate(self._items):
            if item is None:
                continue
            idx = self._items.index(item) - len(previous)
            if item.startswith('https://'):
                item = item[8:]
            label = item[:35] + '...' if len(item) > 35 else item
            label_obj = Label(label)
            li_obj = ListItem(label_obj, id=f'playlist_item_{idx}')
            li_obj.idx = idx
            self.listview.append(li_obj)
            if idx == 0:
                zero_item = i
        if zero_item is not None:
            self.listview.index = zero_item

    def on_mount(self):
        self.set_interval(1, self.update_list)

    @on(Button.Pressed, "#playlist_close_btn")
    def on_close_btn(self):
        self.app.pop_screen()
