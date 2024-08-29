import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
from PIL import Image, ImageTk


class FinanceToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tool")

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

        # Keep track of graph type
        self.graph_type = "line"

        # History for back/forward functionality
        self.history = []
        self.history_index = -1

    def setup_toolbar(self):
        toolbar_frame = tk.Frame(self.root)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Icons and buttons with resized icons
        icon_size = (24, 24)  # Set desired icon size

        open_icon = self.resize_icon("icons/folder.png", icon_size)
        home_icon = self.resize_icon("icons/home.png", icon_size)
        back_icon = self.resize_icon("icons/back.png", icon_size)
        forward_icon = self.resize_icon("icons/forward.png", icon_size)
        move_icon = self.resize_icon("icons/move.png", icon_size)
        zoom_icon = self.resize_icon("icons/zoom.png", icon_size)
        subplot_icon = self.resize_icon("icons/subplot.png", icon_size)
        graph_icon = self.resize_icon("icons/graph.png", icon_size)
        edit_icon = self.resize_icon("icons/edit.png", icon_size)
        theme_icon = self.resize_icon("icons/theme.png", icon_size)
        save_icon = self.resize_icon("icons/save.png", icon_size)

        tk.Button(toolbar_frame, image=open_icon, command=self.open_file).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=home_icon, command=self.reset_view).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=back_icon, command=self.go_back).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=forward_icon, command=self.go_forward).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=move_icon, command=self.enable_move).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=zoom_icon, command=self.enable_zoom).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=subplot_icon, command=self.configure_subplots).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=graph_icon, command=self.edit_graph_type).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=edit_icon, command=self.edit_income).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=theme_icon, command=self.change_theme).pack(side=tk.LEFT, padx=2)
        tk.Button(toolbar_frame, image=save_icon, command=self.save_graph).pack(side=tk.LEFT, padx=2)

        # Store references to images so they aren't garbage collected
        self.icons = [open_icon, home_icon, back_icon, forward_icon, move_icon, zoom_icon,
                      subplot_icon, graph_icon, edit_icon, theme_icon, save_icon]

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
            self.income_data = self.income_data.append({"Period": len(self.income_data) + 1, "Amount": amount}, ignore_index=True)
            self.history.append(self.income_data.copy())
            self.history_index += 1
            self.update_graph()

    def change_theme(self):
        """Allows the user to change the theme."""
        options = ["Light", "Dark", "Solarized", "ggplot"]
        theme = simpledialog.askstring("Select Theme", f"Choose the theme: {', '.join(options)}")
        if theme:
            plt.style.use(theme.lower())
            self.update_graph()

    def save_graph(self):
        """Saves the current graph as an image file."""
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
        if save_path:
            self.figure.savefig(save_path)
            messagebox.showinfo("Info", f"Graph saved as {save_path}")

    def add_income_data(self):
        """Adds income data from the form to the dataset."""
        try:
            period = int(self.period_entry.get())
            amount = float(self.amount_entry.get())
            self.income_data = self.income_data.append({"Period": period, "Amount": amount}, ignore_index=True)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceToolApp(root)
    root.mainloop()
