import threading
import asyncio
import tkinter as tk

def create_store(reducer, initial_state):
    """
    Crea un Store funcional usando Closures.
    Devuelve una tupla de funciones: (dispatch, subscribe, get_state)
    """
    
    # --- CLOSURE SCOPE (Estado encapsulado) ---
    # Usamos un diccionario mutable para mantener la referencia en el closure
    scope = {
        "state": initial_state,
        "listeners": []
    }

    # --- FUNCIONES INTERNAS (Helpers) ---

    def _notify():
        """Avisa a todos los suscriptores del cambio."""
        current_state = scope["state"]
        for callback in scope["listeners"]:
            callback(current_state)

    def _apply_change(action):
        """Ejecuta el reducer y actualiza el estado (Hilo Principal)."""
        scope["state"] = reducer(scope["state"], action)
        _notify()

    def _run_async_thread(async_action, ui_ref, dispatch_fn):
        """Ejecuta corutinas en un hilo separado."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Wrapper para volver al hilo principal desde el async
        def thread_safe_dispatch(action):
            if ui_ref:
                ui_ref.after(0, lambda: dispatch_fn(action, ui_ref))
            else:
                dispatch_fn(action, ui_ref)

        try:
            loop.run_until_complete(async_action(thread_safe_dispatch))
        finally:
            loop.close()

    # --- FUNCIONES PÚBLICAS (Interfaz) ---

    def get_state():
        return scope["state"]

    def subscribe(callback):
        scope["listeners"].append(callback)
        
        # --- NUEVO: Retornar función para des-suscribirse ---
        def unsubscribe():
            if callback in scope["listeners"]:
                scope["listeners"].remove(callback)
        
        return unsubscribe

    def dispatch(action, ui_ref: tk.Widget = None):
        """
        Función polimórfica: maneja acciones síncronas, thunks y async.
        """
        
        # 1. ¿Es una función asíncrona? (Async/Await)
        if asyncio.iscoroutinefunction(action):
            if not ui_ref:
                print("⚠️ Warning: Async action despachada sin ui_ref.")
            # Iniciamos hilo daemon para no bloquear GUI
            threading.Thread(
                target=_run_async_thread, 
                args=(action, ui_ref, dispatch), 
                daemon=True
            ).start()
            return

        # 2. ¿Es un Thunk síncrono? (Función normal)
        if callable(action):
            # Inyección de dependencia recursiva
            action(lambda a: dispatch(a, ui_ref))
            return

        # 3. Es un objeto plano (Dict/Tuple) -> Ejecutar Reducer
        
        # Si por alguna razón estamos en otro hilo, forzamos volver al main
        if ui_ref and threading.current_thread() is not threading.main_thread():
            ui_ref.after(0, lambda: _apply_change(action))
        else:
            _apply_change(action)

    # Retornamos las funciones "hermanas"
    return dispatch, subscribe, get_state