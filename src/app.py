"""
Gematria Calc
"""
import asyncio
import gematria.gematria as gem
import toga
import time
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
WORDS_HISTORY = gem.get_history()
WORDS_LEXICON = gem.get_lexicon()
SRP = Pack(direction=ROW, padding=5)
SCP = Pack(direction=COLUMN, padding=5)
SFP = Pack(flex=1, padding=5)
OTHER_COLORS = [
    'BLACK',
    'DARKGRAY',
    'GRAY',
    'LIGHTGRAY',
    'WHITE',
    'YELLOW',
    'CLEAR',
    'CYAN',
    'MAGENTA'
    ]
COLOR_PACKS = list()
for color in ['BLUE', 'GREEN', 'BROWN', 'ORANGE', 'RED', 'PURPLE', 'BLACK']:
    COLOR_PACKS.append(
        Pack(
            color=color,
            direction=ROW,
            flex=1,
            alignment='center'
            )
        )
COLOR_RANGE = range(len(COLOR_PACKS) - 2)
FULL_TEST_LABELS = [
    'Standard',
    'Reverse Standard',
    'Reduction',
    'Reverse Reduction',
    'Sumerian',
    'Reverse Sumerian',
    'Jewish',
    'Reverse Jewish',
    'Fibonacci',
    'Reverse Fibonacci'
    ]
EMPTY_ENTRY = [0 for i in range(len(FULL_TEST_LABELS))]


class ColorfulEntry(toga.Box):
    """
    Colorized display of a single lexicon entry.
    """
    def create_layout(self, root_app, entry_word, entry_data):
        """
        Create objects with given data.
        """
        self.style = Pack(direction=COLUMN, flex=1)
        self.entry_word = entry_word
        self.entry_data = entry_data
        self.searchable_elements = [
            toga.Button(
                entry_word,
                style=COLOR_PACKS[-1],
                on_press=root_app.__do_full_search__
                )
            ]
        ci = 0
        change_color = False
        for entry in entry_data:
            if ci > COLOR_RANGE[-1]:
                ci = 0
            self.searchable_elements.append(
                toga.Button(
                    entry,
                    style=COLOR_PACKS[ci],
                    on_press=root_app.__do_full_search__
                    )
                )
            if change_color:
                ci += 1
            change_color = not change_color
        elements = 4
        elements_max = 4
        obj = list()
        layout_objects = list()
        for element in self.searchable_elements:
            obj.append(element)
            elements += 1
            if elements >= elements_max:
                elements = 0
                layout_objects.append(
                    toga.Box(
                        style=Pack(direction=ROW),
                        children=obj
                        )
                    )
                obj = list()
        layout_objects.append(
            toga.Box(
                style=Pack(direction=ROW),
                children=obj
                )
            )
        self.add(
            toga.Box(
                style=Pack(direction=COLUMN),
                children=layout_objects
                )
            )


class ViewportSearch(toga.Box):
    """
    Main window content for searching the lexicon.
    """
    def create_layout(self, root_app, word='DIVINE'):
        """
        Create objects and apply them to the layout.
        """
        self.style = Pack(direction=COLUMN)
        self.search_box = toga.TextInput(
            style=Pack(flex=2),
            on_change=root_app.__search_change_event__
            )
        self.button_search = toga.Button(
            style=Pack(flex=1),
            label='Search',
            on_press=root_app.__do_lexicon_search__
            )
        self.button_settings = toga.Button(
            style=Pack(flex=1),
            label='Settings',
            on_press=root_app.__goto_settings__
            )
        self.search_bar = toga.Box(
            style=Pack(direction=ROW, flex=1),
            children=[
                self.search_box,
                self.button_search,
                self.button_settings
                ]
            )
        self.quick_lookup = ColorfulEntry()
        if word.isnumeric():
            self.quick_lookup.create_layout(
                root_app,
                word,
                EMPTY_ENTRY
                )
        else:
            self.quick_lookup.create_layout(
                root_app,
                word,
                gem.full_test(word)
                )
        root_app.display_page = list()
        if len(root_app.results_page) > 0:
            for entry in root_app.results_page[root_app.current_page]:
                obj = SearchEntry()
                obj.create_layout(root_app, entry[0])
                root_app.display_page.append(obj)
        self.results_list = toga.ScrollContainer(
            style=Pack(direction=COLUMN, flex=4),
            )
        self.results_list.content = toga.Box(
            style=Pack(direction=COLUMN, flex=1),
            children=root_app.display_page
            )
        self.results_bar = toga.Box(
            style=Pack(direction=ROW, flex=2),
            children=[
                toga.Button(
                    style=Pack(direction=ROW, flex=1),
                    label='Previous',
                    on_press=root_app.__view_results_page__
                    ),
                toga.Button(
                    style=Pack(direction=ROW, flex=1),
                    label='Next',
                    on_press=root_app.__view_results_page__
                    )
                ]
            )
        self.add(self.search_bar)
        self.add(self.quick_lookup)
        self.add(self.results_list)
        self.add(self.results_bar)


