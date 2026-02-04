from store.utils.utils import create_slice
from gui.theme.app_pallete import APP_PALETTE # Tu paleta dinámica generada

# Estado inicial del tema
initial_state = {
    "mode": "light",     # 'light' | 'dark'
    "scale": 1.0,        # Para zoom de UI futuro
    # Podrías guardar preferencias de color personalizadas aquí si quisieras
}

def toggle_mode(state, _):
    new_mode = "dark" if state["mode"] == "light" else "light"
    return {**state, "mode": new_mode}

def set_mode(state, payload):
    # payload: "light" o "dark"
    return {**state, "mode": payload}

theme_reducer, theme_actions = create_slice(
    name="theme",
    initial_state=initial_state,
    reducers={
        "toggleMode": toggle_mode,
        "setMode": set_mode,
    }
)