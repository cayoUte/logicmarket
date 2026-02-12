import threading
import asyncio
import tkinter as tk


def create_store(reducer, initial_state):

    scope = {"state": initial_state, "listeners": []}

    def _notify():
        current_state = scope["state"]
        for callback in scope["listeners"]:
            callback(current_state)

    def _apply_change(action):
        scope["state"] = reducer(scope["state"], action)
        _notify()

    def _run_async_thread(async_action, ui_ref, dispatch_fn):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        def thread_safe_dispatch(action):
            if ui_ref:
                ui_ref.after(0, lambda: dispatch_fn(action, ui_ref))
            else:
                dispatch_fn(action, ui_ref)

        try:
            loop.run_until_complete(async_action(thread_safe_dispatch))
        finally:
            loop.close()

    def get_state():
        return scope["state"]

    def subscribe(callback):
        scope["listeners"].append(callback)

        def unsubscribe():
            if callback in scope["listeners"]:
                scope["listeners"].remove(callback)

        return unsubscribe

    def dispatch(action, ui_ref: tk.Widget = None):

        if asyncio.iscoroutinefunction(action):
            if not ui_ref:
                print("⚠️ Warning: Async action despachada sin ui_ref.")
            threading.Thread(
                target=_run_async_thread, args=(action, ui_ref, dispatch), daemon=True
            ).start()
            return

        if callable(action):
            action(lambda a: dispatch(a, ui_ref))
            return

        if ui_ref and threading.current_thread() is not threading.main_thread():
            ui_ref.after(0, lambda: _apply_change(action))
        else:
            _apply_change(action)

    return dispatch, subscribe, get_state
