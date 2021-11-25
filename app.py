"""
Gematria Calc
"""
import toga
import testapp.gematria
from toga import App, Box, TextInput, Table, DetailedList, MainWindow
from toga import Button, ScrollContainer, NumberInput, Label
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from testapp.gematria import full_test, numerology, get_lexicon
BASE_LEXICON = get_lexicon(1)


# Main application
class TestApp(App):
    def do_search(self, *args):
        search_term = str(self.search_box.value).upper()
        lexicon_keys = BASE_LEXICON.keys()
        if search_term in lexicon_keys:
            search_results = BASE_LEXICON[search_term]
        else:
            search_results = full_test(search_term, 1)
        results_data = [[*search_results, search_term]]
        matched_words = list()
        for key in lexicon_keys:
            matches = 0
            lexicon_entry = BASE_LEXICON[key]
            if lexicon_entry[0] == search_results[0]: matches += 1
            if lexicon_entry[1] == search_results[1]: matches += 1
            if lexicon_entry[2] == search_results[2]: matches += 1
            if lexicon_entry[3] == search_results[3]: matches += 1
            if matches >= self.matches_select.value: matched_words.append(key)
        for word in matched_words:
            results_data.append([*BASE_LEXICON[word], word])
        self.results_table.data = results_data
    def startup(self):
        """
        Attempt to build and show the application.
        """
        ### Style Stuff ###
        SRP = Pack(direction=ROW, padding=5)
        SCP = Pack(direction=COLUMN, padding=5)
        SFP = Pack(flex=1, padding=5)

        ### Search Window ###
        self.search_box = TextInput(style=SFP)
        self.search_but = Button(label='Search', style=SRP)
        self.search_but.on_press = self.do_search
        self.matches_select = NumberInput(step=1, min_value=1, max_value=4, style=SRP)
        self.matches_select.value = 4
        sb = Box(children=[self.search_box, self.matches_select, self.search_but], style=SRP)
        h = ['Standard', 'Reverse Standard', 'Full Reduction', 'Reverse Full Reduction', 'Word']
        self.results_table = Table(headings=h, style=SFP)
        #rt = ScrollContainer(style=SFP, horizontal=False, vertical=True)
        self.search_view = Box(children=[sb, self.results_table], style=SCP)

        ### Filter Window ###
        self.favorites_list = DetailedList()
        self.words_list = DetailedList()
        self.hidden_list = DetailedList()
        layout = [self.favorites_list, self.words_list, self.hidden_list]
        self.filter_view = Box(children=layout)

        ### Main Window ###
        self.search_window = MainWindow(title='Gematria Lookup')
        self.search_window.content = self.search_view
        self.windows += self.search_window
        self.filter_window = MainWindow(title='Word Filter')
        self.filter_window.content = self.filter_view
        self.windows += self.filter_window
        self.main_window = self.search_window
        self.main_window.show()


def main():
    return TestApp()
