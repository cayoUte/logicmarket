def create_slice(name, initial_state, reducers):
    """
    Fábrica de Slices Funcional.
    """
    
    action_creators = {}
    reducer_map = {}
    
    # 1. Procesamos cada mini-reducer (Igual que antes)
    for key, handler in reducers.items():
        action_type = f"{name}/{key}"
        reducer_map[action_type] = handler
        
        def make_action_creator(type_name):
            def action_creator(payload=None):
                return (type_name, payload)
            return action_creator
            
        action_creators[key] = make_action_creator(action_type)

    # 2. Creamos el Reducer Maestro del Slice (AQUÍ ESTÁ EL FIX)
    def slice_reducer(state=initial_state, action=None):
        # --- FIX CRÍTICO ---
        # Si state se pasa explícitamente como None (desde combine_reducers o init),
        # forzamos el uso de initial_state.
        if state is None:
            state = initial_state
            
        if action is None:
            return state
            
        tipo, payload = action
        
        # Si el tipo existe en este slice, ejecutamos su lógica
        if tipo in reducer_map:
            handler = reducer_map[tipo]
            return handler(state, payload)
            
        return state

    return slice_reducer, action_creators