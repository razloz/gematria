import gematria.gematria as gem
from toga import Box, WebView, TextInput, Button
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from gematria.table_wright import TableWright


class HomeScreen(Box):
    def __init__(self, root_app):
        self._root_app_ = root_app
        self._entry_headers_ = root_app._entry_headers_
        self._header_count_ = len(self._entry_headers_)
        self._header_range_ = range(self._header_count_)
        self._path_history_ = f'{root_app._resources_path_}/history.json'
        if not root_app._clear_search_text_:
            initial_text = root_app._search_unit_[0]
        else:
            initial_text = ''
            root_app._clear_search_text_ = False
        self._search_box_ = TextInput(
            initial=initial_text,
            placeholder='GEMATRIA',
            style=Pack(direction=ROW, flex=1),
            on_change=self.__on_text_change__
            )
        self._search_button_ = Button(
            'Search',
            style=Pack(direction=ROW, flex=1),
            on_press=self.__on_press_search__
            )
        self._evaluate_button_ = Button(
            'Evaluate',
            style=Pack(direction=ROW, flex=1),
            on_press=self.__on_press_evaluate__
            )
        self._clear_button_ = Button(
            'Clear',
            style=Pack(direction=ROW, flex=1),
            on_press=self.__on_press_clear__
            )
        self._search_bar_ = Box(
            style=Pack(direction=COLUMN, flex=10),
            children=[
                self._search_box_,
                Box(
                    style=Pack(direction=ROW, flex=1),
                    children=[
                        self._search_button_,
                        self._evaluate_button_,
                        self._clear_button_
                        ]
                    )
                ]
            )
        self._search_unit_ = root_app._search_unit_
        self._history_ = root_app.__load_json__(self._path_history_)
        root_app._lexical_units_ = [(k, v) for k, v in self._history_.items()]
        self._table_wright_ = TableWright(root_app)
        super().__init__(
            id='screen_home',
            style=Pack(direction=COLUMN),
            children=[
                self._search_bar_,
                self._table_wright_
                ]
            )

    def __on_text_change__(self, widget):
        v = widget.value
        if len(v) > 0:
            t = v.replace(f'\n', '').upper()
            if not self._root_app_._search_unit_[0] == t:
                if not t.isnumeric():
                    self._root_app_._search_unit_ = (t, gem.full_test(t))
                    self._table_wright_.build_table()
            if v[-1] == f'\n':
                self.__on_press_evaluate__()

    def __on_press_search__(self, *ignore):
        t = self._search_box_.value.replace(f'\n', '').upper()
        lexical_unit = (t, self._root_app_._empty_values_)
        if len(t) > 0:
            if not t.isnumeric():
                lexical_unit = (t, gem.full_test(t))
        self._root_app_._clear_search_text_ = True
        self._root_app_.__do_search__(lexical_unit)

    def __on_press_evaluate__(self, *ignore):
        search_text = self._search_box_.value.replace(f'\n', '').upper()
        if len(search_text) > 0:
            if not search_text.isnumeric():
                self._history_[search_text] = gem.full_test(search_text)
                self._root_app_.__save_json__(self._path_history_, self._history_)
            self._root_app_._clear_search_text_ = True
            self._root_app_.__goto_home__()

    def __on_press_clear__(self, *ignore):
        self._history_ = dict()
        self._root_app_.__save_json__(self._path_history_, self._history_)
        self._root_app_.__goto_home__()

