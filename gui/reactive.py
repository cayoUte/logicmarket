import utils

def connect_theme(store):
    """
    Returns a Decorator/HOF that connects a component to the store.
    """
    get_state, _, subscribe = store

    def decorator(component_fn):
        """
        The HOF wrapper.
        Interceps the creation call.
        """
        def wrapper(parent, **props):
            # 1. Get current global theme
            current_theme = get_state()
            
            # 2. Merge props: Explicit props override theme props
            # We convert to object for dot notation access inside component
            initial_context = utils.props_to_obj({**current_theme, **props})

            # 3. Render the Component
            # Contract: Component MUST return (widget, update_logic_fn)
            widget, reaction_fn = component_fn(parent, initial_context)

            # 4. Define the Reactive Bridge
            def on_theme_change(w, new_theme_dict):
                # Merge new theme with original props (props are sticky)
                new_context = utils.props_to_obj({**new_theme_dict, **props})
                reaction_fn(new_context)

            # 5. Auto-subscribe
            subscribe(widget, on_theme_change)

            return widget
            
        return wrapper
    return decorator