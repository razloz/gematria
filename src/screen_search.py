import gematria.gematria as gem
from toga import Box, WebView, TextInput, Button
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from gematria.table_wright import TableWright


class SearchScreen(Box):
    def __init__(self, root_app):
        self._root_app_ = root_app
        self._search_unit_ = root_app._search_unit_
        self._lexical_units_ = root_app._lexical_units_
        self._button_previous_ = Button(
            'Previous',
            id='button_next',
            style=Pack(direction=COLUMN, flex=1),
            on_press=self._root_app_.__view_results_page__
            )
        self._button_next_ = Button(
            'Next',
            id='button_next',
            style=Pack(direction=COLUMN, flex=1),
            on_press=self._root_app_.__view_results_page__
            )
        self._nav_box_ = Box(
            id='nav_box',
            style=Pack(direction=ROW, flex=1),
            children=[self._button_previous_, self._button_next_]
            )
        self._table_wright_ = TableWright(root_app)
        super().__init__(
            id='screen_search',
            style=Pack(direction=COLUMN),
            children=[self._nav_box_, self._table_wright_]
            )
