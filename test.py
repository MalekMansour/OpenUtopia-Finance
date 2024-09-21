# Author: Malek Mansour
# LICENSE: MIT License
# Year Created: 2024
# Description: N/A

# Imports
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Toplevel, Label, Button, Scale, HORIZONTAL
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from PIL import Image, ImageTk
import mplfinance as mpf
import xlsxwriter
import openpyxl
import numpy as np

class OpenUtopiaFinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenUtopia Finance")

        # Default Grid Toggled OFF
        self.grid_shown = False

        # Initialize income data
        self.income_data = pd.DataFrame(columns=["Period", "Amount"])

        # Toolbar
        self.setup_toolbar()

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

        # Default margins for the graph
        self.default_margins = {"left": 0.1, "right": 0.9, "top": 0.9, "bottom": 0.1}
        self.current_margins = self.default_margins.copy()

    def setup_toolbar(self):
        toolbar_frame = tk.Frame(self.root)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Icon Size & Images
        icon_size = (30, 30) 

        open_icon = self.resize_icon("icons/folder.png", icon_size)
        home_icon = self.resize_icon("icons/home.png", icon_size)
        back_icon = self.resize_icon("icons/back.png", icon_size)
        forward_icon = self.resize_icon("icons/forward.png", icon_size)
        move_icon = self.resize_icon("icons/move.png", icon_size)
        zoom_icon = self.resize_icon("icons/zoom.png", icon_size)
        grid_icon = self.resize_icon("icons/grid.png", icon_size)
        resize_icon = self.resize_icon("icons/edit.png", icon_size)
        graph_icon = self.resize_icon("icons/graph.png", icon_size)
        edit_icon = self.resize_icon("icons/add.png", icon_size)
        theme_icon = self.resize_icon("icons/theme.png", icon_size)
        shortcuts_icon = self.resize_icon("icons/shortcuts.png", icon_size)
        save_icon = self.resize_icon("icons/save.png", icon_size)

        # Icons & Their Functions
        tk.Button(toolbar_frame, image=open_icon, command=self.open_file).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=home_icon, command=self.home).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=back_icon, command=self.go_back).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=forward_icon, command=self.go_forward).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=move_icon, command=self.enable_move).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=zoom_icon, command=self.enable_zoom).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=grid_icon, command=self.toggle_grid).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=resize_icon, command=self.resize_graph).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=graph_icon, command=self.edit_graph_type).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=edit_icon, command=self.edit_income).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=theme_icon, command=self.change_theme).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=shortcuts_icon, command=self.edit_shortcuts).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=save_icon, command=self.save_graph).pack(side=tk.LEFT, padx=2)

        # Store references to images so they aren't garbage collected
        self.icons = [open_icon, home_icon, back_icon, forward_icon, move_icon, zoom_icon,
                graph_icon, edit_icon, theme_icon, save_icon, grid_icon, shortcuts_icon, resize_icon]
        
    def home(self):
        pass

# SHORTCUT BUTTON SECTION
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
            self.unbind_shortcuts() 

            self.shortcuts["edit_income"] = edit_income_entry.get()
            self.shortcuts["toggle_grid"] = toggle_grid_entry.get()
            self.shortcuts["change_theme"] = change_theme_entry.get()
            self.shortcuts["enable_zoom"] = enable_zoom_entry.get()
            self.shortcuts["save_graph"] = save_graph_entry.get()

            self.bind_shortcuts()  
            shortcut_dialog.destroy()

        def reset_shortcuts():
            """Resets shortcuts to their original values and rebinds them."""
            self.unbind_shortcuts()  

            self.shortcuts = self.original_shortcuts.copy()  
            self.bind_shortcuts()  

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

# THEMES
    def apply_theme(self, background, foreground):
        """Applies the theme to the plot."""
        self.figure.patch.set_facecolor(background)
        self.ax.set_facecolor(background)
        self.ax.tick_params(colors=foreground)
        self.ax.xaxis.label.set_color(foreground)
        self.ax.yaxis.label.set_color(foreground)
        self.ax.title.set_color(foreground)
        self.current_theme = {"background": background, "foreground": foreground}
        self.canvas.draw()

    def change_theme(self):
        """Switches between multiple themes."""
        if self.current_theme == "default":
            self.apply_theme("#0C0C0C", "#FFFFFF")  # Switch to dark theme
            self.current_theme = "dark"
        elif self.current_theme == "dark":
            self.apply_theme("#001F3F", "#FFFFFF")  # Switch to blue theme
            self.current_theme = "blue"
        elif self.current_theme == "blue":
            self.apply_theme("#31363F", "#FFFFFF")  # Switch to red theme
            self.current_theme = "red"
        else:
            self.apply_theme("#F5F7F8", "#000000")  # Switch back to default theme
            self.current_theme = "default"

