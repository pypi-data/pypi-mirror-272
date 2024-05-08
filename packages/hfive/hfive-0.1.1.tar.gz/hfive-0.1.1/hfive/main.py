# This file is part of hfive, a simple HDF5 viewer for the terminal.
#
# https://gitlab.com/zrlf/hfive
#
# Copyright 2024 Flavio Lorez and contributors
#
# There is no warranty for this code
from __future__ import annotations

import os

import h5py
import numpy as np
import urwid

from hfive.common import Caller, Keybinds, palette
from hfive.widgets import (
    FocusedList,
    SelectionIcon,
    cActionItem,
    cConfirmDialog,
    cEdit,
    cKeybindsOverlay,
    cListBoxSelectionCharacter,
    cPopup,
    cRoundedLineBox,
)


class AttrsList(cListBoxSelectionCharacter):
    def __init__(self, parent: HFive, attr_map: dict = None, focus_map: dict = None):
        self.parent = parent
        self.attr_map = attr_map
        self.focus_map = focus_map

    def update(self, key: str = ""):
        super().__init__(self._get_action_items(key), self.attr_map, self.focus_map)
        return self

    def _get_action_items(self, key: str = ""):
        return [ActionItemPatched(i) for i in self.parent.get_attrs(key)]


class ActionItemPatched(cActionItem):
    def rows(self, size, focus=False):
        # dynamic resize (fixed, weight) of columns based on content
        # rows is called before render, that's why the reconstruction of the widget is done here
        wide = size[0] > self.column_widths[0] * 1.8
        self.widget = urwid.AttrMap(
            urwid.Columns(
                [("fixed", 1, SelectionIcon())]
                + [
                    self._render_column(i, text, focus, wide) for i, text in enumerate(self.content)
                ],
                dividechars=1,
            ),
            self.column_attr_map,
            self.column_focus_map,
        )
        return self.widget.rows(size, focus)

    def render(self, size, focus=False):
        return self.widget.render(size, focus)

    def _render_column(self, i: int, text: str, focus: bool = False, wide: bool = False):
        if i == 0 and self.column_widths and wide:
            return ("fixed", self.column_widths[i], urwid.AttrMap(urwid.Text(text), i))

        return ("weight", 1, urwid.AttrMap(urwid.Text(text), i))


