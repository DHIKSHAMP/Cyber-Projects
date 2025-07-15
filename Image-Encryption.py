import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import hashlib
import random
import pickle
import os

# ---------------- Encryption & Decryption Functions ---------------- #

def generate_seed(key):
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % (10 ** 8)

def encrypt_image(input_image_path, output_bin_path, key):
    img = Image.open(input_image_path).convert('RGB')
    img_array = np.array(img)
    original_shape = img_array.shape

    flat_array = img_array.reshape(-1, 3)
    seed = generate_seed(key)
    random.seed(seed)

    indices = list(range(len(flat_array)))
    random.shuffle(indices)

    shuffled = flat_array[indices]
    encrypted_pixels = (shuffled + seed % 256) % 256

    with open(output_bin_path, 'wb') as f:
        pickle.dump({
            'data': encrypted_pixels,
            'indices': indices,
            'shape': original_shape
        }, f)

def decrypt_image(input_bin_path, output_image_path, key):
    with open(input_bin_path, 'rb') as f:
        encrypted = pickle.load(f)

    seed = generate_seed(key)
    encrypted_pixels = encrypted['data']
    indices = encrypted['indices']
    original_shape = encrypted['shape']
    decrypted_pixels = (encrypted_pixels - seed % 256) % 256

    flat_array = np.zeros_like(decrypted_pixels)
    for i, idx in enumerate(indices):
        flat_array[idx] = decrypted_pixels[i]

    img_array = flat_array.reshape(original_shape)
    img = Image.fromarray(img_array.astype('uint8'))
    img.save(output_image_path)

# ---------------- GUI Application ---------------- #

class ImageEncryptorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Image Encryptor/Decryptor")
        self.geometry("700x500")
        ctk.set_appearance_mode("dark")

        self.file_path = ""
        self.key = ctk.StringVar()

        # Background image (static, local)
        self.bg_image = ctk.CTkImage(Image.open("bg.jpg"), size=(700, 500))
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(relx=0.5, rely=0.5, anchor="center")

        self.create_widgets()

    def create_widgets(self):
        container = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="🛡️ Image Encryption Tool", font=("Arial", 22, "bold")).pack(pady=15)

        ctk.CTkButton(container, text="Choose File", command=self.browse_file,
                      fg_color="red", hover_color="#cc0000", corner_radius=10).pack(pady=10)

        self.file_label = ctk.CTkLabel(container, text="No file selected", wraplength=500)
        self.file_label.pack(pady=5)

        key_frame = ctk.CTkFrame(container, fg_color="transparent")
        key_frame.pack(pady=10)

        ctk.CTkLabel(key_frame, text="Enter Key:").pack(side="left", padx=(0, 10))
        self.key_entry = ctk.CTkEntry(key_frame, placeholder_text="Secret key", textvariable=self.key, width=200)
        self.key_entry.pack(side="left")

        ctk.CTkButton(key_frame, text="Clear Key", width=80, command=self.clear_key,
                      fg_color="red", hover_color="#cc0000", corner_radius=10).pack(side="left", padx=10)

        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Encrypt", command=self.encrypt,
                      fg_color="red", hover_color="#cc0000", corner_radius=10).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Decrypt", command=self.decrypt,
                      fg_color="red", hover_color="#cc0000", corner_radius=10).pack(side="left", padx=10)

    def browse_file(self):
        filetypes = [("Image or Encrypted Files", "*.png *.jpg *.jpeg *.bmp *.bin"), ("All files", "*.*")]
        self.file_path = filedialog.askopenfilename(title="Select File", filetypes=filetypes)
        self.file_label.configure(text=self.file_path if self.file_path else "No file selected")

    def encrypt(self):
        if not self.file_path or not self.key.get():
            messagebox.showerror("Error", "Please select a file and enter a key.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Binary files", "*.bin")])
        if save_path:
            try:
                encrypt_image(self.file_path, save_path, self.key.get())
                messagebox.showinfo("Success", f"Encrypted file saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def decrypt(self):
        if not self.file_path or not self.key.get():
            messagebox.showerror("Error", "Please select a file and enter a key.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if save_path:
            try:
                decrypt_image(self.file_path, save_path, self.key.get())
                messagebox.showinfo("Success", f"Decrypted image saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def clear_key(self):
        self.key.set("")

# ---------------- Run Application ---------------- #

if __name__ == "__main__":
    app = ImageEncryptorApp()
    app.mainloop()
