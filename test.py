import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Toplevel, Label, Button
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from PIL import Image, ImageTk

class OpenUtopiaFinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenUtopia Finance")

        # Default Grid Toggled OFF
        self.grid_shown = False

        # Initialize income data
        self.income_data = pd.DataFrame(columns=["Period", "Amount"])

        # Set up toolbar
        self.setup_toolbar()

        # Set up data entry form
        self.setup_data_entry_form()

        # Set up matplotlib figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Matplotlib Navigation Toolbar
        self.nav_toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.nav_toolbar.update()

        # Keep track of graph type and theme
        self.graph_type = "line"
        self.current_theme = "default"

        # History for back/forward functionality
        self.history = []
        self.history_index = -1

        # Set initial theme
        self.apply_theme("#F5F7F8", "black")

         # Shortcuts storage
        self.original_shortcuts = {
            "edit_income": "<Shift-X>",
            "toggle_grid": "<Shift-G>",
            "change_theme": "<Shift-T>",
            "enable_zoom": "<Shift-Z>",
            "save_graph": "<Shift-S>"
        }

        # Shortcuts
        self.shortcuts = self.original_shortcuts.copy()
        self.bind_shortcuts()

    def setup_toolbar(self):
        toolbar_frame = tk.Frame(self.root)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Icons Size
        icon_size = (30, 30) 

        open_icon = self.resize_icon("icons/folder.png", icon_size)
        home_icon = self.resize_icon("icons/home.png", icon_size)
        back_icon = self.resize_icon("icons/back.png", icon_size)
        forward_icon = self.resize_icon("icons/forward.png", icon_size)
        move_icon = self.resize_icon("icons/move.png", icon_size)
        zoom_icon = self.resize_icon("icons/zoom.png", icon_size)
        grid_icon = self.resize_icon("icons/grid.png", icon_size)
        subplot_icon = self.resize_icon("icons/subplot.png", icon_size)
        resize_icon = self.resize_icon("icons/resize.png", icon_size)
        graph_icon = self.resize_icon("icons/graph.png", icon_size)
        edit_icon = self.resize_icon("icons/edit.png", icon_size)
        theme_icon = self.resize_icon("icons/theme.png", icon_size)
        shortcuts_icon = self.resize_icon("icons/shortcuts.png", icon_size)
        save_icon = self.resize_icon("icons/save.png", icon_size)

        tk.Button(toolbar_frame, image=open_icon, command=self.open_file).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=home_icon, command=self.reset_view).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=back_icon, command=self.go_back).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=forward_icon, command=self.go_forward).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=move_icon, command=self.enable_move).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=zoom_icon, command=self.enable_zoom).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=grid_icon, command=self.toggle_grid).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=subplot_icon, command=self.configure_subplots).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=graph_icon, command=self.edit_graph_type).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=edit_icon, command=self.edit_income).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=theme_icon, command=self.change_theme).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=shortcuts_icon, command=self.edit_shortcuts).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=save_icon, command=self.save_graph).pack(side=tk.LEFT, padx=2)

        # Store references to images so they aren't garbage collected
        self.icons = [open_icon, home_icon, back_icon, forward_icon, move_icon, zoom_icon,
                      subplot_icon, graph_icon, edit_icon, theme_icon, save_icon, grid_icon, shortcuts_icon]
        
    def bind_shortcuts(self):
        """Binds keyboard shortcuts."""
        self.root.bind(self.shortcuts["edit_income"], lambda event: self.edit_income())
        self.root.bind(self.shortcuts["toggle_grid"], lambda event: self.toggle_grid())
        self.root.bind(self.shortcuts["change_theme"], lambda event: self.change_theme())
        self.root.bind(self.shortcuts["enable_zoom"], lambda event: self.enable_zoom())
        self.root.bind(self.shortcuts["save_graph"], lambda event: self.save_graph())

    def unbind_shortcuts(self):
        """Unbinds all current shortcuts."""
        for shortcut in self.shortcuts.values():
            self.root.unbind(shortcut)

    def edit_shortcuts(self):
        """Allows the user to modify keyboard shortcuts."""
        shortcut_dialog = Toplevel(self.root)
        shortcut_dialog.title("Edit Shortcuts")
        shortcut_dialog.geometry("300x300")

        Label(shortcut_dialog, text="Edit Income:").grid(row=0, column=0, padx=10, pady=10)
        edit_income_entry = tk.Entry(shortcut_dialog)
        edit_income_entry.insert(0, self.shortcuts["edit_income"])
        edit_income_entry.grid(row=0, column=1, padx=10, pady=10)

        Label(shortcut_dialog, text="Toggle Grid:").grid(row=1, column=0, padx=10, pady=10)
        toggle_grid_entry = tk.Entry(shortcut_dialog)
        toggle_grid_entry.insert(0, self.shortcuts["toggle_grid"])
        toggle_grid_entry.grid(row=1, column=1, padx=10, pady=10)

        Label(shortcut_dialog, text="Change Theme:").grid(row=2, column=0, padx=10, pady=10)
        change_theme_entry = tk.Entry(shortcut_dialog)
        change_theme_entry.insert(0, self.shortcuts["change_theme"])
        change_theme_entry.grid(row=2, column=1, padx=10, pady=10)

        Label(shortcut_dialog, text="Enable Zoom:").grid(row=3, column=0, padx=10, pady=10)
        enable_zoom_entry = tk.Entry(shortcut_dialog)
        enable_zoom_entry.insert(0, self.shortcuts["enable_zoom"])
        enable_zoom_entry.grid(row=3, column=1, padx=10, pady=10)

        Label(shortcut_dialog, text="Save Graph:").grid(row=4, column=0, padx=10, pady=10)
        save_graph_entry = tk.Entry(shortcut_dialog)
        save_graph_entry.insert(0, self.shortcuts["save_graph"])
        save_graph_entry.grid(row=4, column=1, padx=10, pady=10)

        def save_shortcuts():
            """Saves the user-defined shortcuts and rebinds them."""
            self.unbind_shortcuts()  # Unbind all current shortcuts

            self.shortcuts["edit_income"] = edit_income_entry.get()
            self.shortcuts["toggle_grid"] = toggle_grid_entry.get()
            self.shortcuts["change_theme"] = change_theme_entry.get()
            self.shortcuts["enable_zoom"] = enable_zoom_entry.get()
            self.shortcuts["save_graph"] = save_graph_entry.get()

            self.bind_shortcuts()  # Rebind new shortcuts
            shortcut_dialog.destroy()

        def reset_shortcuts():
            """Resets shortcuts to their original values and rebinds them."""
            self.unbind_shortcuts()  # Unbind all current shortcuts

            self.shortcuts = self.original_shortcuts.copy()  # Reset to original
            self.bind_shortcuts()  # Rebind original shortcuts

            # Update the entries in the dialog to reflect the reset shortcuts
            edit_income_entry.delete(0, tk.END)
            edit_income_entry.insert(0, self.shortcuts["edit_income"])
            toggle_grid_entry.delete(0, tk.END)
            toggle_grid_entry.insert(0, self.shortcuts["toggle_grid"])
            change_theme_entry.delete(0, tk.END)
            change_theme_entry.insert(0, self.shortcuts["change_theme"])
            enable_zoom_entry.delete(0, tk.END)
            enable_zoom_entry.insert(0, self.shortcuts["enable_zoom"])
            save_graph_entry.delete(0, tk.END)
            save_graph_entry.insert(0, self.shortcuts["save_graph"])

        Button(shortcut_dialog, text="Save", command=save_shortcuts).grid(row=5, column=0, padx=10, pady=20)
        Button(shortcut_dialog, text="Reset", command=reset_shortcuts).grid(row=5, column=1, padx=10, pady=20)

    def setup_data_entry_form(self):
        """Sets up the data entry form for user input."""
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(entry_frame, text="Period:").grid(row=0, column=0, padx=5, pady=5)
        self.period_entry = tk.Entry(entry_frame)
        self.period_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(entry_frame, text="Amount:").grid(row=0, column=2, padx=5, pady=5)
        self.amount_entry = tk.Entry(entry_frame)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        add_button = tk.Button(entry_frame, text="Add Data", command=self.add_income_data)
        add_button.grid(row=0, column=4, padx=5, pady=5)

        clear_button = tk.Button(entry_frame, text="Clear Data", command=self.clear_income_data)
        clear_button.grid(row=0, column=5, padx=5, pady=5)

        update_button = tk.Button(entry_frame, text="Update Graph", command=self.update_graph)
        update_button.grid(row=0, column=6, padx=5, pady=5)

    def resize_icon(self, image_path, size):
        """Resizes an icon to the specified size and returns a PhotoImage."""
        image = Image.open(image_path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def open_file(self):
        """Opens a file dialog to select an existing graph file."""
        filename = filedialog.askopenfilename(title="Open Graph", filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if filename:
            self.load_graph(filename)

    def load_graph(self, filename):
        """Loads a graph from a CSV file."""
        try:
            self.income_data = pd.read_csv(filename)
            self.history.append(self.income_data.copy())
            self.history_index += 1
            self.update_graph()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load graph: {e}")

    def reset_view(self):
        """Resets the view to the default state."""
        self.ax.set_xlim(auto=True)
        self.ax.set_ylim(auto=True)
        self.canvas.draw()

    def go_back(self):
        """Navigates back in the graph history."""
        if self.history_index > 0:
            self.history_index -= 1
            self.income_data = self.history[self.history_index].copy()
            self.update_graph()

    def go_forward(self):
        """Navigates forward in the graph history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.income_data = self.history[self.history_index].copy()
            self.update_graph()

    def enable_move(self):
        """Enables the move functionality."""
        self.nav_toolbar.pan()

    def enable_zoom(self):
        """Enables the zoom functionality."""
        self.nav_toolbar.zoom()

    def configure_subplots(self):
        """Configures subplots."""
        plt.subplots_adjust(left=0.1, bottom=0.3, right=0.9, top=0.7)
        self.update_graph()

    def edit_graph_type(self):
        """Allows the user to choose the graph type."""
        options = ["Line", "Bar", "Candlestick"]
        graph_type = simpledialog.askstring("Select Graph Type", f"Choose the graph type: {', '.join(options)}")
        if graph_type:
            self.graph_type = graph_type.lower()
            self.update_graph()

    def edit_income(self):
        """Allows the user to edit income data."""
        amount = simpledialog.askfloat("Edit Income", "Enter the new income amount:")
        if amount is not None:
            new_row = pd.DataFrame({"Period": [len(self.income_data) + 1], "Amount": [amount]})
            self.income_data = pd.concat([self.income_data, new_row], ignore_index=True)
            self.history.append(self.income_data.copy())
            self.history_index += 1
            self.update_graph()

    def change_theme(self):
        """Allows the user to change the application theme."""
        themes = {
            "Default": ("#F5F7F8", "black", "default"),
            "Dark": ("#1e1e1e", "blue", "dark"),
            "Blue": ("#001f3f", "black", "blue"),
            "Hacker": ("black", "#06D001", "hacker"),
            "Orange": ("#E3651D", "black", "orange"),
            "Red": ("#B31312", "black", "red"),
            "Sakura": ("#FF8C9E", "black", "sakura"),
            "Acid": ("#674188", "black", "acid")
        }
        theme_names = ", ".join(themes.keys())
        theme_choice = simpledialog.askstring("Select Theme", f"Choose a theme: {theme_names}")
        if theme_choice and theme_choice in themes:
            bg_color, fg_color, self.current_theme = themes[theme_choice]
            self.apply_theme(bg_color, fg_color)

    def apply_theme(self, bg_color, fg_color):
        """Applies the selected theme to the app."""
        self.root.configure(bg=bg_color)

        # Update the colors for all widgets
        for widget in self.root.winfo_children():
            widget.configure(bg=bg_color)
        
            # Apply foreground color if the widget supports it
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text, tk.Checkbutton, tk.Radiobutton)):
                widget.configure(fg=fg_color)
    
        # Update the matplotlib graph background and axis colors
        self.ax.set_facecolor(bg_color)
        self.ax.spines['bottom'].set_color(fg_color)
        self.ax.spines['left'].set_color(fg_color)
        self.ax.spines['top'].set_color(fg_color)
        self.ax.spines['right'].set_color(fg_color)
        self.ax.xaxis.label.set_color(fg_color)
        self.ax.yaxis.label.set_color(fg_color)
        self.ax.tick_params(axis='x', colors=fg_color)
        self.ax.tick_params(axis='y', colors=fg_color)
        self.update_graph()

    def save_graph(self):
        """Saves the current graph as an image."""
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
        if filename:
            self.figure.savefig(filename)

    def add_income_data(self):
        """Adds income data to the graph."""
        try:
            period = int(self.period_entry.get())
            amount = float(self.amount_entry.get())
            new_row = pd.DataFrame({"Period": [period], "Amount": [amount]})
            self.income_data = pd.concat([self.income_data, new_row], ignore_index=True)
            self.history.append(self.income_data.copy())
            self.history_index += 1
            self.update_graph()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for period and amount.")

    def clear_income_data(self):
        """Clears all income data."""
        self.income_data = pd.DataFrame(columns=["Period", "Amount"])
        self.history = []
        self.history_index = -1
        self.update_graph()

    def update_graph(self):
        """Updates the graph with the current income data."""
        self.ax.clear()
        if not self.income_data.empty:
            if self.graph_type == "line":
                self.income_data.plot(x="Period", y="Amount", ax=self.ax, legend=False)
            elif self.graph_type == "bar":
                self.income_data.plot(kind="bar", x="Period", y="Amount", ax=self.ax, legend=False)
            elif self.graph_type == "candlestick":
                self.ax.plot(self.income_data["Period"], self.income_data["Amount"], 'o-')
        self.canvas.draw()

    def toggle_grid(self):
        """Toggles the grid on the graph."""
        self.grid_shown = not self.grid_shown
        self.ax.grid(self.grid_shown)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenUtopiaFinanceApp(root)
    root.mainloop()