# OPEN FILE
    def open_file(self):
        """Handles the action of opening a file."""
        file_path = filedialog.askopenfilename(title="Open Income Data", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.income_data = pd.read_csv(file_path)
                self.plot_income() 
                self.history.append(self.income_data.copy())  
                self.history_index += 1  
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    import os

# GO BACK AND FORWARD
    def go_back(self):
        """Go back to the previous state in the history."""
        if self.history_index > 0:
            self.history_index -= 1
            self.income_data = self.history[self.history_index].copy()
            self.plot_income()

    def go_forward(self):
        """Go forward to the next state in the history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.income_data = self.history[self.history_index].copy()
            self.plot_income()

# ENABLE MOVEMENT
    def enable_move(self):
        """Enable panning of the plot."""
        self.canvas.get_tk_widget().configure(cursor="fleur")
        self.nav_toolbar.pan() 

# ENABLE ZOOM
    def enable_zoom(self):
        """Enable zoom functionality."""
        self.canvas.get_tk_widget().configure(cursor="cross")
        self.nav_toolbar.zoom() 

# TOGGLE GRID
    def toggle_grid(self):
        """Toggle the grid display on the graph."""
        self.grid_shown = not self.grid_shown
        self.ax.grid(self.grid_shown)
        self.canvas.draw()

# EDIT GRAPH TYPE
    def edit_graph_type(self):
        """Opens a window to edit the graph type."""
        graph_type_dialog = Toplevel(self.root)
        graph_type_dialog.title("Edit Graph Type")
        graph_type_dialog.geometry("300x350")

        Label(graph_type_dialog, text="Select Graph Type:").pack(pady=20)

        def set_graph_type(graph_type):
            self.graph_type = graph_type
            self.update_graph()  # Update the graph with the selected type
            graph_type_dialog.destroy()

        # Add buttons for each graph type
        Button(graph_type_dialog, text="Line Graph", command=lambda: set_graph_type("line")).pack(pady=5)
        Button(graph_type_dialog, text="Bar Graph", command=lambda: set_graph_type("bar")).pack(pady=5)
        Button(graph_type_dialog, text="Candlestick Chart", command=lambda: set_graph_type("candlestick")).pack(pady=5)
        Button(graph_type_dialog, text="Histogram", command=lambda: set_graph_type("histogram")).pack(pady=5)
        Button(graph_type_dialog, text="Area Chart", command=lambda: set_graph_type("area")).pack(pady=5)
        Button(graph_type_dialog, text="Spline Chart", command=lambda: set_graph_type("spline")).pack(pady=5)

# GRAPH RESIZING
    def resize_graph(self):
        """Resize the graph area in real-time."""
        resize_dialog = Toplevel(self.root)
        resize_dialog.title("Resize Graph")
        resize_dialog.geometry("300x300")

        Label(resize_dialog, text="Left Margin:").pack()
        left_scale = Scale(resize_dialog, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        left_scale.set(self.current_margins["left"])
        left_scale.pack()

        Label(resize_dialog, text="Right Margin:").pack()
        right_scale = Scale(resize_dialog, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        right_scale.set(self.current_margins["right"])
        right_scale.pack()

        Label(resize_dialog, text="Top Margin:").pack()
        top_scale = Scale(resize_dialog, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        top_scale.set(self.current_margins["top"])
        top_scale.pack()

        Label(resize_dialog, text="Bottom Margin:").pack()
        bottom_scale = Scale(resize_dialog, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        bottom_scale.set(self.current_margins["bottom"])
        bottom_scale.pack()

        # Update the graph as the user adjusts the scales
        def update_margins(event=None):
            """Update the margins and redraw the graph in real-time."""
            self.current_margins["left"] = left_scale.get()
            self.current_margins["right"] = right_scale.get()
            self.current_margins["top"] = top_scale.get()
            self.current_margins["bottom"] = bottom_scale.get()

            self.figure.subplots_adjust(left=self.current_margins["left"], right=self.current_margins["right"],
                                    top=self.current_margins["top"], bottom=self.current_margins["bottom"])
            self.canvas.draw()

        # Bind scale adjustments to real-time updates
        left_scale.bind("<Motion>", update_margins)
        right_scale.bind("<Motion>", update_margins)
        top_scale.bind("<Motion>", update_margins)
        bottom_scale.bind("<Motion>", update_margins)

# EDIT DATA
    def edit_income(self):
        """Allows the user to edit income data."""
        amount = simpledialog.askfloat("Edit Income", "Enter the new income amount:")
        if amount is not None:
            new_row = pd.DataFrame({"Period": [len(self.income_data) + 1], "Amount": [amount]})
            self.income_data = pd.concat([self.income_data, new_row], ignore_index=True)
            self.history.append(self.income_data.copy())
            self.history_index += 1
            self.update_graph()

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

    def plot_income(self):
        """Plots the income data."""
        self.ax.clear()  # Clear the previous plot

        if self.graph_type == "line":
            # Linear chart (line chart)
            self.ax.plot(self.income_data["Period"], self.income_data["Amount"], marker="o")
        
        elif self.graph_type == "candlestick":
            # Candlestick chart
            # Assuming you have 'Open', 'Close', 'High', and 'Low' columns in your data
            # Convert period to a datetime index if needed
            income_candlestick_data = self.income_data.copy()
            income_candlestick_data['Period'] = pd.to_datetime(income_candlestick_data['Period'])
            mpf.plot(income_candlestick_data.set_index('Period'), type='candle', ax=self.ax)

        elif self.graph_type == "bar":
            # Bar chart
            self.ax.bar(self.income_data["Period"], self.income_data["Amount"])
        
        elif self.graph_type == "histogram":
            # Histogram
            self.ax.hist(self.income_data["Amount"], bins=10, color='blue', alpha=0.7)
        
        elif self.graph_type == "area":
            # Area chart
            self.ax.fill_between(self.income_data["Period"], self.income_data["Amount"], color="skyblue", alpha=0.4)
            self.ax.plot(self.income_data["Period"], self.income_data["Amount"], color="Slateblue", alpha=0.6)

        elif self.graph_type == "spline":
            # Spline (smoothed line) chart
            x = np.arange(len(self.income_data["Period"]))
            z = np.polyfit(x, self.income_data["Amount"], 3)
            p = np.poly1d(z)
            self.ax.plot(self.income_data["Period"], p(x), color='green')

        # General configuration
        self.ax.set_title("Income Data")
        self.ax.set_xlabel("Period")
        self.ax.set_ylabel("Amount")

        # Rotate date labels if using datetime for Period
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45)

        self.canvas.draw()  # Update the plot on the canvas
# DONT TOUCH THIS
    def resize_icon(self, path, size):
        """Resizes an icon for the toolbar."""
        image = Image.open(path)
        image = image.resize(size, Image.Resampling.LANCZOS) 
        return ImageTk.PhotoImage(image)
    
# SAVE GRAPH TO EXCEL FILE
    def save_graph(self):
        """Save the income data and graph settings to an Excel file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                # Create an Excel writer
                with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                    # Save the income data
                    self.income_data.to_excel(writer, sheet_name="Income Data", index=False)
                
                # Save metadata (like graph type and theme) in a separate sheet
                    metadata = pd.DataFrame({
                        "Setting": ["GraphType", "Theme"],
                        "Value": [self.graph_type, self.current_theme]
                    })
                    metadata.to_excel(writer, sheet_name="Metadata", index=False)
                
                messagebox.showinfo("Success", "Data saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

# IMPORT EXCEL FILE
    def open_file(self):
        """Load the income data and graph settings from an Excel file."""
        file_path = filedialog.askopenfilename(title="Open Excel File", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                # Load the income data
                self.income_data = pd.read_excel(file_path, sheet_name="Income Data")
            
            # Load the metadata
                metadata = pd.read_excel(file_path, sheet_name="Metadata")
                self.graph_type = metadata.loc[metadata['Setting'] == 'GraphType', 'Value'].values[0]
                self.current_theme = metadata.loc[metadata['Setting'] == 'Theme', 'Value'].values[0]
            
                self.plot_income() 
            
                messagebox.showinfo("Success", "Data loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

# UPDATE GRAPH (DONT TOUCH)
    def update_graph(self):
        """Updates the graph with the current income data."""
        self.ax.clear()  # Clear the previous plot

        if not self.income_data.empty:
            if self.graph_type == "line":
                # Line chart
                self.income_data.plot(x="Period", y="Amount", ax=self.ax, legend=False, marker='o')

            elif self.graph_type == "bar":
                # Bar chart
                self.income_data.plot(kind="bar", x="Period", y="Amount", ax=self.ax, legend=False)

            elif self.graph_type == "candlestick":
                # Candlestick chart
                income_candlestick_data = self.income_data.copy()
                income_candlestick_data['Period'] = pd.to_datetime(income_candlestick_data['Period'])
                mpf.plot(income_candlestick_data.set_index('Period'), type='candle', ax=self.ax)

            elif self.graph_type == "histogram":
                # Histogram
                self.ax.hist(self.income_data["Amount"], bins=10, color='blue', alpha=0.7)

            elif self.graph_type == "area":
                # Area chart
                self.ax.fill_between(self.income_data["Period"], self.income_data["Amount"], color="skyblue", alpha=0.4)
                self.ax.plot(self.income_data["Period"], self.income_data["Amount"], color="Slateblue", alpha=0.6)

            elif self.graph_type == "spline":
                # Spline (smoothed line) chart
                x = np.arange(len(self.income_data["Period"]))
                z = np.polyfit(x, self.income_data["Amount"], 3)
                p = np.poly1d(z)
                self.ax.plot(self.income_data["Period"], p(x), color='green')

            # Set the title, axis labels
            self.ax.set_title("Income Data")
            self.ax.set_xlabel("Period")
            self.ax.set_ylabel("Amount")

            # Rotate date labels if using datetime for Period
            if pd.api.types.is_datetime64_any_dtype(self.income_data['Period']):
                self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                self.ax.xaxis.set_major_locator(mdates.MonthLocator())  # Adjust as necessary
                plt.xticks(rotation=45)

        self.canvas.draw()  # Update the canvas with the new plot

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenUtopiaFinanceApp(root)
    root.mainloop()
