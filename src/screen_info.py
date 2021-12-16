from toga import Box, WebView
from toga.style import Pack
from toga.style.pack import COLUMN


class InfoScreen(Box):
    def __init__(self, root_app):
        self._root_app_ = root_app
        super().__init__(
            id='screen_info',
            style=Pack(direction=COLUMN, flex=1),
            children=[]
            )
