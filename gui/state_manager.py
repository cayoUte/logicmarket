import weakref


def create_store(initial_state):
    state = {"current": initial_state}

    listeners = weakref.WeakKeyDictionary()

    def get_state():
        return state["current"]

    def subscribe(widget, reaction_fn):
        listeners[widget] = reaction_fn

    def dispatch(new_state):
        state["current"] = new_state
        for widget, reaction_fn in list(listeners.items()):
            if widget.winfo_exists():
                reaction_fn(widget, new_state)

    return get_state, dispatch, subscribe
