# This file is part of hfive, a simple HDF5 viewer for the terminal.
#
# https://gitlab.com/zrlf/hfive
#
# Copyright 2024 Flavio Lorez and contributors
#
# There is no warranty for this code

from typing import Iterable, List, Union

import urwid

from hfive.common import Caller, Keybinds


class SelectionIcon(urwid.Text):
    SELECT_CHARACTER = "❯"

    def __init__(self):
        super().__init__(self.SELECT_CHARACTER, align="center")

    def render(self, size, focus=False):
        if focus:
            self.set_text(("4", self.SELECT_CHARACTER))
        else:
            self.set_text(" ")
        return super().render(size, focus)


class cRoundedLineBox(urwid.AttrWrap):
    def __init__(self, *args, attr_map=None, focus_map=None, **kwargs):
        self.widget = urwid.LineBox(
            *args,
            tlcorner=urwid.LineBox.Symbols.LIGHT.TOP_LEFT_ROUNDED,
            trcorner=urwid.LineBox.Symbols.LIGHT.TOP_RIGHT_ROUNDED,
            blcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_LEFT_ROUNDED,
            brcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_RIGHT_ROUNDED,
            **kwargs,
        )
        if attr_map is None:
            attr_map = "default"
        if focus_map is None:
            focus_map = "green_box"
        super().__init__(self.widget, attr_map, focus_map)

    def __getattr__(self, name: str):
        return self.widget.base_widget.__getattribute__(name)

    def keypress(self, size: tuple[()] | tuple[int] | tuple[int, int], key: str) -> str | None:
        return super().keypress(size, key)


class cEdit(urwid.Edit):
    def __init__(self, *args, callback: callable = None, **kwargs):
        self.callback = callback
        super().__init__(*args, **kwargs)

    def keypress(self, size: tuple, key: str) -> Union[str, None]:
        if key == "meta backspace":
            # Logic to delete the word before the cursor
            new_pos = (
                self.edit_text.rfind(" ", 0, self.edit_pos - 1) + 1 if self.edit_pos > 0 else 0
            )
            new_text = self.edit_text[:new_pos] + self.edit_text[self.edit_pos :]
            self.set_edit_text(new_text)
            self.set_edit_pos(new_pos)
        elif key == "esc":
            Caller.exit_widget()
        elif key == "enter":
            if self.callback is not None:
                self.callback(self.edit_text)
                return
            return super().keypress(size, key)

        else:
            return super().keypress(size, key)


class cListBox(urwid.ListBox):
    _sizing = frozenset(["box", "flow"])

    def __init__(self, *args, wrap: bool = False, keymap_jk: bool = False, **kwargs):
        self.wrap = wrap
        self.keymap_jk = keymap_jk
        super().__init__(*args, **kwargs)

        self.keys = {
            "j": (self._navigate_down, "Move down", ["ctrl n"]),
            "k": (self._navigate_up, "Move up", ["ctrl p"]),
        }

    def _navigate_down(self, *args) -> None:
        try:
            self.set_focus(self.focus_position + 1, "above")
        except IndexError:
            pass

    def _navigate_up(self, *args) -> None:
        try:
            self.set_focus(self.focus_position - 1, "below")
        except IndexError:
            pass

    def rows(self, size, focus):
        return len(self.body)

    @property
    def keybinds(self) -> dict:
        if not hasattr(self, "__keybinds"):
            self.__keybinds = dict(
                **self.keys,
                **{
                    alias: (func, desc, aliases)
                    for func, desc, aliases in self.keys.values()
                    for alias in aliases
                },
            )
        return self.__keybinds

    @property
    def focused_text(self) -> str:
        return self.get_focus()[0].base_widget.text

    def keypress(self, size: tuple, key: str) -> Union[str, None]:
        if key == "?":
            if not hasattr(self, "_help_widget"):
                self._help_widget = cKeybindsOverlay(Caller.main_loop, self.keys)
            self._help_widget.toggle()
            return

        if key in self.keybinds:
            return self.keybinds[key][0](size, key)
        return super().keypress(size, key)


