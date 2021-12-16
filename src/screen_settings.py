from toga import Box, Switch, Selection, Label
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class SettingsScreen(Box):
    def __init__(self, root_app):
        self._setup_complete_ = False
        self._root_app_ = root_app
        self._path_settings_ = f'{root_app._resources_path_}/settings.json'
        self._settings_ = root_app.__load_json__(self._path_settings_)
        self._headers_label_ = self._root_app_._entry_headers_
        self._headers_len_ = len(self._headers_label_)
        self._headers_range_ = range(self._headers_len_)
        settings_keys = self._settings_.keys()
        self._colors_ = [
            'BLACK',
            'BLUE',
            'BROWN',
            'CYAN',
            'DARKGRAY',
            'GRAY',
            'GREEN',
            'LIGHTGRAY',
            'MAGENTA',
            'ORANGE',
            'PURPLE',
            'RED',
            'WHITE',
            'YELLOW'
            ]
        self._ciphers_ = list()
        self._cipher_colors_ = list()
        self._cipher_boxes_ = [Label('Ciphers to display:')]
        for i in self._headers_range_:
            label = self._headers_label_[i]
            if label not in settings_keys:
                self._settings_[label] = {'toggled': True, 'color': 'BLACK'}
            self._ciphers_.append(
                Switch(
                    'Show',
                    id=f'cipher_{i}',
                    style=Pack(direction=ROW, flex=1),
                    on_toggle=self.__update_settings__,
                    is_on=self._settings_[label]['toggled']
                    )
                )
            self._cipher_colors_.append(
                Selection(
                    id=f'cipher_color_{i}',
                    style=Pack(direction=ROW, flex=1),
                    items=self._colors_,
                    on_select=self.__update_settings__
                    )
                )
            self._cipher_colors_[i].value = self._settings_[label]['color']
            self._cipher_boxes_.append(
                Box(
                    id=f'cipher_box_{i}',
                    style=Pack(direction=ROW, flex=1),
                    children=[
                        Box(
                            id=f'cipher_box_child_{i}-0',
                            style=Pack(direction=COLUMN, flex=1, padding=5),
                            children=[
                                Label(label),
                                self._ciphers_[i]
                                ]
                            ),
                        Box(
                            id=f'cipher_box_child_{i}-1',
                            style=Pack(direction=COLUMN, flex=1, padding=5),
                            children=[
                                Label('Color'),
                                self._cipher_colors_[i]
                                ]
                            )
                        ]
                    )
                )
        super().__init__(
            id='screen_settings',
            style=Pack(direction=COLUMN, flex=1),
            children=self._cipher_boxes_
            )
        self._setup_complete_ = True

    def __update_settings__(self, widget):
        if self._setup_complete_:
            for i in self._headers_range_:
                key = self._headers_label_[i]
                self._settings_[key]['toggled'] = self._ciphers_[i].is_on
                self._settings_[key]['color'] = self._cipher_colors_[i].value
            self._root_app_.__save_json__(self._path_settings_, self._settings_)
