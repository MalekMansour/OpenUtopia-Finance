import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd

class FinanceToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tool")

        # Initialize income data
        self.income_data = pd.DataFrame(columns=["Period", "Amount"])

        # Set up toolbar
        self.setup_toolbar()

        # Set up matplotlib figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Matplotlib Navigation Toolbar
        self.nav_toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.nav_toolbar.update()

    def setup_toolbar(self):
        toolbar_frame = tk.Frame(self.root)
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)

        # Icons and buttons
        open_icon = tk.PhotoImage(file="icons/folder.png")
        home_icon = tk.PhotoImage(file="icons/home.png")
        back_icon = tk.PhotoImage(file="icons/back.png")
        forward_icon = tk.PhotoImage(file="icons/forward.png")
        move_icon = tk.PhotoImage(file="icons/move.png")
        zoom_icon = tk.PhotoImage(file="icons/zoom.png")
        subplot_icon = tk.PhotoImage(file="icons/subplot.png")
        graph_icon = tk.PhotoImage(file="icons/graph.png")
        edit_icon = tk.PhotoImage(file="icons/edit.png")
        theme_icon = tk.PhotoImage(file="icons/theme.png")
        save_icon = tk.PhotoImage(file="icons/save.png")

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

    # Toolbar functionalities
    def open_file(self):
        file_path = filedialog.askopenfilename(title="Select Graph File", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            img = plt.imread(file_path)
            self.ax.imshow(img)
            self.canvas.draw()

    def reset_view(self):
        self.ax.set_xlim(auto=True)
        self.ax.set_ylim(auto=True)
        self.canvas.draw()

    def go_back(self):
        # Implement go back functionality
        pass

    def go_forward(self):
        # Implement go forward functionality
        pass

    def enable_move(self):
        self.nav_toolbar.pan()
        messagebox.showinfo("Info", "Move mode activated")

    def enable_zoom(self):
        self.nav_toolbar.zoom()
        messagebox.showinfo("Info", "Zoom mode activated")

    def configure_subplots(self):
        self.nav_toolbar.configure_subplots()
    
    def edit_graph_type(self):
        # Let the user pick a graph type
        graph_types = ["Bar", "Line", "Candlestick"]
        choice = tk.simpledialog.askstring("Choose Graph Type", "Select graph type: " + ", ".join(graph_types))
        if choice in graph_types:
            # Implement graph type change functionality here
            pass

    def edit_income(self):
        # Edit income data
        self.add_income("New Period", 7000)
        self.plot_income()

    def change_theme(self):
        # Implement theme changing logic
        themes = ["Light", "Dark", "Solarized"]
        choice = tk.simpledialog.askstring("Choose Theme", "Select theme: " + ", ".join(themes))
        if choice:
            # Implement theme change here
            pass

    def save_graph(self):
        save_path = filedialog.asksaveasfilename(title="Save Graph", defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            self.figure.savefig(save_path)
            messagebox.showinfo("Saved", f"Graph saved to {save_path}")

    # Data handling and plotting
    def add_income(self, period, amount):
        new_data = pd.DataFrame({"Period": [period], "Amount": [amount]})
        self.income_data = pd.concat([self.income_data, new_data], ignore_index=True)

    def plot_income(self):
        self.ax.clear()
        self.ax.bar(self.income_data['Period'], self.income_data['Amount'], color='green')
        self.ax.set_xlabel('Period')
        self.ax.set_ylabel('Amount ($)')
        self.ax.set_title('Income Visualization')
        self.canvas.draw()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceToolApp(root)
    root.mainloop()
