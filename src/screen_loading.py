from toga import Box, Label, ImageView
from toga.images import Image
from toga.style import Pack
from toga.style.pack import COLUMN


class LoadingScreen(Box):
    def __init__(self, root_app, display_text):
        self._root_app_ = root_app
        self._image_path_ = f'{root_app._resources_path_}/gematria_flat.png'
        super().__init__(
            id='screen_loading',
            style=Pack(direction=COLUMN),
            children=[
                Label(
                    display_text,
                    style=Pack(
                        font_size=21,
                        flex=1,
                        text_align='center',
                        alignment='bottom'
                        )
                    ),
                ImageView(
                    image=Image(self._image_path_),
                    id='splash_image',
                    style=Pack(
                        flex=8,
                        text_align='center',
                        alignment='center'
                        )
                    ),
                Label(
                    '''https://github.com/razloz/gematria''',
                    style=Pack(
                        font_size=21,
                        flex=1,
                        text_align='center',
                        alignment='top'
                        )
                    )
                ]
            )
