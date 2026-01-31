import weakref

def create_store(initial_state):
    """
    Creates a functional store closure.
    Returns: (get_state, update_state, subscribe)
    """
    # State is enclosed in the closure
    state = {"current": initial_state}
    
    # We use WeakSet to automatically remove dead widgets/functions
    # This fixes the "invalid command name" bug automatically.
    listeners = weakref.WeakKeyDictionary() 

    def get_state():
        return state["current"]

    def subscribe(widget, reaction_fn):
        """
        Binds a widget lifecycle to a reaction function.
        If the widget is destroyed, the subscription dies with it.
        """
        listeners[widget] = reaction_fn

    def dispatch(new_state):
        state["current"] = new_state
        # Notify only alive listeners
        for widget, reaction_fn in list(listeners.items()):
            # Double check existence (tkinter specific)
            if widget.winfo_exists():
                reaction_fn(widget, new_state)

    return get_state, dispatch, subscribe