"""
Gematria Calc
"""
import toga, json, asyncio
import gematria.gematria as gem
from toga import Icon
from toga.command import Command, Group
from gematria.screen_home import HomeScreen
from gematria.screen_search import SearchScreen
from gematria.screen_settings import SettingsScreen
from gematria.screen_info import InfoScreen
from gematria.screen_loading import LoadingScreen
from os.path import dirname, realpath, abspath, exists


def process_lexical_units(
    lexicon,
    search_term,
    search_results,
    check_range,
    toggle_values,
    toggle_count,
    numeric_search
    ):
    """
    Returns a list of matched lexical units.
    """
    results = list()
    for key, values in lexicon.items():
        if key == search_term:
            continue
        matched = False
        matches = 0
        for i in check_range:
            if toggle_values[i] and not matched:
                if not numeric_search:
                    m = values[i] == search_results[i]
                else:
                    m = values[i] == search_term
                if m:
                    matched = True
        if matched:
            results.append((key, values))
    return results



class GematriaApp(toga.App):
    async def __await_lexicon__(self, *args):
        self._lexicon_full_ = self.__load_json__(self._lexicon_path_)
        self._lexicon_keys_ = list(self._lexicon_full_)
        self._lexicon_len_ = len(self._lexicon_keys_)
        self.__goto_home__()
        return False

    def __do_search__(self, lexical_unit):
        self._search_term_ = lexical_unit[0]
        self._search_values_ = lexical_unit[1]
        self.__goto_loading__()
        self._await_thread_ = self.add_background_task(self.__search_lexicon__)

    async def __search_lexicon__(self, *args):
        """
        Search lexicon for matched units.
        """
        self._results_page_ = list()
        self._current_page_ = 0
        search_term = self._search_term_.replace(f'\n', '').upper()
        if len(search_term) == 0:
            self.__goto_home__()
            return False
        search_results = self._search_values_
        numeric_search = search_term.isnumeric()
        if numeric_search:
            search_term = int(search_term)
        settings = self._screen_settings_._settings_
        toggle_values = [v['toggled'] for v in settings.values()]
        toggle_count = sum([1 if b else 0 for b in toggle_values])
        toggle_len = len(toggle_values)
        check_range = range(toggle_len)
        if toggle_count == 0:
            self.__goto_home__()
            return False
        _args_ = (
            search_term,
            search_results,
            check_range,
            toggle_values,
            toggle_count,
            numeric_search
        )
        sorted_results = [list() for _ in check_range]
        m = process_lexical_units(self._lexicon_full_, *_args_)
        h = self._screen_home_._history_
        if len(h) > 0:
            m += process_lexical_units(h, *_args_)
        for entry in sorted(m):
            matched = -1
            for i in check_range:
                if numeric_search:
                    e = entry[1][i] == search_term
                else:
                    e = entry[1][i] == search_results[i]
                if e:
                    matched += 1
            sorted_results[matched].append(entry)
        entry_objects = list()
        for i in check_range:
            p = (toggle_len - 1) - i
            for e in sorted_results[p]:
                entry_objects.append(e)
                if len(entry_objects) == self._display_lexical_units_:
                    self._results_page_.append(entry_objects)
                    entry_objects = list()
        self.__view_results_page__(None)
        return False

    def __view_results_page__(self, widget):
        """
        Update results list with new content from page index.
        """
        results_len = len(self._results_page_)
        if not widget:
            if results_len < 1:
                self.__goto_search__()
                return False
        elif widget.label == 'Previous':
            self._current_page_ -= 1
            if self._current_page_ < 0:
                self._current_page_ = 0
        elif widget.label == 'Next':
            self._current_page_ += 1
            last_page = results_len - 1
            if self._current_page_ > last_page:
                self._current_page_ = last_page
        results = self._results_page_[self._current_page_]
        self.__generate_html__(results, self._search_html_path_)
        self.__goto_search__()
        return False

    def __generate_html__(self, lexical_units, document_path):
        entry = '<{1} style="text-align:right;white-space:nowrap;color:{2};'
        entry += 'padding-left:5;padding-right:5" scope="row">{0}</{1}>'
        html_doc = '<html><body><table><tbody>'
        s = self._screen_settings_._settings_.values()
        t = [v['toggled'] for v in s]
        c = [v['color'] for v in s]
        for e in lexical_units:
            k, v = e[0], e[1]
            html_doc += '<tr>'
            html_doc += entry.format(k, 'th', 'black')
            for i in range(len(v)):
                if t[i]:
                    html_doc += entry.format(v[i], 'td', c[i])
            html_doc += '</tr>'
        html_doc += '</tbody></table></body></html>'
        with open(document_path, 'w+') as f:
            f.write(html_doc)

    def __load_json__(self, file_path):
        result = dict()
        if exists(file_path):
            with open(file_path, 'r') as f:
                result = dict(json.load(f))
        return result

    def __save_json__(self, file_path, data):
        with open(file_path, 'w+') as f:
            json.dump(data, f)

    def __goto_home__(self, *ignore):
        self._screen_home_ = HomeScreen(self)
        self.main_window.content = self._screen_home_

    def __goto_search__(self, *ignore):
        self._screen_search_ = SearchScreen(self, self._search_html_path_)
        self.main_window.content = self._screen_search_

    def __goto_settings__(self, *ignore):
        self._screen_settings_ = SettingsScreen(self)
        self.main_window.content = self._screen_settings_

    def __goto_info__(self, *ignore):
        self._screen_info_ = InfoScreen(self)
        self.main_window.content = self._screen_info_

    def __goto_loading__(self, *ignore):
        self._screen_loading_ = LoadingScreen(self, 'Searching...')
        self.main_window.content = self._screen_loading_

    def startup(self):
        self._entry_headers_ = [
            'Standard', 'Reverse Standard',
            'Reduction', 'Reverse Reduction',
            'Sumerian', 'Reverse Sumerian',
            'Jewish', 'Reverse Jewish',
            'Fibonacci', 'Reverse Fibonacci'
            ]
        self._search_term_ = ''
        self._search_values_ = list()
        self._results_page_ = list()
        self._current_page_ = 0
        self._display_lexical_units_ = 250
        self._absolute_path_ = abspath(dirname(realpath(__file__)))
        self._resources_path_ = f'{self._absolute_path_}/resources'
        self._search_html_path_ = f'{self._resources_path_}/search_screen.html'
        self._lexicon_path_ = f'{self._resources_path_}/lexicon.json'
        self._cmd_home_ = Command(
            self.__goto_home__,
            'Home',
            tooltip='Switch to home screen',
            icon='resources/icons/home.png',
            group=Group.WINDOW,
            section=0,
            order=0
            )
        self._cmd_search_ = Command(
            self.__goto_search__,
            'Search',
            tooltip='Switch to search screen',
            icon='resources/icons/search.png',
            group=Group.WINDOW,
            section=0,
            order=1
            )
        self._cmd_settings_ = Command(
            self.__goto_settings__,
            'Settings',
            tooltip='Switch to settings screen',
            icon='resources/icons/settings.png',
            group=Group.WINDOW,
            section=0,
            order=2
            )
        self._cmd_info_ = Command(
            self.__goto_info__,
            'Info',
            tooltip='Switch to info screen',
            icon='resources/icons/info.png',
            group=Group.WINDOW,
            section=0,
            order=3
            )
        self._screen_loading_ = LoadingScreen(self, 'Loading the lexicon...')
        self._screen_settings_ = SettingsScreen(self)
        self._screen_search_ = SearchScreen(self, self._search_html_path_)
        self._screen_info_ = InfoScreen(self)
        self._screen_home_ = HomeScreen(self)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.toolbar.add(
            self._cmd_home_,
            self._cmd_search_,
            self._cmd_settings_,
            self._cmd_info_
            )
        self.main_window.content = self._screen_loading_
        self._await_thread_ = self.add_background_task(self.__await_lexicon__)


def main():
    return GematriaApp()
