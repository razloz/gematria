import gematria.gematria as gem
from toga import Box, WebView, TextInput, Button
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from gematria.quick_lookup import QuickLookup

class HomeScreen(Box):
    def __init__(self, root_app):
        self._root_app_ = root_app
        self._lexical_unit_ = ('CHARITY', gem.full_test('CHARITY'))
        self._entry_headers_ = root_app._entry_headers_
        self._header_count_ = len(self._entry_headers_)
        self._header_range_ = range(self._header_count_)
        self._path_screen_ = f'{root_app._resources_path_}/home_screen.html'
        self._path_history_ = f'{root_app._resources_path_}/history.json'
        self._search_box_ = TextInput(
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
        self._quick_lookup_ = QuickLookup(root_app, self._lexical_unit_)
        self._history_ = root_app.__load_json__(self._path_history_)
        self._history_units_ = [(k, v) for k, v in self._history_.items()]
        root_app.__generate_html__(self._history_units_, self._path_screen_)
        self._view_history_ = WebView(
            id='view_history',
            style=Pack(direction=COLUMN, flex=80),
            url=f'file://{self._path_screen_}'
            )
        super().__init__(
            id='screen_home',
            style=Pack(direction=COLUMN),
            children=[
                self._search_bar_,
                self._quick_lookup_,
                self._view_history_
                ]
            )

    def __get_lexical_unit__(self, search_term):
        lexical_unit = (search_term, [])
        if len(search_term) > 0:
            if not search_term.isnumeric():
                s = search_term
                v = gem.full_test(s)
                lexical_unit = (s, v)
        return lexical_unit

    def __on_text_change__(self, widget):
        v = widget.value
        if len(v) > 0:
            settings = self._root_app_._screen_settings_._settings_
            t = self.__get_lexical_unit__(v.replace(f'\n', '').upper())
            self._quick_lookup_._lookup_entry_.label = t[0]
            r = t[1]
            for b in self._quick_lookup_._value_buttons_:
                for i in self._header_range_:
                    if settings[self._entry_headers_[i]]['toggled']:
                        b.label = r[i]
            if v[-1] == f'\n':
                self.__on_press_evaluate__()

    def __on_press_search__(self, *ignore):
        t = self._search_box_.value.replace(f'\n', '').upper()
        self._lexical_unit_ = self.__get_lexical_unit__(t)
        self._root_app_.__do_search__(self._lexical_unit_)

    def __on_press_evaluate__(self, *ignore):
        search_text = self._search_box_.value.replace(f'\n', '').upper()
        if len(search_text) > 0:
            if not search_text.isnumeric():
                self._history_[search_text] = gem.full_test(search_text)
                self._root_app_.__save_json__(self._path_history_, self._history_)
            self._root_app_.__goto_home__()

    def __on_press_clear__(self, *ignore):
        self._history_ = dict()
        self._root_app_.__save_json__(self._path_history_, self._history_)
        self._root_app_.__goto_home__()

