import utils


def connect_theme(store):
    get_state, _, subscribe = store

    def decorator(component_fn):
        def wrapper(parent, **props):
            current_theme = get_state()
            initial_context = utils.props_to_obj({**current_theme, **props})
            widget, reaction_fn = component_fn(parent, initial_context)

            def on_theme_change(w, new_theme_dict):
                new_context = utils.props_to_obj({**new_theme_dict, **props})
                reaction_fn(new_context)

            subscribe(widget, on_theme_change)
            return widget

        return wrapper

    return decorator
