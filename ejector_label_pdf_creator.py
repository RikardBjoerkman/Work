import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
import os
import webbrowser
from PIL import Image, ImageTk

# Function to create PDF labels with serial numbers, date, and product type
def create_labels(serial_numbers, date, product_type):
    c = canvas.Canvas("labels.pdf", pagesize=A4)  # Create a PDF file with A4 page size
    width, height = A4

    # Label dimensions in points
    label_width = 180.08  # Width of the label in points (63.5 mm)
    label_height = 107.64  # Height of the label in points (38.1 mm)

    # Margin and spacing
    margin = 56.7  # Margin from the edges of the page
    x_spacing = 5.67  # Horizontal spacing between labels in points (2 mm)
    y_spacing = 0  # Vertical spacing between labels in points (0 mm)

    # Calculate number of labels per row and column
    labels_per_row = 3
    labels_per_column = 7  # 18 labels / 3 labels per row

    try:
        # Register Arial font for the PDF
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))  # Ensure 'Arial.ttf' is available in your directory
        c.setFont("Arial", 18)  # Set font to Arial, size 10
    except Exception as e:
        messagebox.showerror("Font Error", "Arial font not found. Ensure 'Arial.ttf' is in the directory.")
        return

    # Loop through the list of serial numbers and place each label on the PDF
    for index, serial in enumerate(serial_numbers):
        row = index // labels_per_row  # Determine the row position
        col = index % labels_per_row   # Determine the column position
        x = margin + col * (label_width + x_spacing)
        y = height - margin - (row + 1) * (label_height + y_spacing)

        # Draw text on the PDF
        c.drawString(x + 10, y + label_height - 20, f"#{serial}")  # Serial number
        c.drawString(x + 10, y + label_height - 40, f"Typ {product_type}")  # Product type
        c.drawString(x + 10, y + label_height - 60, date)  # Date

    c.save()  # Save the PDF file

    # Open the PDF file using the default viewer
    webbrowser.open_new("labels.pdf")

# Function to generate and display the PDF based on user input
def generate_and_display_pdf():
    try:
        # Retrieve input values
        date = date_entry.get().strip()
        product_type = product_type_entry.get().strip()
        num_labels = num_labels_var.get()

        # Validate number of labels
        try:
            num_labels = int(num_labels)
        except ValueError:
            raise ValueError("Number of labels must be a valid integer.")

        # Validate required fields
        if not date or not product_type:
            raise ValueError("Date and Product Type cannot be empty.")
        if num_labels <= 0:
            raise ValueError("Number of labels must be greater than 0.")

        # Generate serial numbers
        if auto_radio_var.get() == "auto":
            try:
                serial_start = int(serial_start_entry.get().strip())
                serial_numbers = [str(serial_start + i) for i in range(num_labels)]
            except ValueError:
                raise ValueError("Starting Serial Number must be a valid integer.")
        else:
            serial_numbers = [entry.get().strip() for entry in manual_entries]
            if any(not sn for sn in serial_numbers):
                raise ValueError("Please provide all serial numbers.")

        # Check if the number of serial numbers matches the number of labels
        if len(serial_numbers) != num_labels:
            raise ValueError(f"Number of serial numbers does not match the number of labels ({num_labels}).")

        # Provide feedback during PDF creation
        messagebox.showinfo("Generating PDF", "PDF has been! Press OK to continue.")
        
        # Create PDF labels
        create_labels(serial_numbers, date, product_type)

    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to update the manual entry fields based on the number of labels
def update_manual_entries(*args):
    try:
        num_labels = int(num_labels_var.get())
        
        # Ensure at least one entry field
        num_labels = max(1, num_labels)
        
        # Clear existing manual entry widgets
        for widget in manual_entries_frame.winfo_children():
            widget.destroy()
        
        global manual_entries
        manual_entries = []
        for i in range(num_labels):
            entry = tk.Entry(manual_entries_frame, width=50, bg="#feffff")
            entry.grid(row=i, column=0, padx=10, pady=5)
            manual_entries.append(entry)

        # Bind navigation keys for focus movement
        for entry in manual_entries:
            entry.bind("<Up>", move_focus_up)
            entry.bind("<Down>", move_focus_down)

    except ValueError:
        pass

# Function to move focus to the previous manual entry field
def move_focus_up(event):
    current_widget = event.widget
    current_index = manual_entries.index(current_widget)
    if current_index > 0:
        manual_entries[current_index - 1].focus_set()

