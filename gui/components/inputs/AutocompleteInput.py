import tkinter as tk
from gui.theme.app_pallete import get_app_color

class AutocompleteInput(tk.Frame):
    """
    Input con sugerencias basado en una lista estática.
    """
    def __init__(self, parent, suggestions=[], placeholder="", width=200, variant="neutral"):
        super().__init__(parent, bg=get_app_color("neutral", 0))
        
        self.suggestions = suggestions
        self.var = tk.StringVar()
        self.width = width
        
        # Colores
        bg_color = get_app_color("neutral", 0)
        fg_color = get_app_color("neutral", 900)
        border_color = get_app_color(variant, "Basic")
        
        # Entry Widget
        self.entry = tk.Entry(
            self, 
            textvariable=self.var, 
            font=("Segoe UI", 10),
            bg=bg_color,
            fg=fg_color,
            relief="flat",
            highlightthickness=1,
            highlightbackground=get_app_color("neutral", 300),
            highlightcolor=border_color
        )
        self.entry.pack(fill="x", ipady=4)
        
        # Placeholder logic
        self.placeholder = placeholder
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.config(fg="grey")
            self.entry.bind("<FocusIn>", self._on_focus_in)
            self.entry.bind("<FocusOut>", self._on_focus_out)

        # Listbox flotante (inicialmente oculta)
        # Usamos Toplevel para que flote sobre todo, o un Frame posicionado.
        # Para simplificar en layouts complejos, usaremos Listbox dentro del mismo frame
        # pero solo visible cuando hay match.
        self.listbox = tk.Listbox(
            self, 
            height=4, 
            font=("Segoe UI", 9),
            bg=bg_color,
            selectbackground=border_color,
            selectforeground="white",
            relief="flat",
            borderwidth=1
        )
        
        # Eventos de tecleo
        self.entry.bind("<KeyRelease>", self._on_key_release)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    def _on_key_release(self, event):
        val = self.var.get()
        if val == self.placeholder: return
        
        # Si está vacío, ocultamos lista
        if val == '':
            self.listbox.pack_forget()
        else:
            # Filtramos
            hits = [item for item in self.suggestions if val.lower() in item.lower()]
            self._update_list(hits)

    def _update_list(self, hits):
        self.listbox.delete(0, tk.END)
        if hits:
            # Mostramos máximo 5 sugerencias
            for item in hits[:5]:
                self.listbox.insert(tk.END, item)
            self.listbox.pack(fill="x", before=self.entry) # Truco: pack antes o despues
            # Ajuste visual: queremos que aparezca DEBAJO del entry.
            self.listbox.pack_forget()
            self.listbox.pack(fill="x", pady=(0,5))
        else:
            self.listbox.pack_forget()

    def _on_select(self, event):
        if not self.listbox.curselection(): return
        
        index = self.listbox.curselection()[0]
        val = self.listbox.get(index)
        
        # Set value
        self.var.set(val)
        self.entry.config(fg=get_app_color("neutral", 900)) # Restore color if was placeholder
        
        # Hide list
        self.listbox.pack_forget()
        
        # Refocus entry (optional)
        self.entry.focus_set()

    def get_value(self):
        val = self.var.get()
        return "" if val == self.placeholder else val

    # --- Placeholder Handlers ---
    def _on_focus_in(self, e):
        if self.var.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg=get_app_color("neutral", 900))

    def _on_focus_out(self, e):
        if not self.var.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="grey")