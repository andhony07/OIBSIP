"""
BMI Calculator — Phase 2: Advanced Tier GUI Application
OASIS Infobyte Python Internship

Tkinter GUI featuring multi-user support, SQLite database persistence,
historical records table (Treeview), and Matplotlib trend visualization.
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from bmi_calculator import calculate_bmi, classify_bmi
import database


class BMICalculatorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("OASIS Infobyte — BMI Calculator & Tracker")
        self.root.geometry("820x700")
        self.root.minsize(780, 640)

        # Apply clean TTK theme
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure custom styles
        self._configure_styles()

        # Initialize database
        try:
            database.init_db()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")

        # Build UI layout
        self._create_widgets()

        # Populate user lists and history table
        self.refresh_users()
        self.refresh_history()

    def _configure_styles(self):
        """Sets up styles and color palettes for widgets."""
        self.style.configure("TFrame", background="#f5f7fa")
        self.style.configure("Card.TFrame", background="#ffffff", relief="solid", borderwidth=1)
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), background="#f5f7fa", foreground="#2c3e50")
        self.style.configure("SubHeader.TLabel", font=("Helvetica", 12, "bold"), background="#ffffff", foreground="#34495e")
        self.style.configure("TLabel", font=("Helvetica", 10), background="#ffffff", foreground="#2c3e50")
        self.style.configure("Bold.TLabel", font=("Helvetica", 10, "bold"), background="#ffffff", foreground="#2c3e50")
        self.style.configure("Status.TLabel", font=("Helvetica", 9, "italic"), background="#f5f7fa", foreground="#7f8c8d")

        self.style.configure("Primary.TButton", font=("Helvetica", 10, "bold"), background="#2980b9", foreground="#ffffff")
        self.style.map("Primary.TButton", background=[("active", "#3498db")])

        self.style.configure("Secondary.TButton", font=("Helvetica", 10, "bold"), background="#27ae60", foreground="#ffffff")
        self.style.map("Secondary.TButton", background=[("active", "#2ecc71")])

        self.style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#e0e6ed", foreground="#2c3e50")
        self.style.configure("Treeview", font=("Helvetica", 9), rowheight=24)

    def _create_widgets(self):
        """Constructs all GUI layout components."""
        # Main Container
        main_frame = ttk.Frame(self.root, style="TFrame", padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Banner
        title_label = ttk.Label(main_frame, text="BMI Calculator & Health Tracker", style="Header.TLabel")
        title_label.pack(anchor="w", pady=(0, 15))

        # Top Section: Input Card & Result Card
        top_frame = ttk.Frame(main_frame, style="TFrame")
        top_frame.pack(fill=tk.X, pady=(0, 15))

        # --- INPUT CARD (Left Side) ---
        input_card = ttk.Frame(top_frame, style="Card.TFrame", padding="15")
        input_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        ttk.Label(input_card, text="Calculate New BMI", style="SubHeader.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        # User Name Entry / Combobox
        ttk.Label(input_card, text="User Name:", style="Bold.TLabel").grid(row=1, column=0, sticky="w", pady=6)
        self.user_name_cb = ttk.Combobox(input_card, font=("Helvetica", 10), width=22)
        self.user_name_cb.grid(row=1, column=1, sticky="e", pady=6)

        # Weight Input
        ttk.Label(input_card, text="Weight (kg):", style="Bold.TLabel").grid(row=2, column=0, sticky="w", pady=6)
        self.weight_entry = ttk.Entry(input_card, font=("Helvetica", 10), width=24)
        self.weight_entry.grid(row=2, column=1, sticky="e", pady=6)

        # Height Input
        ttk.Label(input_card, text="Height (m):", style="Bold.TLabel").grid(row=3, column=0, sticky="w", pady=6)
        self.height_entry = ttk.Entry(input_card, font=("Helvetica", 10), width=24)
        self.height_entry.grid(row=3, column=1, sticky="e", pady=6)

        # Calculate Button
        calc_btn = ttk.Button(input_card, text="Calculate & Save BMI", style="Primary.TButton", command=self.on_calculate)
        calc_btn.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))

        # --- RESULT CARD (Right Side) ---
        self.result_card = ttk.Frame(top_frame, style="Card.TFrame", padding="15")
        self.result_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        ttk.Label(self.result_card, text="Calculation Result", style="SubHeader.TLabel").pack(anchor="w", pady=(0, 12))

        self.result_bmi_label = tk.Label(
            self.result_card,
            text="BMI: --",
            font=("Helvetica", 22, "bold"),
            bg="#ffffff",
            fg="#7f8c8d"
        )
        self.result_bmi_label.pack(pady=(10, 5))

        self.result_category_label = tk.Label(
            self.result_card,
            text="Category: Pending",
            font=("Helvetica", 12, "bold"),
            bg="#f0f3f4",
            fg="#7f8c8d",
            padx=12,
            pady=6,
            relief="solid",
            bd=1
        )
        self.result_category_label.pack(pady=(5, 10))

        # --- BOTTOM SECTION: HISTORICAL RECORDS & TREND GRAPH ---
        history_card = ttk.Frame(main_frame, style="Card.TFrame", padding="15")
        history_card.pack(fill=tk.BOTH, expand=True)

        # History Header & Controls
        hist_header_frame = ttk.Frame(history_card, style="TFrame")
        hist_header_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(hist_header_frame, text="Historical BMI Records", style="SubHeader.TLabel").pack(side=tk.LEFT)

        # Filter Control
        filter_frame = ttk.Frame(hist_header_frame, style="TFrame")
        filter_frame.pack(side=tk.RIGHT)

        ttk.Label(filter_frame, text="Filter User:", style="Bold.TLabel").pack(side=tk.LEFT, padx=(0, 5))
        self.filter_user_cb = ttk.Combobox(filter_frame, font=("Helvetica", 9), state="readonly", width=18)
        self.filter_user_cb.pack(side=tk.LEFT, padx=(0, 10))
        self.filter_user_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_history())

        trend_btn = ttk.Button(filter_frame, text="View BMI Trend Graph", style="Secondary.TButton", command=self.on_show_trend)
        trend_btn.pack(side=tk.LEFT)

        # History Treeview Table
        tree_frame = ttk.Frame(history_card, style="TFrame")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("recorded_at", "user_name", "weight", "height", "bmi", "category")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("recorded_at", text="Date / Time")
        self.tree.heading("user_name", text="User Name")
        self.tree.heading("weight", text="Weight (kg)")
        self.tree.heading("height", text="Height (m)")
        self.tree.heading("bmi", text="BMI")
        self.tree.heading("category", text="Category")

        self.tree.column("recorded_at", width=160, anchor="center")
        self.tree.column("user_name", width=140, anchor="w")
        self.tree.column("weight", width=100, anchor="center")
        self.tree.column("height", width=100, anchor="center")
        self.tree.column("bmi", width=90, anchor="center")
        self.tree.column("category", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Status Bar
        self.status_label = ttk.Label(main_frame, text="Ready", style="Status.TLabel")
        self.status_label.pack(anchor="w", pady=(10, 0))

    def refresh_users(self):
        """Fetches distinct user names from DB and updates user dropdown lists."""
        try:
            users = database.get_all_users()
            self.user_name_cb["values"] = users
            self.filter_user_cb["values"] = ["All Users"] + users
            if not self.filter_user_cb.get():
                self.filter_user_cb.set("All Users")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading user list: {e}")

    def refresh_history(self):
        """Loads records from database into Treeview based on current filter."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        selected_user = self.filter_user_cb.get()
        try:
            records = database.get_user_history(selected_user)
            for rec in records:
                self.tree.insert("", tk.END, values=rec)
            self.status_label.config(text=f"Loaded {len(records)} record(s) from database.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error loading history: {e}")

    def on_calculate(self):
        """Handles validation, calculation, color formatting, DB saving, and UI update."""
        user_name = self.user_name_cb.get().strip()
        weight_str = self.weight_entry.get().strip()
        height_str = self.height_entry.get().strip()

        # Validation 1: User Name
        if not user_name:
            messagebox.showerror("Validation Error", "Please enter or select a User Name.")
            return

        # Validation 2: Weight
        if not weight_str:
            messagebox.showerror("Validation Error", "Please enter weight in kilograms.")
            return
        try:
            weight = float(weight_str)
            if weight <= 0:
                messagebox.showerror("Validation Error", "Weight must be a positive number greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Validation Error", "Weight must be a valid numeric value.")
            return

        # Validation 3: Height
        if not height_str:
            messagebox.showerror("Validation Error", "Please enter height in meters.")
            return
        try:
            height = float(height_str)
            if height <= 0:
                messagebox.showerror("Validation Error", "Height must be a positive number greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Validation Error", "Height must be a valid numeric value.")
            return

        # Perform BMI calculation & classification
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        # Update Result Display with Color-Coding
        self._display_result(bmi, category)

        # Save to SQLite Database
        try:
            database.save_bmi_record(user_name, weight, height, bmi, category)
            self.refresh_users()
            self.filter_user_cb.set(user_name)
            self.refresh_history()
            self.status_label.config(text=f"Successfully calculated and saved record for '{user_name}'.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save record: {e}")

    def _display_result(self, bmi: float, category: str):
        """Formats and sets color coding for result widgets."""
        color_scheme = {
            "Underweight": {"bg": "#E3F2FD", "fg": "#0D47A1", "border": "#1976D2"},
            "Normal":      {"bg": "#E8F5E9", "fg": "#1B5E20", "border": "#388E3C"},
            "Overweight":  {"bg": "#FFF3E0", "fg": "#E65100", "border": "#F57C00"},
            "Obese":       {"bg": "#FFEBEE", "fg": "#B71C1C", "border": "#D32F2F"}
        }

        colors = color_scheme.get(category, {"bg": "#f0f3f4", "fg": "#2c3e50", "border": "#bdc3c7"})

        self.result_bmi_label.config(
            text=f"BMI: {bmi:.2f}",
            fg=colors["fg"]
        )

        self.result_category_label.config(
            text=f"Category: {category}",
            bg=colors["bg"],
            fg=colors["fg"]
        )

    def on_show_trend(self):
        """Plots Matplotlib line chart for selected user's historical BMI trends."""
        selected_user = self.filter_user_cb.get().strip()

        if selected_user == "All Users" or not selected_user:
            # If "All Users" is selected, default to the entry user or prompt selection
            current_entry_user = self.user_name_cb.get().strip()
            if current_entry_user and current_entry_user in self.user_name_cb["values"]:
                selected_user = current_entry_user
            else:
                messagebox.showinfo("Select User", "Please select a specific user from the 'Filter User' dropdown to view their BMI trend.")
                return

        try:
            records = database.get_user_history(selected_user)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to fetch history for graph: {e}")
            return

        if not records:
            messagebox.showinfo("No Records Found", f"No historical BMI records found for user '{selected_user}'.")
            return

        # Extract timestamps and BMI values
        timestamps = [rec[0] for rec in records]
        bmis = [rec[4] for rec in records]

        # Create Toplevel Window for embedded Matplotlib Plot
        top = tk.Toplevel(self.root)
        top.title(f"BMI Trend Graph — {selected_user}")
        top.geometry("700x500")

        fig, ax = plt.subplots(figsize=(7, 4.5), dpi=100)
        
        # Plot line chart
        ax.plot(timestamps, bmis, marker='o', color='#2980b9', linewidth=2, markersize=6, label="BMI")

        # Reference lines for categories
        ax.axhline(y=18.5, color='#3498db', linestyle='--', alpha=0.7, label='Underweight Threshold (18.5)')
        ax.axhline(y=25.0, color='#2ecc71', linestyle='--', alpha=0.7, label='Normal Threshold (25.0)')
        ax.axhline(y=30.0, color='#e74c3c', linestyle='--', alpha=0.7, label='Obese Threshold (30.0)')

        ax.set_title(f"BMI Progress Trend for {selected_user}", fontsize=14, fontweight='bold', pad=12)
        ax.set_xlabel("Recording Date / Time", fontsize=10, fontweight='bold')
        ax.set_ylabel("BMI Value", fontsize=10, fontweight='bold')
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='upper left', fontsize=8)
        fig.autofmt_xdate(rotation=30)

        # Embed Figure in Tkinter Window
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, top)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    root = tk.Tk()
    app = BMICalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