# Function to move focus to the next manual entry field
def move_focus_down(event):
    current_widget = event.widget
    current_index = manual_entries.index(current_widget)
    if current_index < len(manual_entries) - 1:
        manual_entries[current_index + 1].focus_set()

# Function to handle the selection of the "Auto Generate" radio button
def on_auto_radio_selected():
    manual_entries_frame.grid_forget()
    serial_start_entry.grid(row=0, column=1, padx=10, pady=5)
    update_manual_entries()

# Function to handle the selection of the "Manual Entry" radio button
def on_manual_radio_selected():
    serial_start_entry.grid_forget()
    manual_entries_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
    update_manual_entries()

# Initialize the main application window
app = ThemedTk()
app.set_theme("arc")
app.title("Ejector Label PDF Creator")

# Load and set the application icon
try:
    logo_image = tk.PhotoImage(file="mycronic_logo.png")
    app.iconphoto(True, logo_image)
except tk.TclError:
    print("Failed to load logo image. Ensure the image file is in the correct format and location.")

# Configure the style for the application
style = ttk.Style()
style.configure("TCombobox",
                font=("Arial", 12),
                padding=5,
                relief="flat",
                background="#feffff",
                foreground="#0087be")
style.configure("TLabel",
                font=("Arial", 12, "bold"),
                background="#0087be",  # Set label background color
                foreground="#fffeff")  # Set label text color
style.configure("TRadiobutton",
                font=("Arial", 12, "bold"),
                background="#feffff",
                foreground="#0087be")
style.configure("TEntry",
                font=("Arial", 12),
                padding=5,
                relief="flat",
                background="#feffff",
                foreground="#0087be")

auto_radio_var = tk.StringVar(value="auto")  # Variable to track selected radio button value

# Create frames for layout
main_frame = tk.Frame(app, padx=20, pady=20, bg="#feffff")  # Main frame with background color
main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Logo Frame
logo_frame = tk.Frame(main_frame, bg="#feffff")
logo_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Load and display the large logo
try:
    logo_img = Image.open("mycronic RGB.png")
    logo_img = logo_img.resize(
        (500, int(logo_img.height * (500 / logo_img.width))), 
        Image.LANCZOS
    )
    logo_img_tk = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(logo_frame, image=logo_img_tk, bg="#feffff")
    logo_label.image = logo_img_tk
    logo_label.pack(fill="x")
except Exception as e:
    print(f"Failed to load or resize large logo image: {e}")

# Input Details Frame
input_frame = tk.LabelFrame(main_frame, text="Input Details", padx=10, pady=10, font=("Arial", 14, "bold"), bg="#0087be", fg="#fffeff", relief="solid")
input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Labels and Entry Widgets
tk.Label(input_frame, text="Starting Serial Number:", bg="#0087be", fg="#fffeff", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
serial_start_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#feffff", fg="#0087be")
serial_start_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg="#0087be", fg="#fffeff", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
date_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#feffff", fg="#0087be")
date_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Product Type:", bg="#0087be", fg="#fffeff", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
product_type_entry = tk.Entry(input_frame, font=("Arial", 12), bg="#feffff", fg="#0087be")
product_type_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Number of Labels:", bg="#0087be", fg="#fffeff", font=("Arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky="w")
num_labels_var = tk.StringVar()
num_labels_entry = tk.Entry(input_frame, textvariable=num_labels_var, font=("Arial", 12), bg="#feffff", fg="#0087be")
num_labels_entry.grid(row=3, column=1, padx=10, pady=5)
num_labels_var.trace_add("write", update_manual_entries)

# Radio Buttons for Auto Generate and Manual Entry
tk.Radiobutton(input_frame, text="Auto Generate", variable=auto_radio_var, value="auto", command=on_auto_radio_selected, bg="#feffff", fg="#0087be", font=("Arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=5, sticky="w")
tk.Radiobutton(input_frame, text="Manual Entry", variable=auto_radio_var, value="manual", command=on_manual_radio_selected, bg="#feffff", fg="#0087be", font=("Arial", 12, "bold")).grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Manual Entries Frame (initially hidden)
manual_entries_frame = tk.Frame(main_frame, bg="#feffff")

# Button to generate PDF
generate_button = ttk.Button(main_frame, text="Generate PDF", command=generate_and_display_pdf)
generate_button.grid(row=6, column=0, padx=10, pady=10)

# Start the main application loop
app.mainloop()