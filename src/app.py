"""
Gematria Calc
"""
import toga
import gematria.gematria as gem
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
WORDS_HIDDEN = gem.get_hidden()
WORDS_FAVORITE = gem.get_favorite()
WORDS_LEXICON = gem.get_lexicon()
SRP = Pack(direction=ROW, padding=5)
SCP = Pack(direction=COLUMN, padding=5)
SFP = Pack(flex=1, padding=5)
HEADER_INFO = """
Values in order:
    [
        standard, rev_standard,
        reduction, rev_reduction,
        sumerian, rev_sumerian,
        jewish, rev_jewish,
        fib, rev_fib
    ]
"""


class GematriaApp(toga.App):
    def do_search(self, *args):
        """
        Check lexicon for word or phrase.
        """
        search_value = str(self.search_box.value)
        cat_words = dict(WORDS_FAVORITE)
        cat_words.update(WORDS_LEXICON)
        lexicon_keys = cat_words.keys()
        new_entry = False
        numeric_search = search_value.isnumeric()
        if numeric_search:
            search_term = int(search_value)
            search_results = None
        else:
            search_term = search_value.upper()
            if search_term in lexicon_keys:
                search_results = cat_words[search_term]
            else:
                search_results = gem.full_test(search_term)
                new_entry = True
        toggle_check = [
            self.opt_1st.is_on, self.opt_2nd.is_on,
            self.opt_3rd.is_on, self.opt_4th.is_on,
            self.opt_5th.is_on, self.opt_6th.is_on,
            self.opt_7th.is_on, self.opt_8th.is_on,
            self.opt_9th.is_on, self.opt_10th.is_on,
            ]
        results_data = HEADER_INFO
        toggle_len = len(toggle_check)
        full_check = range(toggle_len)
        if not numeric_search:
            results_data += f'\n{search_term}:\n{search_results}\n'
        matched_words = list()
        match_all = self.match_all.is_on
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
                tc = len(toggle_check)
                matches = 0
                for i in range(tc):
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
            m = -1
            if numeric_search:
                for i in full_check:
                    if lexicon_entry[i] == search_term:
                        m += 1
            else:
                for i in full_check:
                    if lexicon_entry[i] == search_results[i]:
                        m += 1
            sorted_results[m].append((word, lexicon_entry))
        for i in full_check:
            p = (toggle_len - 1) - i
            for e in sorted_results[p]:
                results_data += f'\n{e[0]}:\n{e[1]}\n'
        self.results_list.value = results_data
        if new_entry:
            WORDS_FAVORITE[search_term] = search_results
            gem.save_favorite(WORDS_FAVORITE)

    def goto_search(self, *ignore):
        """
        Switch to search view.
        """
        self.main_tools = toga.Box(style=SRP, children=[
            toga.Button(style=SFP, label='Settings', on_press=self.goto_settings),
            toga.Button(style=SFP, label='Lexicon', on_press=self.goto_lexicon)
            ])
        self.search_box = toga.TextInput(style=SFP)
        self.sb = toga.Button(style=SRP, label='Search', on_press=self.do_search)
        self.sbb = toga.Box(style=SRP, children=[self.search_box, self.sb])
        self.results_list = toga.MultilineTextInput(style=SFP, readonly=True)
        self.search_view = toga.Box(style=SCP, children=[self.sbb, self.results_list])
        self.main_window.content = toga.Box(style=SCP, children=[
            self.main_tools,
            self.search_view
            ])

    def goto_settings(self, *ignore):
        """
        Switch to settings view.
        """
        self.settings_tools = toga.Box(style=SRP, children=[
            toga.Button(style=SFP, label='Lookup', on_press=self.goto_search),
            toga.Button(style=SFP, label='Lexicon', on_press=self.goto_lexicon)
            ])
        self.match_all = toga.Switch('Match All', style=SFP)
        self.opt_1st = toga.Switch('Standard', style=SFP)
        self.opt_2nd = toga.Switch('Reverse Standard', style=SFP)
        self.opt_3rd = toga.Switch('Reduction', style=SFP)
        self.opt_4th = toga.Switch('Reverse Reduction', style=SFP)
        self.opt_5th = toga.Switch('Sumerian', style=SFP)
        self.opt_6th = toga.Switch('Reverse Sumerian', style=SFP)
        self.opt_7th = toga.Switch('Jewish', style=SFP)
        self.opt_8th = toga.Switch('Reverse Jewish', style=SFP)
        self.opt_9th = toga.Switch('Fibonacci', style=SFP)
        self.opt_10th = toga.Switch('Reverse Fibonacci', style=SFP)
        self.box_1 = toga.Box(style=SRP, children=[self.match_all])
        self.box_2 = toga.Box(style=SRP, children=[self.opt_1st, self.opt_2nd])
        self.box_3 = toga.Box(style=SRP, children=[self.opt_3rd, self.opt_4th])
        self.box_4 = toga.Box(style=SRP, children=[self.opt_5th, self.opt_6th])
        self.box_5 = toga.Box(style=SRP, children=[self.opt_7th, self.opt_8th])
        self.box_6 = toga.Box(style=SRP, children=[self.opt_9th, self.opt_10th])
        self.settings_view = toga.Box(style=SCP, children=[
            self.box_1,
            self.box_2,
            self.box_3,
            self.box_4,
            self.box_5,
            self.box_6
            ])
        self.main_window.content = toga.Box(style=SCP, children=[
            self.settings_tools,
            self.settings_view
            ])

    def goto_lexicon(self, *ignore):
        """
        Switch to lexicon view.
        """
        words_fav = WORDS_FAVORITE.keys()
        words_hid = WORDS_HIDDEN.keys()
        self.lexicon_tools = toga.Box(style=SRP, children=[
            toga.Button(style=SFP, label='Lookup', on_press=self.goto_search),
            toga.Button(style=SFP, label='Settings', on_press=self.goto_settings)
            ])
        self.select_fav = toga.Selection(style=SFP, items=words_fav)
        self.but_fav = toga.Box(style=SRP, children=[
            toga.Button(style=SFP, label='Unfavorite', on_press=self.unfavorite_word),
            toga.Button(style=SFP, label='Delete', on_press=self.delete_favorite)
            ])
        self.box_fav = toga.Box(style=SCP, children=[
            toga.Label('Favorite Words', style=SFP),
            self.select_fav,
            self.but_fav
            ])
        self.select_hid = toga.Selection(style=SFP, items=words_hid)
        self.but_hid = toga.Box(style=SRP, children=[
            toga.Button(style=SFP, label='Unhide', on_press=self.unhide_word),
            toga.Button(style=SFP, label='Delete', on_press=self.delete_hidden)
            ])
        self.box_hid = toga.Box(style=SCP, children=[
            toga.Label('Hidden Words', style=SFP),
            self.select_hid,
            self.but_hid
            ])
        self.lexicon_view = toga.Box(style=SCP, children=[
            self.box_fav,
            self.box_hid
            ])
        self.main_window.content = toga.Box(style=SCP, children=[
            self.lexicon_tools,
            self.lexicon_view
            ])

    def delete_favorite(self, *ignore):
        """
        Delete word from favorites.
        """
        selected_word = str(self.select_fav.value)
        if selected_word in WORDS_FAVORITE.keys():
            del WORDS_FAVORITE[selected_word]
            gem.save_favorite(WORDS_FAVORITE)
            self.select_fav.items = WORDS_FAVORITE.keys()

    def delete_hidden(self, *ignore):
        """
        Delete word from hidden.
        """
        selected_word = str(self.select_hid.value)
        if selected_word in WORDS_HIDDEN.keys():
            del WORDS_HIDDEN[selected_word]
            gem.save_hidden(WORDS_HIDDEN)
            self.select_hid.items = WORDS_HIDDEN.keys()

    def unfavorite_word(self, *ignore):
        """
        Move word from favorites to lexicon.
        """
        selected_word = str(self.select_fav.value)
        if selected_word in WORDS_FAVORITE.keys():
            selected_values = WORDS_FAVORITE[selected_word]
            del WORDS_FAVORITE[selected_word]
            WORDS_LEXICON[selected_word] = selected_values
            gem.save_favorite(WORDS_FAVORITE)
            gem.save_lexicon(WORDS_LEXICON)
            self.select_fav.items = WORDS_FAVORITE.keys()

    def unhide_word(self, *ignore):
        """
        Move word from hidden to lexicon.
        """
        selected_word = str(self.select_hid.value)
        if selected_word in WORDS_HIDDEN.keys():
            selected_values = WORDS_HIDDEN[selected_word]
            del WORDS_HIDDEN[selected_word]
            WORDS_LEXICON[selected_word] = selected_values
            gem.save_hidden(WORDS_HIDDEN)
            gem.save_lexicon(WORDS_LEXICON)
            self.select_hid.items = WORDS_HIDDEN.keys()

    def startup(self):
        """
        Attempt to build and show the application.
        """
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.goto_lexicon()
        self.goto_settings()
        self.goto_search()
        self.main_window.show()


def main():
    """
    Start the application.
    """
    return GematriaApp()
