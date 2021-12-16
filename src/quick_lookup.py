from toga import Box, Button, ScrollContainer
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class QuickLookup(ScrollContainer):
    def __init__(self, root_app, lexical_unit):
        self._root_app_ = root_app
        self._settings_ = root_app._screen_settings_._settings_
        self._lexical_headers_ = list(self._settings_)
        self._lexical_unit_ = lexical_unit
        lexical_values = lexical_unit[1]
        row_size = 4
        row_values = list()
        row_entry = list()
        item_count = 0
        header_count = len(self._lexical_headers_)
        self._value_buttons_ = list()
        for i in range(header_count):
            h = self._lexical_headers_[i]
            s = self._settings_[h]
            t = s['toggled']
            if not t:
                continue
            c = s['color']
            self._value_buttons_.append(
                Button(
                    lexical_values[i],
                    id=f'lookup_entry_{i}',
                    style=Pack(
                        direction=ROW,
                        flex=1,
                        color=c,
                        text_align='center'
                        ),
                    on_press=self.__do_search__
                    )
                )
            row_entry.append(self._value_buttons_[-1])
            if len(row_entry) == row_size or i == header_count - 1:
                row_values.append(
                    Box(
                        style=Pack(
                            direction=ROW,
                            flex=1,
                            text_align='center'
                            ),
                        children=row_entry
                        )
                    )
                row_entry = list()
        self._lookup_entry_ = Button(
            self._lexical_unit_[0],
            id='lookup_entry',
            style=Pack(direction=ROW, flex=1, text_align='center'),
            on_press=self.__do_search__
            )
        self._lookup_values_ = Box(
            id='lookup_box_values',
            style=Pack(direction=COLUMN, flex=1, text_align='center'),
            children=row_values
            )
        self._lookup_layout_ = Box(
            id='lookup_box_layout',
            style=Pack(direction=COLUMN, flex=1, text_align='center'),
            children = [self._lookup_entry_, self._lookup_values_]
            )
        super().__init__(
            id='quick_lookup',
            style=Pack(direction=COLUMN, flex=10),
            content=self._lookup_layout_
            )

    def __do_search__(self, widget):
        self._root_app_.__do_search__(self._lexical_unit_)
