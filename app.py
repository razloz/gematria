"""
Gematria Calc
"""
import toga
import testapp.gematria
from toga import App, MainWindow, Box, TextInput, DetailedList, Button, Label, Switch
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from testapp.gematria import full_test, numerology, get_lexicon
BASE_LEXICON = get_lexicon(1)


class TestApp(App):
    def do_search(self, *args):
        """
        Check lexicon for word or phrase.
        """
        numeric_search = False
        search_value = str(self.search_box.value)
        lexicon_keys = BASE_LEXICON.keys()
        if search_value.isnumeric():
            search_term = int(search_value)
            search_results = None
            numeric_search = True
        else:
            search_term = search_value.upper()
            if search_term in lexicon_keys:
                search_results = BASE_LEXICON[search_term]
            else:
                search_results = full_test(search_term, 1)
        data_entry = {
            'icon': None,
            'title': '[Standard, Reverse Standard, Reduction, Reverse Reduction]',
            'subtitle': '',
        }
        results_data = [dict(**data_entry)]
        if not numeric_search:
            data_entry['title'] = search_term
            data_entry['subtitle'] = f'{search_results}'
            results_data.append(dict(**data_entry))
        matched_words = list()
        toggle_check = [
            self.toggle_1st.is_on, self.toggle_2nd.is_on,
            self.toggle_3rd.is_on, self.toggle_4th.is_on
        ]
        if any(toggle_check):
            for key in lexicon_keys:
                matched = False
                lexicon_entry = BASE_LEXICON[key]
                for i in range(4):
                    if toggle_check[i] and not matched:
                        if not numeric_search:
                            if lexicon_entry[i] == search_results[i]:
                                matched = True
                        else:
                            if lexicon_entry[i] == search_term:
                                matched = True
                if matched:
                    matched_words.append(key)
        for word in matched_words:
            lexicon_entry = BASE_LEXICON[word]
            data_entry['title'] = word
            data_entry['subtitle'] = f'{lexicon_entry}'
            results_data.append(dict(**data_entry))
        print(f'*** Results Data: {results_data}')
        self.results_list.data = results_data

    def startup(self):
        """
        Attempt to build and show the application.
        """
        ### Style Stuff ###
        SRP = Pack(direction=ROW, padding=5)
        SCP = Pack(direction=COLUMN, padding=5)
        SFP = Pack(flex=1, padding=5)

        ### Search View ###
        self.search_box = TextInput(style=SFP)
        self.search_but = Button(label='Search', on_press=self.do_search, style=SRP)
        self.toggle_1st = Switch('1st')
        self.toggle_2nd = Switch('2nd')
        self.toggle_3rd = Switch('3rd')
        self.toggle_4th = Switch('4th')
        tb = [self.toggle_1st, self.toggle_2nd, self.toggle_3rd, self.toggle_4th]
        btb = Box(children=tb, style=SRP)
        sb = Box(children=[self.search_box, self.search_but], style=SRP)
        #h = ['Standard', 'Reverse', 'Reduce', 'Reverse Reduce', 'Word']
        self.results_list = DetailedList(style=SFP)
        self.search_view = Box(children=[btb, sb, self.results_list], style=SCP)

        ### Main Window ###
        self.main_window = MainWindow(title=self.formal_name)
        self.main_window.content = self.search_view
        self.main_window.show()


def main():
    """
    Start the application.
    """
    return TestApp()
