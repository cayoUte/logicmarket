import tkinter as tk
from ui import styles, utils
from ui.components.buttons.Button import Pillow_Button

def DrawerLayout(root, routes, hooks, **initial_props):
    """
    DrawerLayout: The main skeleton of the application.
    
    Args:
        root: The parent Tkinter widget.
        routes: Dictionary {'Route Name': render_function}.
        hooks: Dictionary for state management/event subscription.
        **initial_props: Theme properties and configuration.
    """
    defaults = styles.get_theme("light")
    props = utils.props_to_obj(defaults, initial_props)
    
    # --- 1. MAIN STRUCTURE (2-COLUMN GRID) ---
    # We use pack side='left' for the drawer and fill='both' for the content
    
    # Sidebar Container (Left)
    sidebar = tk.Frame(root, bg=props.bg_sidebar, width=250)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False) # Force fixed width
    
    # Vertical Divider Line (Aesthetic)
    tk.Frame(root, bg=props.divider, width=1).pack(side="left", fill="y")

    # Content Container (Right - Dynamic)
    content_area = tk.Frame(root, bg=props.bg_app)
    content_area.pack(side="right", expand=True, fill="both")

    # --- 2. NAVIGATION LOGIC (ROUTER) ---
    nav_state = {"current": list(routes.keys())[0]} # Store current route
    button_refs = {} # Store references to update button styles (Active/Inactive)

    def update_buttons():
        """Iterates through buttons and changes color based on active state."""
        for route, btn_widget in button_refs.items():
            is_active = (route == nav_state["current"])
            
            # Define "Active" vs "Inactive" styles
            # We calculate the specific colors for this state
            state_style = {
                # Merge current global props to keep fonts/sizes
                **initial_props, 
                "bg_app": props.bg_sidebar, # The canvas background must match sidebar
                
                # Visual Logic:
                "primary": props.sidebar_active if is_active else props.bg_sidebar,
                "text_btn": props.sidebar_active_text if is_active else props.text_sidebar,
                "primary_active": props.sidebar_active,
                "primary_hover": props.sidebar_active if is_active else props.sidebar_active
            }
            
            # Trigger the theme update hook manually for this specific button
            # We assume the Pillow_Button subscribed itself to the global hook system.
            # Ideally, we would have a specific 'update' method, but we reuse the theme hook.
            if hasattr(btn_widget, 'trigger_style_update'):
                 btn_widget.trigger_style_update(state_style)
            else:
                # Fallback if you haven't implemented a specific method:
                # We simulate a theme change just for this widget if your system allows it,
                # otherwise, this part requires the button to expose an update function.
                pass

    def navigate_to(route_name):
        # A. Update Visual State of Buttons
        nav_state["current"] = route_name
        update_buttons()

        # B. Clear Content Area
        for widget in content_area.winfo_children():
            widget.destroy()
        
        # C. Render New View
        render_func = routes[route_name]
        render_func(content_area, hooks, **initial_props)
        
        # D. Ensure content area background is correct
        content_area.configure(bg=props.bg_app)

    # --- 3. SIDEBAR CONSTRUCTION ---
    
    # App Logo / Title
    lbl_logo = tk.Label(
        sidebar, 
        text="LogicMarket", 
        font=(props.family[0], 18, "bold"),
        bg=props.bg_sidebar,
        fg=props.primary,
        pady=30
    )
    lbl_logo.pack(anchor="center")

    # Generate Navigation Buttons
    for route_name in routes.keys():
        
        # Closure to capture the specific route name for the lambda
        def create_command(r):
            return lambda: navigate_to(r)

        # Style definition for Navigation Buttons (Ghost Style)
        nav_btn_style = {
            "bg_app": props.bg_sidebar, # Canvas bg matches sidebar
            "primary": props.bg_sidebar, # Transparent-ish base
            "text_btn": props.text_sidebar,
            "font_btn": (props.family[0], 11, "bold")
        }
        
        # Create the button
        btn = Pillow_Button(
            sidebar, 
            text=route_name, 
            on_click=create_command(route_name), 
            hooks=hooks, 
            width=210, 
            height=45, 
            radius=10, 
            **nav_btn_style
        )
        btn.pack(pady=5)
        
        # Save reference for future updates
        button_refs[route_name] = btn
        
    # Footer (Optional)
    tk.Label(
        sidebar, 
        text="v1.0.0", 
        bg=props.bg_sidebar, 
        fg=props.text_sidebar, 
        font=(props.family[0], 8)
    ).pack(side="bottom", pady=20)

    # --- 4. INITIAL LOAD ---
    # Load the first route by default
    navigate_to(list(routes.keys())[0])

    # Global Theme Hooks (Reactive)
    hooks['subscribe'](sidebar, lambda w, p: w.configure(bg=p['bg_sidebar']))
    hooks['subscribe'](content_area, lambda w, p: w.configure(bg=p['bg_app']))