class cKeybindsOverlay(urwid.Frame):
    """Displays the keybindings in an overlay

    Args:
        main_loop (urwid.MainLoop): The main loop (Caller.main_loop)
        keybinds (Keybinds): The keybindings to be displayed
    """

    _sizing = frozenset(["box"])

    def __init__(self, main_loop: urwid.MainLoop, keybinds: Keybinds, *args, **kwargs):
        self.main_loop = main_loop
        self.bottom_w = main_loop.widget
        self.keybinds: Keybinds = keybinds
        self.is_visible: bool = False
        self.longest_key = max(len(key) for key in keybinds.keys())
        self.list_entries = [
            urwid.Columns(
                [
                    (self.longest_key, urwid.Text(("3-bold", key), align="right")),
                    urwid.Text([("", desc), ("9", "\n" + ", ".join(aliases) if aliases else "")]),
                ],
                dividechars=2,
            )
            for key, (_, desc, aliases) in self.keybinds.items()
        ]
        self.box = cRoundedLineBox(
            urwid.Pile(self.list_entries), focus_map="3", title="Keybinds", title_align="left"
        )
        self.overlay = urwid.Overlay(
            self.box,
            self.bottom_w,
            align="left",
            width="pack",
            valign="bottom",
            height="pack",
            bottom=1,
        )
        super().__init__(self.overlay, *args, **kwargs)

    def toggle(self) -> None:
        if self.is_visible:
            self.main_loop.widget = self.bottom_w
            self.is_visible = False
        else:
            self.main_loop.widget = self
            self.is_visible = True

    def keypress(self, size: tuple[()] | tuple[int] | tuple[int, int], key: str) -> str | None:
        if key in ("esc", "q"):
            # Set the widget of loop back to the original widget
            return self.toggle()

        return self.bottom_w.keypress(size, key)


class cConfirmDialog(urwid.Frame):
    """A dialog box for confirming an action.

    Args:
        - main_loop (urwid.MainLoop): The main loop (Caller.main_loop)
        - text (str): The text to display in the dialog box.
        - callback (callable): The callback function to be called when the "Yes"
          button is pressed.
    """

    _selectable = True

    def __init__(self, main_loop: urwid.MainLoop, text: str, callback: callable, *args, **kwargs):
        self.main_loop = main_loop
        self.bottom_w = main_loop.widget
        self.text = text
        self.callback = callback
        self.yes_button = urwid.Button("Yes", on_press=self.yes)
        self.no_button = urwid.Button("No", on_press=self.no)
        self.buttons = urwid.Columns([self.no_button, self.yes_button], dividechars=2)
        self.box = cRoundedLineBox(
            urwid.Pile([urwid.Text(text), self.buttons]), focus_map="2", title="Confirmation"
        )
        self.overlay = urwid.Overlay(
            self.box,
            self.bottom_w,
            align="center",
            width="pack",
            valign="middle",
            height="pack",
        )
        super().__init__(self.overlay, *args, **kwargs)

    def yes(self, button: urwid.Button) -> None:
        Caller.exit_widget()
        self.callback()
        return

    def no(self, button: urwid.Button) -> None:
        Caller.exit_widget()
        return

    def keypress(self, size: tuple[()] | tuple[int] | tuple[int, int], key: str) -> str | None:
        if key in ("esc", "q"):
            # Set the widget of loop back to the original widget
            Caller.exit_widget()
            return
        if key == "l":
            return super().keypress(size, "right")
        if key == "h":
            return super().keypress(size, "left")

        return super().keypress(size, key)


class cActionItem(urwid.Widget):
    """A custom widget class for action items in an Urwid application.

    Args:
        - content (str | Iterable): The content to be displayed in the widget.
          Can be a list of strings.
        - callback (callable, optional): The callback function to be called
          when the widget is activated. The callback function takes the widget
          as an argument.
    """

    _sizing = frozenset(["box"])
    _selectable = True
    signals = ["set_footer"]

    def __init__(self, content: Union[str, Iterable], callback: callable = None) -> None:
        self.content = [content] if isinstance(content, str) else content
        self._callback = callback
        self.column_widths = {}
        self.column_attr_map = {None: "default"}
        self.column_focus_map = {None: "bold"}

        super().__init__()

    def _invalidate(self):
        self.widget = urwid.AttrMap(
            urwid.Columns(
                [("fixed", 1, SelectionIcon())]
                + [self._render_column(i, text) for i, text in enumerate(self.content)],
                dividechars=2,
            ),
            self.column_attr_map,
            self.column_focus_map,
        )
        return super()._invalidate()

    def rows(self, size, focus):
        return self.widget.rows(size, focus)

    def callback(self) -> callable:
        return self._callback(self) or (lambda *args: None)

    def keypress(self, size, key):
        if key == "enter":
            self.callback()
            return
        return key

    @property
    def widget(self) -> urwid.Columns:
        return self._widget

    @widget.setter
    def widget(self, value: urwid.Columns) -> None:
        self._widget = value

    def render(self, size, focus=False):
        # Before render, the rows() method is called by urwid!
        # Therefore, we don't need to update the widget here again but only in rows()
        return self.widget.render(size, focus)

    def _render_column(self, i: int, text: str, focus: bool = False):
        if i == 0 and self.column_widths:
            return ("fixed", self.column_widths[i], urwid.AttrMap(urwid.Text(text), i))

        return ("weight", 1, urwid.AttrMap(urwid.Text(text), i))


