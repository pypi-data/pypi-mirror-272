# This file is part of hfive, a simple HDF5 viewer for the terminal.
#
# https://gitlab.com/zrlf/hfive
#
# Copyright 2024 Flavio Lorez and contributors
#
# There is no warranty for this code

from typing import Callable, Dict, List, Tuple

import urwid


# ----------------------------------------
# Main loop holder and widget stack
# ----------------------------------------
class Caller:
    """Caller is a class that holds the main loop and the widget stack. It
    provides a way to enter and exit widgets from the stack.
    """

    widget_stack = []
    main_loop: urwid.MainLoop = None

    @classmethod
    def enter_widget(cls, widget: urwid.Widget):
        """Enters a new widget into the widget stack and sets it as the main
        widget in the main loop.

        Parameters:
            - widget (urwid.Widget): The widget to enter into the widget stack.
        """
        cls.widget_stack.append(widget)
        cls.main_loop.widget = widget

    @classmethod
    def exit_widget(cls):
        """Exits the current widget by removing it from the widget stack and
        setting the previous widget as the main widget in the main loop.

        Raises:
            - urwid.ExitMainLoop: If there are no more widgets in the stack,
              raises an ExitMainLoop exception to exit the main loop.
        """
        if len(cls.widget_stack) <= 1:
            raise urwid.ExitMainLoop()
        cls.widget_stack.pop()
        cls.main_loop.widget = cls.widget_stack[-1]

# If a Caller is present from the parent bamboost cli, use it. 
# It uses the urwid namespace as this is the only way I know currently to share
# the Caller object
try:
    Caller = urwid.Caller
except AttributeError:
    pass


# ----------------------------------------
# Type definitions
# ----------------------------------------
Keybinds = Dict[str, Tuple[Callable, str, List[str]]]


# ----------------------------------------
# COLOR PALETTE
# ----------------------------------------
# 1-16: standard colors
color_map = {
    1: "black",
    2: "dark red",
    3: "dark green",
    4: "brown",  # or 'yellow' for some terminals that treat this as yellow/brown/orange
    5: "dark blue",
    6: "dark magenta",
    7: "dark cyan",
    8: "light gray",
    9: "dark gray",
    10: "light red",
    11: "light green",
    12: "yellow",  # or 'brown' if the terminal uses yellow for color 4
    13: "light blue",
    14: "light magenta",
    15: "light cyan",
    16: "white",
}

palette = [
    ("selected", "standout", ""),
    ("bold", "bold", ""),
    ("boldselected", "standout,bold", ""),
    ("footer", color_map[2], ""),
    ("green_box", color_map[6], ""),
    ("default text", color_map[2], ""),
    ("failed", "dark red", ""),
    ("success", "dark green", ""),
]

# Add default colors to palette 1-16
palette.extend([(str(num), "", "", "", color_map[num], "") for num in color_map])

# bold
palette.extend([(f"{num}-bold", "", "", "", f"{color_map[num]},bold", "") for num in color_map])

# reverse
palette.extend([(f"{num}-reverse", "black", color_map[num]) for num in color_map])

# bold-reverse
palette.extend([(f"{num}-reverse-bold", "black,bold", f"{color_map[num]}") for num in color_map])

# on-white
palette.extend(
    [
        (f"{num}-on-white", f"{color_map[num] if num<=8 else color_map[num-8]}", "white")
        for num in color_map
    ]
)

# bold-on-white
palette.extend(
    [
        (
            f"{num}-bold-on-white",
            f"{color_map[(num-1) % 8 + 1]},bold",
            "white",
            "",
            f"{color_map[(num-1) % 8 + 1]},bold",
            "h15",
        )
        for num in color_map
    ]
)
