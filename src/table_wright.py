from toga import WebView
TABLE_HEADER = '<{1} colspan="{2}" style="text-align:left;white-space:nowrap;'
TABLE_HEADER += 'padding-top:5;padding-left:5;padding-right:5">{0}</{1}>'
TABLE_ENTRY = '<{1} style="text-align:right;white-space:nowrap;color:{2};'
TABLE_ENTRY += 'padding-left:5;padding-right:5" scope="row">{0}</{1}>'


class TableWright(WebView):
    def __init__(self, root_app):
        super().__init__()
        self._root_app_ = root_app
        self.build_table()

    def build_table(self):
        lexical_units = list(self._root_app_._lexical_units_)
        lexical_units.insert(0, self._root_app_._search_unit_)
        s = self._root_app_._screen_settings_._settings_.values()
        t = [v['toggled'] for v in s]
        c = [v['color'] for v in s]
        toggled = sum([1 if v else 0 for v in t])
        html_doc = '<html><body>'
        if toggled > 0 and len(lexical_units) > 0:
            html_doc += '<table><tbody>'
            for e in lexical_units:
                k, v = e[0], e[1]
                header = TABLE_HEADER.format(k, 'th', toggled)
                html_doc += f'<tr>{header}</tr><tr>'
                for i in range(len(t)):
                    if t[i]:
                        html_doc += TABLE_ENTRY.format(v[i], 'td', c[i])
                html_doc += '</tr>'
            html_doc += '</tbody></table>'
        html_doc += '</body></html>'
        self.set_content(None, html_doc)
