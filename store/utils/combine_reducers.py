def combine_reducers(reducers_dict):
    """
    Combina múltiples reducers en uno solo.
    Cada reducer gestionará solo su parte del estado global.
    """
    def root_reducer(state, action):
        if state is None: state = {}
        
        next_state = {}
        has_changed = False
        
        for key, reducer in reducers_dict.items():
            # Obtenemos el sub-estado anterior (o None si es init)
            previous_state_for_key = state.get(key)
            
            # Ejecutamos el reducer del slice
            next_state_for_key = reducer(previous_state_for_key, action)
            
            # Guardamos el nuevo sub-estado
            next_state[key] = next_state_for_key
            
            # Chequeo simple de cambios (por referencia)
            if next_state_for_key is not previous_state_for_key:
                has_changed = True
                
        return next_state if has_changed else state

    return root_reducer