class ViewportSettings(toga.Box):
    """
    Main window content for changing settings.
    """
    def create_layout(self, root_app):
        """
        Create objects and apply them to the layout.
        """
        self.style = Pack(direction=COLUMN)
        self.button_goto_search = toga.Button(
            style=SFP,
            label='Search',
            on_press=root_app.__goto_search__
            )
        self.opt_list = list()
        for label_text in FULL_TEST_LABELS:
            self.opt_list.append(
                toga.Switch(
                    label_text,
                    style=SFP,
                    is_on=True
                    )
                )
        self.opt_switches = toga.Box(
            style=SCP,
            children=self.opt_list
            )
        self.match_all = toga.Switch(
            'Match All',
            style=SFP
            )
        self.history_select = toga.Selection(
            style=SFP,
            items=WORDS_HISTORY.keys()
            )
        self.button_clear_history = toga.Button(
            style=SFP,
            label='Clear',
            on_press=root_app.__clear_history__
            )
        self.button_delete_history = toga.Button(
            style=SFP,
            label='Delete',
            on_press=root_app.__delete_history__
            )
        self.add(
            toga.Box(
                style=SCP,
                children=[
                    self.button_goto_search,
                    toga.Label(
                        'Select which values to compare when searching:'
                        ),
                    self.opt_switches,
                    self.match_all,
                    toga.Label(
                        'Search History:',
                        style=SFP
                        ),
                    self.history_select,
                    toga.Box(
                        style=SRP,
                        children=[
                            self.button_clear_history,
                            self.button_delete_history
                            ]
                        )
                    ]
                )
            )


class SearchEntry(toga.Box):
    """
    Widget for comparing search results.
    """
    def create_layout(self, root_app, entry):
        self.style = Pack(direction=COLUMN)
        self._entry_ = entry
        self.add(
            toga.Button(
                entry,
                style=COLOR_PACKS[-1],
                on_press=root_app.__compare_words__
                )
            )


class ViewportCompare(toga.Box):
    """
    Main window content for comparing lexicon entries.
    """
    def create_layout(self, root_app, top_entry, bottom_entry):
        """
        Create objects and apply them to the layout.
        """
        self.style = Pack(direction=COLUMN)
        self.nav_bar = toga.Box(
            style=Pack(direction=ROW),
            children=[
                toga.Button(
                    style=Pack(direction=ROW, flex=1),
                    label='Search',
                    on_press=root_app.__goto_search__
                    ),
                toga.Button(
                    style=Pack(direction=ROW, flex=1),
                    label='Settings',
                    on_press=root_app.__goto_settings__
                    )
                ]
            )
        self.top_entry = ColorfulEntry()
        self.top_entry.create_layout(
            root_app,
            top_entry[0],
            top_entry[1]
            )
        self.bottom_entry = ColorfulEntry()
        self.bottom_entry.create_layout(
            root_app,
            bottom_entry[0],
            bottom_entry[1]
            )
        self.add(self.nav_bar)
        self.add(self.top_entry)
        self.add(self.bottom_entry)