class HFive(urwid.Frame):

    DEFAULT_FOOTER = "q: Quit | ?: Keybindings | tab: Toggle focus"

    def __init__(self, filename: str) -> None:

        self.filename = filename
        self._file_path = os.path.abspath(filename)
        self._current_dir = []
        self._focus_stack = []

        self.current_dir_list = FocusedList(urwid.SimpleFocusListWalker(self.get_items()))
        self.parent_dir_list = FocusedList(urwid.SimpleFocusListWalker([]))
        self.preview = urwid.ListBox(urwid.SimpleListWalker([]))

        # Header: File path, File size, Divider
        file_size = os.path.getsize(self._file_path) / (1024 * 1024)
        self.header = urwid.Pile(
            [
                urwid.AttrWrap(urwid.Text(f"{self._file_path}"), "bold"),
                urwid.AttrWrap(urwid.Text(f"Size: {file_size:.2f} MB"), "8-bold"),
                urwid.Divider(),
            ]
        )
        self.placehold_footer = urwid.AttrWrap(urwid.Text(self.DEFAULT_FOOTER), "footer")

        self.navigator = urwid.Columns(
            [("weight", 1, self.current_dir_list), ("weight", 2, self.preview)],
            dividechars=2,
            focus_column=0,
        )
        self.attrs_focused = AttrsList(
            self, {0: "5", 1: "default"}, {0: "5-bold", 1: "bold"}
        ).update(self.current_dir_list.focus.base_widget.get_text()[0])
        self.attrs_current_dir = AttrsList(
            self, {0: "5", 1: "default"}, {0: "5-bold", 1: "bold"}
        ).update()

        # Layout: Navigator | Attributes of current dir | Attributes of focused item
        self._layout = urwid.Pile(
            [
                ("weight", 2, self.navigator),
                (
                    "weight",
                    1.3,
                    urwid.Columns(
                        [
                            cRoundedLineBox(
                                self.attrs_current_dir,
                                title=f"Attributes of current directory",
                                title_align="left",
                                focus_map="5",
                            ),
                            cRoundedLineBox(
                                self.attrs_focused,
                                title=f"Attributes of selected item",
                                title_align="left",
                                focus_map="5",
                            ),
                        ]
                    ),
                ),
            ],
        )

        super().__init__(
            self._layout,
            header=self.header,
            footer=self.placehold_footer,
            focus_part="body",
        )

        # Add the keybindings
        self.keybinds: Keybinds = {
            "j": (self.navigate_down, "Move focus down", ["ctrl n", "down"]),
            "k": (self.navigate_up, "Move focus up", ["ctrl p", "up"]),
            "l": (self.navigate_enter, "Enter directory", ["enter", "right"]),
            "h": (self.navigate_exit, "Exit directory", ["backspace", "left"]),
            "q": (Caller.exit_widget, "Exit", []),
            "?": (self.show_help, "Show keybindings", []),
            "tab": (self.move_focus, "Move focus between widgets [forwards]", []),
            "shift tab": (
                lambda: self.move_focus(backwards=True),
                "Move focus between widgets [backwards]",
                [],
            ),
            "d": (self.delete_focused, "Delete focused item", []),
            "r": (self.rename_focused, "Rename focused item", []),
        }

    @property
    def _keybinds(self) -> Keybinds:
        try:
            return self.__keybinds
        except AttributeError:
            if hasattr(self, "keybinds"):
                self._keybinds = self.keybinds
                return self._keybinds
            raise AttributeError("Keybinds not set")

    @_keybinds.setter
    def _keybinds(self, keybinds: Keybinds) -> None:
        self.__keybinds = {key: func for key, (func, _, _) in keybinds.items()}
        self.__keybinds.update(
            {alias: func for func, _, aliases in keybinds.values() for alias in aliases}
        )

    def open_file(self, mode: str = "r"):
        return h5py.File(self._file_path, mode)

    @property
    def current_dir(self):
        if not self._current_dir:
            return "/"
        return "/" + "/".join(self._current_dir)

    @property
    def parent_dir(self):
        if len(self._current_dir) <= 1:
            return "/"
        return "/" + "/".join(self._current_dir[:-1])

    def get_attrs(self, key: str):
        with self.open_file("r") as f:
            attrs = f[f"{self.current_dir}/{key}"].attrs
            if not attrs:
                return ["No attributes"]
            return [[str(i), str(j)] for i, j in attrs.items()]

    def get_items(self, dir: str = None):
        if dir is None:
            dir = self.current_dir

        with self.open_file("r") as f:
            grp = f[dir]
            if isinstance(grp, h5py.Group):
                groups = (key for key in grp.keys() if isinstance(grp[key], h5py.Group))
                datasets = (key for key in grp.keys() if isinstance(grp[key], h5py.Dataset))
                g = [urwid.AttrWrap(urwid.Text(key), "5", "5-reverse") for key in groups]
                d = [urwid.AttrWrap(urwid.Text(key), "6", "6-reverse") for key in datasets]
                return g + d
            elif isinstance(grp, h5py.Dataset):
                return []
            else:
                return []

    def set_preview(self, key: str = None):
        if key is None:
            key = self.current_dir_list.focus.base_widget.get_text()[0]

        with self.open_file("r") as f:
            obj = f[f"{self.current_dir}/{key}"]
            if isinstance(obj, h5py.Dataset):

                if obj.dtype == "O":
                    # If the dataset is of type object, try displaying the string
                    # representation of the object
                    preview_data = urwid.Text(obj[()].decode("utf-8"))
                else:
                    # Assume it is a numeric dataset and display the first 20 rows
                    try:
                        preview_data = urwid.Columns(
                            [
                                ("fixed", 9, urwid.Text("Preview:")),
                                urwid.Pile(
                                    [
                                        *[
                                            (
                                                urwid.Columns(
                                                    [
                                                        ("fixed", 7, urwid.Text(f"{i:.3f}"))
                                                        for i in row
                                                    ]
                                                )
                                                if isinstance(row, np.ndarray)
                                                else urwid.Text(f"{row:.3f}")
                                            )
                                            for row in obj[:20]
                                        ],
                                        (
                                            urwid.Text("...")
                                            if obj.shape[0] > 20
                                            else urwid.Text("")
                                        ),
                                    ]
                                ),
                            ]
                        )
                    except:
                        preview_data = urwid.Text(
                            str(obj[:20]) + ("..." if obj.shape[0] > 20 else "")
                        )

                # Construct the preview list with the items
                self.preview.body = urwid.SimpleListWalker(
                    [
                        urwid.Text(("6-bold", f"{self.current_dir}/{key}"), wrap="clip"),
                        urwid.Divider(),
                        urwid.Text(
                            ["Shape:   ", ("bold", f"{obj.shape}")],
                            wrap="clip",
                        ),
                        urwid.Text(
                            ["dtype:   ", ("bold", f"{obj.dtype}")],
                            wrap="clip",
                        ),
                        urwid.Divider("\u2500"),
                        preview_data,
                    ]
                )
            elif isinstance(obj, h5py.Group):
                children = self.get_items(f"{self.current_dir}/{key}")
                self.preview.body = urwid.SimpleListWalker(
                    [
                        urwid.Text(("5-bold", f"{self.current_dir}/{key}"), wrap="clip"),
                        urwid.Divider(),
                        urwid.Pile(children) if children else urwid.Text(""),
                    ]
                )
            else:
                self.preview.body = urwid.SimpleListWalker([])

    def navigate_down(self):
        try:
            self.current_dir_list.set_focus(self.current_dir_list.focus_position + 1)
            self.attrs_focused.update(self.current_dir_list.focus.base_widget.get_text()[0])
            self.set_preview()
        except IndexError:
            return

    def navigate_up(self):
        try:
            self.current_dir_list.set_focus(self.current_dir_list.focus_position - 1)
            self.attrs_focused.update(self.current_dir_list.focus.base_widget.get_text()[0])
            self.set_preview()
        except IndexError:
            return

    def navigate_enter(self):
        # If the group is empty, do nothing
        # Or if the current item is a dataset, do nothing
        with self.open_file("r") as f:
            obj = f[f"{self.current_dir}/{self.current_dir_list.focus.base_widget.get_text()[0]}"]
            if isinstance(obj, h5py.Dataset) or not obj.keys():
                return

        self._current_dir.append(self.current_dir_list.focus.base_widget.get_text()[0])
        self._focus_stack.append(self.current_dir_list.focus_position)

        # Update the current directory list and the attributes list to reflect the new directory
        self.current_dir_list.body = urwid.SimpleFocusListWalker(self.get_items())
        self.current_dir_list.set_focus(0)
        self.attrs_focused.update(self.current_dir_list.focus.base_widget.get_text()[0])

        # Add parent dir list to navigator contents, if it doesn't exist
        if len(self.navigator.contents) == 2:
            self.navigator.contents.insert(0, (self.parent_dir_list, ("weight", 0.75, False)))

        # Update the parent directory list and set the focus to the last focused item
        self.parent_dir_list.body = urwid.SimpleFocusListWalker(self.get_items(self.parent_dir))
        self.parent_dir_list.set_focus(self._focus_stack[-1])
        self.set_preview()

        # Set the attributes of the current directory
        self.attrs_current_dir.update()

    def navigate_exit(self):
        # If the current directory is the root, do nothing
        if not self._current_dir:
            return

        self._current_dir.pop()
        self.current_dir_list.body = urwid.SimpleFocusListWalker(self.get_items())
        self.current_dir_list.set_focus(self._focus_stack.pop())

        if not self._focus_stack:
            self.parent_dir_list.body = urwid.SimpleFocusListWalker([])
            self.navigator.contents.pop(0)  # remove parent dir list
        else:
            self.parent_dir_list.body = urwid.SimpleFocusListWalker(self.get_items(self.parent_dir))
            self.parent_dir_list.set_focus(self._focus_stack[-1])

        self.attrs_focused.update(self.current_dir_list.focus.base_widget.get_text()[0])
        self.set_preview()

        # Set the attributes of the current directory
        self.attrs_current_dir.update()

    def show_help(self):
        if not hasattr(self, "_help_widget"):
            self._help_widget = cKeybindsOverlay(Caller.main_loop, self.keybinds)
        self._help_widget.toggle()

    def move_focus(self, backwards: bool = False):
        # if self.focus.focus == self.navigator:
        pile = self.focus
        if pile.focus_position == 0:
            pile.focus_position = 1
            pile.focus.focus_position = 0 if not backwards else 1
            return
        if pile.focus_position == 1:
            if not backwards:
                if pile.focus.focus_position == 0:
                    pile.focus.focus_position = 1
                else:
                    pile.focus_position = 0
            else:
                if pile.focus.focus_position == 1:
                    pile.focus.focus_position = 0
                else:
                    pile.focus_position = 0
        return

    def delete_focused(self):
        """
        Delete the focused item
        """
        key = self.current_dir_list.focus.base_widget.get_text()[0]

        def _delete() -> None:
            with self.open_file("a") as f:
                del f[f"{self.current_dir}/{key}"]

            _fp = self.current_dir_list.focus_position
            self.current_dir_list.body = urwid.SimpleFocusListWalker(self.get_items())

            try:
                self.current_dir_list.set_focus(_fp - 1)
            except IndexError:
                pass  # leave at default position (0)

            if self.current_dir_list.body:
                self.attrs_focused.update(self.current_dir_list.focus.base_widget.get_text()[0])
                self.set_preview()

        ui = cConfirmDialog(
            Caller.main_loop,
            f"Are you sure you want to delete {self.current_dir}/{key}?",
            callback=_delete,
        )
        Caller.enter_widget(ui)

    def rename_focused(self):
        """
        Rename the focused item
        """
        key = self.current_dir_list.focus.base_widget.get_text()[0]

        def _rename(new_name: str) -> None:
            with self.open_file("a") as f:
                f.move(f"{self.current_dir}/{key}", f"{self.current_dir}/{new_name}")

            Caller.exit_widget()
            _fp = self.current_dir_list.focus_position
            self.current_dir_list.body = urwid.SimpleFocusListWalker(self.get_items())

            try:
                self.current_dir_list.set_focus(_fp)
            except IndexError:
                pass

        edit = cEdit(edit_text=key, edit_pos=len(key), callback=_rename)
        ui = cPopup(
            urwid.Filler(edit),
            height=1,
            footer="Enter: Confirm | Esc: Cancel",
            title=f"Rename {self.current_dir}/{key}",
        )
        Caller.enter_widget(ui)

    def enter_command(self):
        self.footer = self.command_line
        self.command_line.edit_text = ""
        self.set_focus("footer")

    def execute_command(self, command: str = None) -> None:
        if command == "q":
            Caller.exit_widget()
        else:
            self.footer = self.placehold_footer
            self.set_focus("body")

    def keypress(self, size: tuple[int, int], key: str) -> str | None:
        if self.focus_part == "footer":
            return self.footer.keypress(size, key)

        if key not in {"tab", "shift tab", "?", "q"} and self.focus.focus_position != 0:
            if self.focus.focus.focus_position == 0:
                self.attrs_current_dir.keypress((1, 1), key)
            else:
                self.attrs_focused.keypress((1, 1), key)
            return
        if key in self._keybinds and self.focus_part == "body":
            self._keybinds[key]()
        else:
            return super().keypress(size, key)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Path to the HDF5 file")
    args = parser.parse_args()

    Caller.main_loop = urwid.MainLoop(urwid.Pile([]), palette)
    Caller.enter_widget(HFive(args.filename))
    Caller.main_loop.screen.set_terminal_properties(colors=256)
    Caller.main_loop.run()


if __name__ == "__main__":

    main()
