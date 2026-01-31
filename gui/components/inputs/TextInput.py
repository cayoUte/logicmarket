from gui.theme.app_pallete import get_app_color
import tkinter as tk
from gui.theme.inputs import INPUT_THEMES


def TextInput(parent, placeholder="", width=200, variant="primary"):
    """
    Functional Text Input with custom styling and state management.

    Args:
        placeholder (str): Text shown when empty.
        variant (str): Palette key for the focus highlight color.
    """

    theme = INPUT_THEMES.get(variant, INPUT_THEMES["primary"])

    def resolve_color(value):
        if isinstance(value, (tuple, list)) and len(value) == 2:
            return get_app_color(value[0], value[1])
        return value

    state = {
        "focused": False,
        "is_placeholder_on": True if placeholder else False,
        "bg_idle": resolve_color(theme["bg_idle"]),
        "bg_focus": resolve_color(theme["bg_focus"]),
        "border_idle": resolve_color(theme["border_idle"]),
        "border_focus": resolve_color(theme["border_focus"]),
        "text_main": resolve_color(theme["text_color"]),
        "text_placeholder": resolve_color(theme["placeholder"]),
    }

    container = tk.Frame(
        parent, bg=state["border_idle"], width=width, height=theme["height"]
    )
    container.pack_propagate(False)

    inner_padding = tk.Frame(container, bg=state["bg_idle"])
    inner_padding.pack(fill="both", expand=True, padx=1, pady=1)

    entry = tk.Entry(
        inner_padding,
        bg=state["bg_idle"],
        fg=state["text_placeholder"],
        font=("Segoe UI", 10),
        relief="flat",
        insertbackground=state["text_main"],
    )
    entry.pack(fill="both", expand=True, padx=8, pady=5)

    def update_visuals():

        border_col = state["border_focus"] if state["focused"] else state["border_idle"]
        container.configure(bg=border_col)

        bg_col = state["bg_focus"] if state["focused"] else state["bg_idle"]
        inner_padding.configure(bg=bg_col)
        entry.configure(bg=bg_col)

    def on_focus_in(e):
        state["focused"] = True

        if state["is_placeholder_on"]:
            entry.delete(0, "end")
            entry.configure(fg=state["text_main"])
            state["is_placeholder_on"] = False

        update_visuals()

    def on_focus_out(e):
        state["focused"] = False

        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(fg=state["text_placeholder"])
            state["is_placeholder_on"] = True

        update_visuals()

    if placeholder:
        entry.insert(0, placeholder)

    def get_value():
        """Returns None if placeholder is active, otherwise the text."""
        if state["is_placeholder_on"]:
            return ""
        return entry.get()

    def set_value(text):
        entry.delete(0, "end")
        if text:
            entry.insert(0, text)
            entry.configure(fg=state["text_main"])
            state["is_placeholder_on"] = False
        else:
            on_focus_out(None)

    container.get_value = get_value
    container.set_value = set_value
    container.entry_widget = entry

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return container