class GematriaApp(toga.App):
    """
    Main application for pairing numbers to letters, words, and phrases.
    """
    async def __search_lexicon__(self, *args):
        """
        Check lexicon for word or phrase.
        """
        search_term = self._last_entry_[0].replace(f'\n', '').upper()
        search_results = self._last_entry_[1]
        self.results_page = list()
        self.current_page = 0
        cat_words = dict(WORDS_HISTORY)
        cat_words.update(WORDS_LEXICON)
        lexicon_keys = cat_words.keys()
        new_entry = False
        numeric_search = search_term.isnumeric()
        if not numeric_search:
            if search_term not in lexicon_keys:
                new_entry = True
        else:
            search_term = int(search_term)
        toggle_check = list()
        for switch in self.settings_viewport.opt_list:
            toggle_check.append(switch)
        toggle_len = len(toggle_check)
        full_check = range(toggle_len)
        matched_words = list()
        match_all = self.settings_viewport.match_all.is_on
        toggled = 0
        for b in toggle_check:
            if b:
                toggled += 1
        if any(toggle_check):
            for key in lexicon_keys:
                if key == search_term:
                    continue
                matched = False
                lexicon_entry = cat_words[key]
                matches = 0
                for i in full_check:
                    if toggle_check[i] and not matched:
                        if not numeric_search:
                            if lexicon_entry[i] == search_results[i]:
                                if match_all:
                                    matches += 1
                                    if toggled == matches:
                                        matched = True
                                else:
                                    matched = True
                        else:
                            if lexicon_entry[i] == search_term:
                                if match_all:
                                    matches += 1
                                    if toggled == matches:
                                        matched = True
                                else:
                                    matched = True
                if matched:
                    matched_words.append(key)
        sorted_results = [list() for i in full_check]
        for word in matched_words:
            lexicon_entry = cat_words[word]
            entry_range = range(len(lexicon_entry))
            m = -1
            if numeric_search:
                for i in entry_range:
                    if lexicon_entry[i] == search_term:
                        m += 1
            else:
                for i in entry_range:
                    if lexicon_entry[i] == search_results[i]:
                        m += 1
            sorted_results[m].append((word, lexicon_entry))
        entry_objects = list()
        for i in full_check:
            p = (toggle_len - 1) - i
            for e in sorted_results[p]:
                entry_objects.append(e)
                if len(entry_objects) == 6:
                    self.results_page.append(entry_objects)
                    entry_objects = list()
        if new_entry:
            WORDS_HISTORY[search_term] = search_results
            gem.save_history(WORDS_HISTORY)
        self.__goto_search__()
        return False

    def __view_results_page__(self, widget):
        """
        Update results list with new content from page index.
        """
        if len(self.results_page) < 1:
            return None
        if widget.label == 'Previous':
            self.current_page -= 1
            if self.current_page < 0:
                self.current_page = 0
        elif widget.label == 'Next':
            self.current_page += 1
            last_page = len(self.results_page) - 1
            if self.current_page > last_page:
                self.current_page = last_page
        self.__goto_search__()

    def __search_change_event__(self, widget):
        """
        Do full test as text changes.
        """
        do_search = False
        search_term = widget.value.upper()
        if len(search_term) < 1:
            return None
        if search_term[:-1] == f'\n':
            do_search = True
            search_term = search_term.replace(f'\n', '')
        if search_term.isnumeric():
            self._last_entry_ = [search_term, EMPTY_ENTRY]
        else:
            self._last_entry_ = [search_term, gem.full_test(search_term)]
        if do_search:
            self.add_background_task(self.__search_lexicon__)
            widget.value = ''
        elif not search_term.isnumeric():
            entry_obj = self.search_viewport.quick_lookup.searchable_elements
            entry_obj[0].label = self._last_entry_[0]
            for i in range(len(self._last_entry_[1])):
                entry_obj[i + 1].label = self._last_entry_[1][i]

    def __compare_words__(self, widget):
        """
        Compare selected entry with last search.
        """
        w = widget.label
        self._compare_entry_ = [w, gem.full_test(w)]
        self.__goto_compare__()

    def __do_full_search__(self, widget):
        """
        Search lexicon for widget value.
        """
        w = widget.label
        if w.isnumeric():
            self._last_entry_ = [w, EMPTY_ENTRY]
        else:
            self._last_entry_ = [w, gem.full_test(w)]
        self.add_background_task(self.__search_lexicon__)

    def __do_lexicon_search__(self, widget):
        """
        Signal that a search is ready.
        """
        e = self.search_viewport.search_box.value.replace(f'\n', '')
        self._last_entry_ = [e, gem.full_test(e)]
        self.add_background_task(self.__search_lexicon__)

    def __goto_search__(self, *ignore):
        """
        Switch to search viewport.
        """
        self.search_viewport = ViewportSearch()
        self.search_viewport.create_layout(
            self,
            word=self._last_entry_[0]
            )
        self.main_window.title = 'Alphabetical Mystery Tour'
        self.main_window.content = self.search_viewport

    def __goto_settings__(self, *ignore):
        """
        Switch to settings viewport.
        """
        self.settings_viewport = ViewportSettings()
        self.settings_viewport.create_layout(self)
        self.main_window.title = 'Settings'
        self.main_window.content = self.settings_viewport

    def __goto_compare__(self, *ignore):
        """
        Switch to compare viewport.
        """
        self.compare_viewport = ViewportCompare()
        self.compare_viewport.create_layout(
            self,
            self._last_entry_,
            self._compare_entry_
            )
        self.main_window.title = 'Comparison'
        self.main_window.content = self.compare_viewport

    def __delete_history__(self, *ignore):
        """
        Delete word from search history.
        """
        selected_word = str(self.history_select.value)
        if selected_word in WORDS_HISTORY.keys():
            del WORDS_HISTORY[selected_word]
            gem.save_history(WORDS_HISTORY)
            self.history_select.items = WORDS_HISTORY.keys()

    def __clear_history__(self, *ignore):
        """
        Clear all words from search history.
        """
        WORDS_HISTORY = dict()
        gem.save_history(WORDS_HISTORY)
        self.history_select.items = WORDS_HISTORY.keys()

    def startup(self):
        """
        Attempt to build and show the application.
        """
        ### Global variables ###
        self.results_page = list()
        self.display_page = list()
        self.current_page = 0
        ### Search Viewport ###
        self._last_entry_ = [
            'GEMATRIA',
            gem.full_test('GEMATRIA')
            ]
        self.search_viewport = ViewportSearch()
        self.search_viewport.create_layout(
            self,
            word=self._last_entry_[0]
            )
        ### Settings Viewport ###
        self.settings_viewport = ViewportSettings()
        self.settings_viewport.create_layout(self)
        ### Compare Viewport ###
        self._compare_entry_ = self._last_entry_
        self.compare_viewport = ViewportCompare()
        self.compare_viewport.create_layout(
            self,
            self._last_entry_,
            self._compare_entry_
            )
        ### Main Window ###
        self.main_window = toga.MainWindow(title='Alphabetical Mystery Tour')
        self.main_window.content = self.search_viewport

def main():
    """
    Start the application.
    """
    return GematriaApp()
