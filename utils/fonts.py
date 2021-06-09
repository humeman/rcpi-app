
from kivy.core.text import LabelBase

# Using some janky code to register different font weights.
# Can't find a better way.


fonts = {
    "main": {
        "fn_regular": "fonts/rubik/Rubik-Regular.ttf",
        "fn_bold": "fonts/rubik/Rubik-SemiBold.ttf",
        "fn_italic": "fonts/rubik/Rubik-Italic.ttf",
        "fn_bolditalic": "fonts/rubik/Rubik-SemiBoldItalic.ttf"
    },
    "title": {
        "fn_regular": "fonts/rubik/Rubik-Black.ttf",
        "fn_bold": "fonts/rubik/Rubik-Black.ttf", 
        "fn_italic": "fonts/rubik/Rubik-BlackItalic.ttf",
        "fn_bolditalic": "fonts/rubik/Rubik-BlackItalic.ttf"
    },
    "monospace": {
        "fn_regular": "fonts/robotomono/RobotoMono-Regular.ttf",
        "fn_bold": "fonts/robotomono/RobotoMono-SemiBold.ttf",
        "fn_italic": "fonts/robotomono/RobotoMono-Italic.ttf",
        "fn_bolditalic": "fonts/robotomono/RobotoMono-SemiBoldItalic.ttf"
    },
    "fa": {
        "fn_regular": "fonts/fa-solid-900.ttf"
    }
}
"""
fonts = {
    "main": {
        "fn_regular": "fonts/cs.ttf"
    },
    "title": {
        "fn_regular": "fonts/cs.ttf"
    },
    "monospace": {
        "fn_regular": "fonts/cm.ttf"
    },
    "fa": {
        "fn_regular": "fonts/fa-solid-900.ttf"
    }
}
"""


def register():
    for name, kwargs in fonts.items():
        LabelBase.register(
            name = name,
            **kwargs
        )