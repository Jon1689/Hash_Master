import customtkinter
from hasher import HashProcessor
from tkinter import filedialog, messagebox

# ====================================================================
# I. CENTRALIZED CONSTANTS
# ====================================================================
TEXTBOX_WIDTH = 350
TEXTBOX_HEIGHT = 300
OUTPUT_WIDTH = 720
OUTPUT_HEIGHT = 90
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 850
COPY_BUTTON_WIDTH = 80

# ====================================================================
# II. CUSTOM FRAME: Hash_Selection
# ====================================================================
class Hash_Selection(customtkinter.CTkFrame):
    """Encapsulates the hash algorithm radio buttons."""
    def __init__(self, master, width=None, height=None):
        # Pass dismension to the parent frame constructor
        super().__init__(master, fg_color="transparent", width=width, height=height)

        self.hash_var = customtkinter.StringVar(value="SHA-224") # Set standard default
        values = ["SHA-224", "SHA-256", "SHA-384", "SHA-512", "Argon2"]

        # Configure grid for internal vertical centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure(len(values) + 2, weight=1)

        for i, value in enumerate(values):
            radiobutton = customtkinter.CTkRadioButton(
                self,
                text=value,
                value=value,
                variable=self.hash_var,
                font=("Times New Roman", 28)
            )
            # Stars at row i+2 to push buttons down for vertical centering
            radiobutton.grid(row=i + 2, column=0, padx=10, pady=(10, 0), sticky="w")

    def get_selected_hash(self) -> str:
        """Returns the currently selected hashing algorithm name."""
        return self.hash_var.get()

