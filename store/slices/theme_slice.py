from store.utils.utils import create_slice
from gui.theme.app_pallete import APP_PALETTE

initial_state = {
    "mode": "light",
    "scale": 1.0,
}


def toggle_mode(state, _):
    new_mode = "dark" if state["mode"] == "light" else "light"
    return {**state, "mode": new_mode}


def set_mode(state, payload):
    return {**state, "mode": payload}


theme_reducer, theme_actions = create_slice(
    name="theme",
    initial_state=initial_state,
    reducers={
        "toggleMode": toggle_mode,
        "setMode": set_mode,
    },
)
