import tkinter as tk
from tkinter import filedialog, messagebox

#enkripsi vigenere
def vigenere_encrypt(text, key):
    result = ""
    text = text.lower()
    key = key.lower()
    
    for i in range(len(text)):
        letter = text[i]
        if letter.isalpha():
            result += chr((ord(letter) + ord(key[i % len(key)]) - 2 * ord('a')) % 26 + ord('a'))
        else:
            result += letter
    return result

#dekripsi vigenere
def vigenere_decrypt(text, key):
    result = ""
    text = text.lower()
    key = key.lower()
    
    for i in range(len(text)):
        letter = text[i]
        if letter.isalpha():
            result += chr((ord(letter) - ord(key[i % len(key)]) + 26) % 26 + ord('a'))
        else:
            result += letter
    return result

#playfair enkripsi
def generate_playfair_matrix(key):
    key = key.lower().replace('j', 'i')
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    matrix = []
    used_chars = set()
    
    for char in key:
        if char not in used_chars and char in alphabet:
            used_chars.add(char)
            matrix.append(char)

    for char in alphabet:
        if char not in used_chars:
            used_chars.add(char)
            matrix.append(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(char, matrix):
    for row in range(5):
        if char in matrix[row]:
            return row, matrix[row].index(char)
    return None, None

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = text.lower().replace('j', 'i').replace(' ', '')
    
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] == text[i + 1]:
            text = text[:i + 1] + 'x' + text[i + 1:]
        i += 2
    if len(text) % 2 != 0:
        text += 'x'

    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        row_a, col_a = find_position(a, matrix)
        row_b, col_b = find_position(b, matrix)
        
        if row_a == row_b:
            result += matrix[row_a][(col_a + 1) % 5]
            result += matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            result += matrix[(row_a + 1) % 5][col_a]
            result += matrix[(row_b + 1) % 5][col_b]
        else:
            result += matrix[row_a][col_b]
            result += matrix[row_b][col_a]
    
    return result

#dekripsi untuk playfair
def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = text.lower().replace('j', 'i').replace(' ', '')
    
    result = ""
    for i in range(0, len(text), 2):
        a, b = text[i], text[i + 1]
        row_a, col_a = find_position(a, matrix)
        row_b, col_b = find_position(b, matrix)

        if row_a == row_b:
            result += matrix[row_a][(col_a - 1) % 5]
            result += matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            result += matrix[(row_a - 1) % 5][col_a]
            result += matrix[(row_b - 1) % 5][col_b]
        else:
            result += matrix[row_a][col_b]
            result += matrix[row_b][col_a]
    
    return result

#enkripsi untuk hill
def hill_encrypt(text, key_matrix):
    text = text.lower().replace(' ', '')
    if len(text) % 3 != 0:
        text += 'x' * (3 - len(text) % 3)

    encrypted = ""
    for i in range(0, len(text), 3):
        block = [ord(char) - ord('a') for char in text[i:i+3]]
        encrypted_block = [
            (key_matrix[0][0] * block[0] + key_matrix[0][1] * block[1] + key_matrix[0][2] * block[2]) % 26,
            (key_matrix[1][0] * block[0] + key_matrix[1][1] * block[1] + key_matrix[1][2] * block[2]) % 26,
            (key_matrix[2][0] * block[0] + key_matrix[2][1] * block[1] + key_matrix[2][2] * block[2]) % 26,
        ]
        encrypted += ''.join([chr(num + ord('a')) for num in encrypted_block])

    return encrypted

#dekripsi untuk hill 
def hill_decrypt(text, key_matrix):
    inv_key_matrix = [[7, 5, 3], [2, 4, 12], [9, 1, 6]] 
    decrypted = ""
    
    for i in range(0, len(text), 3):
        block = [ord(char) - ord('a') for char in text[i:i+3]]
        decrypted_block = [
            (inv_key_matrix[0][0] * block[0] + inv_key_matrix[0][1] * block[1] + inv_key_matrix[0][2] * block[2]) % 26,
            (inv_key_matrix[1][0] * block[0] + inv_key_matrix[1][1] * block[1] + inv_key_matrix[1][2] * block[2]) % 26,
            (inv_key_matrix[2][0] * block[0] + inv_key_matrix[2][1] * block[1] + inv_key_matrix[2][2] * block[2]) % 26,
        ]
        decrypted += ''.join([chr(num + ord('a')) for num in decrypted_block])

    return decrypted

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, file.read())

def process_text():
    text = input_text.get("1.0", tk.END).strip()
    key = key_entry.get().strip()

    if len(key) < 12:
        messagebox.showerror("Error", "Kunci min. 12 karakter")
        return

    cipher = cipher_choice.get()
    mode = mode_choice.get()
    
    if cipher == "Vigenere":
        if mode == "Enkripsi":
            result = vigenere_encrypt(text, key)
        else:
            result = vigenere_decrypt(text, key)
    elif cipher == "Playfair":
        if mode == "Enkripsi":
            result = playfair_encrypt(text, key)
        else:
            result = playfair_decrypt(text, key)
    elif cipher == "Hill":
        key_matrix = [[2, 4, 12], [9, 1, 6], [7, 5, 3]]
        if mode == "Enkripsi":
            result = hill_encrypt(text, key_matrix)
        else:
            result = hill_decrypt(text, key_matrix)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

root = tk.Tk()
root.title("Cipher Program")
root.configure(bg="gray")

cipher_choice = tk.StringVar(value="Vigenere")
mode_choice = tk.StringVar(value="Enkripsi")

tk.Label(root, text="Pilih Cipher:", bg="gray").grid(row=0, column=0, sticky='w', padx=10, pady=5)
tk.OptionMenu(root, cipher_choice, "Vigenere", "Playfair", "Hill").grid(row=0, column=1, sticky='w', padx=10, pady=5)

tk.Label(root, text="Pilih Mode:", bg="gray").grid(row=1, column=0, sticky='w', padx=10, pady=5)
tk.OptionMenu(root, mode_choice, "Enkripsi", "Dekripsi").grid(row=1, column=1, sticky='w', padx=10, pady=5)

tk.Label(root, text="Kunci min. 12 karakter:", bg="gray").grid(row=2, column=0, sticky='w', padx=10, pady=5)
key_entry = tk.Entry(root)
key_entry.grid(row=2, column=1, sticky='w', padx=10, pady=5)

tk.Label(root, text="Input Teks:", bg="gray").grid(row=3, column=0, sticky='w', padx=10, pady=5)
input_text = tk.Text(root, height=5, width=50)
input_text.grid(row=3, column=1, sticky='w', padx=10, pady=5)

tk.Button(root, text="Pilih File", command=load_file).grid(row=4, column=0, sticky='w', padx=10, pady=5)
tk.Button(root, text="Proses", command=process_text).grid(row=4, column=1, sticky='w', padx=10, pady=5)

tk.Label(root, text="Hasil:", bg="gray").grid(row=5, column=0, sticky='w', padx=10, pady=5)
output_text = tk.Text(root, height=5, width=50)
output_text.grid(row=5, column=1, sticky='w', padx=10, pady=5)

root.mainloop()