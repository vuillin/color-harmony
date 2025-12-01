import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import threading

from color_utils import hex_to_rgb
from palette_generator import generate_harmonies, generate_random_palette
from image_extractor import extract_colors_from_image
from renderer import render_palette

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ColorHarmonyApp(ctk.CTk):
    """
    Main GUI Application class for Color Harmony Generator.
    Mimics a modern, Apple-like interface using CustomTkinter.
    """
    def __init__(self):
        super().__init__()

        self.title("Color Harmony Generator")
        self.geometry("1100x700")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="COLOR\nHARMONY", 
                                     font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_color_mode = ctk.CTkButton(self.sidebar_frame, text="From Color", 
                                          command=self.show_color_mode, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.btn_color_mode.grid(row=1, column=0, padx=20, pady=10)

        self.btn_image_mode = ctk.CTkButton(self.sidebar_frame, text="From Image", 
                                          command=self.show_image_mode, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.btn_image_mode.grid(row=2, column=0, padx=20, pady=10)

        self.btn_random_mode = ctk.CTkButton(self.sidebar_frame, text="Random", 
                                           command=self.run_random_mode, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.btn_random_mode.grid(row=3, column=0, padx=20, pady=10)

        self.content_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.current_palettes = {} 
        self.show_color_mode()

    def clear_content(self):
        """Removes all widgets from the main content area."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_color_mode(self):
        """Displays the From Color interface."""
        self.clear_content()
        self.current_palettes = {}

        title = ctk.CTkLabel(self.content_frame, text="Generate from Color", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)

        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(pady=10)

        self.hex_entry = ctk.CTkEntry(input_frame, placeholder_text="#3498db", width=200, height=40)
        self.hex_entry.pack(side="left", padx=10)

        generate_btn = ctk.CTkButton(input_frame, text="Generate", command=self.process_color_input, height=40)
        generate_btn.pack(side="left", padx=10)

    def show_image_mode(self):
        """Displays the From Image interface."""
        self.clear_content()
        self.current_palettes = {}

        title = ctk.CTkLabel(self.content_frame, text="Extract from Image", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)

        upload_btn = ctk.CTkButton(self.content_frame, text="Upload Image", command=self.process_image_input, height=40)
        upload_btn.pack(pady=10)

        self.image_preview_label = ctk.CTkLabel(self.content_frame, text="")
        self.image_preview_label.pack(pady=20)

    def run_random_mode(self):
        """Generates a random palette instantly."""
        self.clear_content()
        self.current_palettes = {}

        title = ctk.CTkLabel(self.content_frame, text="Random Aesthetic", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)

        colors = generate_random_palette()
        self.current_palettes["Random"] = colors
        self.display_palette_row("Random Aesthetic", colors)
        self.add_export_button()

    def process_color_input(self):
        """Handles HEX input processing."""
        hex_code = self.hex_entry.get()
        if not hex_code.startswith("#"):
            hex_code = "#" + hex_code
        
        try:
            # Validate hex
            hex_to_rgb(hex_code)
            
            harmonies = generate_harmonies(hex_code)
            self.current_palettes = harmonies
            
            # Clear previous results but keep header
            for widget in self.content_frame.winfo_children()[2:]: 
                widget.destroy()

            for name, colors in harmonies.items():
                self.display_palette_row(name, colors)
            
            self.add_export_button()

        except Exception:
            error_label = ctk.CTkLabel(self.content_frame, text="Invalid HEX Code", text_color="red")
            error_label.pack()

    def process_image_input(self):
        """Handles Image upload and processing."""
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.jpeg;*.png")])
        if not file_path:
            return

        # Show preview
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        self.image_preview_label.configure(image=ctk_img, text="")
        
        # Process (Threaded to prevent UI freeze)
        loading_label = ctk.CTkLabel(self.content_frame, text="Processing...")
        loading_label.pack()
        self.update()

        extracted_colors = extract_colors_from_image(file_path, num_colors=6)
        
        loading_label.destroy()
        
        if extracted_colors:
            self.current_palettes = {"Image Extracted": extracted_colors}
            self.display_palette_row("Dominant Colors", extracted_colors)
            self.add_export_button()

    def display_palette_row(self, title, colors):
        """Renders a single palette row visually."""
        frame = ctk.CTkFrame(self.content_frame, fg_color=("gray90", "gray20"), corner_radius=10)
        frame.pack(fill="x", padx=20, pady=10)

        lbl = ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14, weight="bold"))
        lbl.pack(anchor="w", padx=10, pady=(10, 5))

        color_container = ctk.CTkFrame(frame, fg_color="transparent")
        color_container.pack(fill="x", padx=10, pady=(0, 10))

        for color in colors:
            c_box = ctk.CTkFrame(color_container, width=80, height=50, fg_color=color, corner_radius=6)
            c_box.pack(side="left", padx=5, expand=True, fill="x")
            
            # Add HEX text with contrast
            text_col = "white"
            rgb = hex_to_rgb(color)
            if (rgb[0]*0.299 + rgb[1]*0.587 + rgb[2]*0.114) > 186:
                text_col = "black"
            
            c_lbl = ctk.CTkLabel(c_box, text=color, text_color=text_col, font=ctk.CTkFont(size=10))
            c_lbl.place(relx=0.5, rely=0.5, anchor="center")

    def add_export_button(self):
        """Adds a button to export all current palettes."""
        btn = ctk.CTkButton(self.content_frame, text="Export All to PNG", 
                          fg_color="#27ae60", hover_color="#2ecc71", 
                          command=self.export_all)
        btn.pack(pady=30)

    def export_all(self):
        """Calls the renderer to save files."""
        if not self.current_palettes:
            return
            
        for name, colors in self.current_palettes.items():
            render_palette(colors, name, output_folder="exports")
        
        done_lbl = ctk.CTkLabel(self.content_frame, text="Exported to /exports !", text_color="#27ae60")
        done_lbl.pack()