class cListBoxSelectionCharacter(cListBox):
    """A custom list box widget for selecting from a list of items with a focus
    character.

    Args:
        - items (List[cActionItem]): A list of cActionItem objects representing
          the items in the list box.
        - attr_map (List[Tuple[str]]): A list of tuples specifying the
          attribute mappings for columns. Defaults to None.

    Attributes:
        - _column_widths (Dict[int, int]): A dictionary mapping column index to
          the width of the longest content in that column. items
          (List[cActionItem]): A list of cActionItem objects representing the
          items in the list box.
        - _listwalker (urwid.SimpleFocusListWalker): A SimpleFocusListWalker
          object for navigating the list items.
    """

    def __init__(
        self,
        items: List[cActionItem],
        attr_map: dict = None,
        focus_map: dict = None,
        *args,
        **kwargs,
    ):
        # get the length of the longest key per column
        self._column_widths = {}
        for item in items:
            if isinstance(item.content, str):
                item.content = [item.content]
            for i, content in enumerate(item.content):
                self._column_widths[i] = max(self._column_widths.get(i, 0), len(str(content)))

        for item in items:
            item.column_widths = self._column_widths
            if attr_map:
                item.column_attr_map = attr_map
            if focus_map:
                item.column_focus_map = focus_map
            item._invalidate()

        self.items = items
        self._listwalker = urwid.SimpleFocusListWalker(self.items)
        super().__init__(self._listwalker, *args, **kwargs, keymap_jk=True)

    def keypress(self, size: tuple[int], key: str) -> Union[str, None]:
        return super().keypress(size, key)


class cPopup(urwid.Overlay):

    def __init__(self, widget: urwid.Widget, *args, **kwargs):
        """A custom Popup widget with a title, frame and footer.

        Args:
            - widget (urwid.Widget): The main widget to display in the popup.
            - *args: Additional positional arguments.
            - **kwargs: Additional keyword arguments.

        Keyword Arguments:
            - height (int): The height of the popup.
            - footer (str): The text to display in the footer.
            - align (str): The alignment of the popup.
            - width (tuple[str, int]): The width of the popup.
            - valign (str): The vertical alignment of the popup.
            - min_height (int): The minimum height of the popup.
            - title (str): The title of the popup.
            - title_align (str): The alignment of the title.
            - focus_map (str): The focus map for the popup.
        """

        if "height" in kwargs:
            if isinstance(kwargs["height"], int):
                kwargs["height"] += 4

        kwargs.setdefault("footer", "Enter: Open | Esc: Close")
        kwargs.setdefault("align", "center")
        kwargs.setdefault("width", ("relative", 80))
        kwargs.setdefault("valign", "middle")
        kwargs.setdefault("height", ("relative", 50))
        kwargs.setdefault("min_height", 5)
        kwargs.setdefault("title", "")
        kwargs.setdefault("title_align", "left")
        kwargs.setdefault("focus_map", "8")

        self._widget = widget

        box = cRoundedLineBox(
            urwid.Frame(
                urwid.Padding(widget, left=1, right=1),
                footer=urwid.Pile(
                    [
                        urwid.Divider("\u2500"),
                        urwid.Padding(urwid.Text(("2", kwargs.pop("footer"))), left=1, right=1),
                    ]
                ),
                focus_part="body",
            ),
            title=kwargs.pop("title"),
            title_align=kwargs.pop("title_align"),
            focus_map=kwargs.pop("focus_map"),
        )

        base_widget = Caller.main_loop.widget if Caller.main_loop else urwid.SolidFill(" ")

        super().__init__(box, base_widget, *args, **kwargs)

    def keypress(self, size: tuple[int, int], key: str) -> str | None:
        return super().keypress((1,), key)


class FocusedList(urwid.ListBox):
    """List box with a focused item even if the list is not in focus."""

    def render(self, size, focus=False):
        return super().render(size, focus=True)
