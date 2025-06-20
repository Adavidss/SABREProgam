import tkinter as tk  # Ensure tkinter is imported for the tooltip functionality

# ==== STANDALONE TOOLTIP CLASS ==============================
class ToolTip:
    """Custom tooltip implementation for tkinter widgets with multi-tab support"""

    # Registry to keep track of tooltips by tab
    _registry = {}

    def __init__(self, widget, text, parent=None, tab_name=None):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.parent = parent  # Reference to main window for tooltip toggle check
        self.tab_name = tab_name

        if tab_name:
            ToolTip._registry.setdefault(tab_name, []).append(self)
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        # Check if tooltips are enabled before showing
        if self.parent and hasattr(self.parent, 'tooltips_enabled') and not self.parent.tooltips_enabled.get():
            return
        self.show_tooltip()

    def on_leave(self, event=None):
        self.hide_tooltip()

    def on_motion(self, event=None):
        if self.tooltip_window:
            self.update_tooltip_position(event)

    def show_tooltip(self):
        if self.tooltip_window:
            return
        
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text, 
                        background="#ffffe0", relief="solid", borderwidth=1,
                        font=("Arial", 8), wraplength=200)
        label.pack()

    def update_tooltip_position(self, event):
        if self.tooltip_window:
            x = self.widget.winfo_rootx() + event.x + 15
            y = self.widget.winfo_rooty() + event.y + 15
            self.tooltip_window.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    @classmethod
    def register_widget_tooltip(cls, widget, text, parent=None, tab_name=None):
        """Convenience method to create and register a tooltip."""
        return cls(widget, text, parent=parent, tab_name=tab_name)

    @classmethod
    def cleanup(cls):
        """Remove tooltips for widgets that no longer exist."""
        for tab, tips in list(cls._registry.items()):
            cls._registry[tab] = [t for t in tips if t.widget.winfo_exists()]