# ====================================================================
# III. MAIN APPLICATION CLASS
# ====================================================================
class HashMasterApp(customtkinter.CTk):
    """The main application window for the Hash Master tool."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Hash Master | Cybersecurity Integration Tool")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.grid_columnconfigure((0,1), weight=1)

        self.hasher = HashProcessor()
        self.file_path = customtkinter.StringVar(value="")

        self._create_widgets()
        self._setup_logic()
    
    # ----------------------------------------------------
    # Helper Methods for Widget Creation (Modularity)
    # ----------------------------------------------------

    def _create_widgets(self):
        """Initalizes and places all main application widgets."""

        # Row 0: Title
        self.title_label = customtkinter.CTkLabel(self, text="Hash Master", font=("Times New Roman", 60, "bold")).grid(row=0, column=0, padx=10, pady=(10, 20), columnspan=2)

        # Row 1: Instructions
        customtkinter.CTkLabel(self, text="Input Text to Hash:", font=("Times New Roman", 32)).grid(row=1, column=0, padx=10, pady=(10, 0))
        customtkinter.CTkLabel(self, text="Choose Hash to Use:", font=("Times New Roman", 32)).grid(row=1, column=1, padx=10, pady=(10, 0))

        # Row 2: Textbox and Hash Selection
        self.text_input = customtkinter.CTkTextbox(self, corner_radius=10, font=("Times New Roman", 25), width=TEXTBOX_WIDTH, height=TEXTBOX_HEIGHT)
        self.text_input.grid(row=2, column=0, padx=10, pady=(10, 10))

        self.hash_frame = Hash_Selection(self, width=TEXTBOX_WIDTH, height=TEXTBOX_HEIGHT)
        self.hash_frame.grid(row=2, column=1, padx=10, pady=(10, 10))

        # Row 3: File Control
        self._create_file_control_widgets(row=3)

        # Row 4: Hash Trigger Button
        self.hash_button = customtkinter.CTkButton(self, text="Hash Input", font=("Times New Roman", 36), height=60, corner_radius=10)
        self.hash_button.grid(row=4, column=0, columnspan=2, padx=10, pady=(20, 20))

        # Row 5: Output Control
        self._create_output_widgets(row_label=5, row_output=6)

    def _create_file_control_widgets(self, row: int):
        """Creates the file Upload button, path entry, and Clear button."""

        # Upload Button
        customtkinter.CTkButton(self, text="Upload File", font=("Times New Roman", 32), command=self._select_file, height=50, corner_radius=10).grid(row=row, column=0, padx=10, pady=(10, 5), sticky="ew")

        # Control Frame for Path Entry and Clear Button (Column 1)
        self.file_control_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.file_control_frame.grid(row=row, column=1, padx=10, pady=(10, 5), sticky="ew")
        self.file_control_frame.grid_columnconfigure(0, weight=1)

        # File Path Entry
        self.file_path_entry = customtkinter.CTkEntry(self.file_control_frame, textvariable=self.file_path, font=("Times New Roman", 18), width=TEXTBOX_WIDTH - 75, state="readonly")
        self.file_path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # Clear File Button
        customtkinter.CTkButton(self.file_control_frame, text="Clear", font=("Times New Roman", 18), command=self._clear_file_selection, width=70, height=38, corner_radius=10).grid(row=0, column=1, sticky="e")

    def _create_output_widgets(self, row_label: int, row_output: int):
        """Creates the Hashed Output label, textbox, and Copy button."""

        # Label
        customtkinter.CTkLabel(self, text="Hashed Output", font=("Times New Roman", 32)).grid(row=row_label, column=0, padx=10, pady=(10, 0), columnspan=2)

        # Control Frame for Output Textbox and Copy Button
        self.output_control_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.output_control_frame.grid(row=row_output, column=0, padx=10, pady=(10, 20), columnspan=2)
        self.output_control_frame.grid_columnconfigure(0, weight=1)

        # Output Textbox
        self.output_text = customtkinter.CTkTextbox(self.output_control_frame, corner_radius=10, font=("Times New Roman", 18), width=OUTPUT_WIDTH, height=OUTPUT_HEIGHT, state="disabled")
        self.output_text.grid(row=0, column=0, padx=(0, 10))

        # Copy-to-Clipboard Button
        customtkinter.CTkButton(self.output_control_frame, text="Copy", font=("Times New Roman", 18), command=self._copy_to_clipboard, height=40, width=COPY_BUTTON_WIDTH, corner_radius=10).grid(row=0, column=1)

    # ----------------------------------------------------
    # Logic and Command Methods
    # ----------------------------------------------------

    def _setup_logic(self):
        """Configures widget commands."""
        self.hash_button.configure(command=self.hash_text)

    def _select_file(self):
        """Opens a file dialog, sets the path, and disables text input."""
        file_path = filedialog.askopenfilename(title="Select a file to hash")

        if file_path:
            self.file_path.set(file_path)
            self.text_input.delete("1.0", "end")
            self.text_input.configure(state="disabled")
    
    def _clear_file_selection(self):
        """Clears the file path and re-enables text input."""
        self.file_path.set("")
        # UX: Re-enables text input when file selection is cleared
        self.text_input.configure(state="normal")

    def _copy_to_clipboard(self):
        """Copies the hash output to the system clipboard."""
        output = self.output_text.get("1.0", "end-1c").strip()

        if output and not output.startswith("Error"):
            self.clipboard_clear()
            self.clipboard_append(output)
            messagebox.showinfo("Copied!", "Hash successfully copied to clipboard.")
        else:
            messagebox.showerror("Cannot Copy", "The output is empty or contains an error message.")
    
    def hash_text(self):
        """Main hashing function: determines input type and calls the appropriate hasher method."""
        input_text = self.text_input.get("1.0", "end-1c").strip()
        file_path = self.file_path.get().strip()
        algorithm = self.hash_frame.get_selected_hash()

        result = ""
        
        if file_path:
            # HASH FILE PATH
            if algorithm in self.hasher.sha_hashes:
                result = self.hasher.hash_file(file_path, algorithm)
            else:
                result = f"Error: File hashing is only availble for SHA algorithms."
                
        elif input_text:
            # HASH TEXT INPUT
            result = self.hasher.hash_text(input_text, algorithm)

        else:
            result = f"Error: Input text box is empty and no file was selected."
        
        # Display the output
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.output_text.configure(state="disabled")

# ====================================================================
# IV. EXECUTION BLOCK
# ====================================================================
if __name__ == "__main__":
    app = HashMasterApp()
    app.mainloop()