class PlayFairCipher:
    def __init__(self) -> None:
        """Initialize the Playfair Cipher class."""
        pass

    def create_playfair_matrix(self, key: str) -> list:
        """Create a 5x5 Playfair matrix from the given key."""
        # Replace 'J' with 'I' and convert to uppercase
        key = key.replace("J", "I").upper()
        # Validate key
        if not all(c.isalpha() for c in key):
            raise ValueError("Key must contain only letters")
        
        # Remove duplicates while preserving order
        key_set = []
        for c in key:
            if c not in key_set:
                key_set.append(c)
        
        # Create matrix with key and remaining letters
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Excludes J
        remaining_letters = [letter for letter in alphabet if letter not in key_set]
        matrix = key_set + remaining_letters[:25 - len(key_set)]
        
        # Ensure matrix has exactly 25 letters
        if len(matrix) != 25:
            raise ValueError("Matrix must contain exactly 25 unique letters")
        
        # Convert to 5x5 grid
        return [matrix[i:i+5] for i in range(0, 25, 5)]

    def find_letter_coords(self, matrix: list, letter: str) -> tuple:
        """Find the row and column of a letter in the matrix."""
        letter = letter.upper().replace("J", "I")
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        raise ValueError(f"Letter {letter} not found in matrix")

    def playfair_encrypt(self, plain_text: str, matrix: list) -> str:
        """Encrypt the plaintext using the Playfair cipher."""
        # Validate and preprocess input
        plain_text = plain_text.replace("J", "I").upper()
        if not all(c.isalpha() for c in plain_text):
            raise ValueError("Plaintext must contain only letters")
        
        # Prepare digraphs
        prepared_text = ""
        i = 0
        while i < len(plain_text):
            prepared_text += plain_text[i]
            if i + 1 < len(plain_text):
                if plain_text[i] == plain_text[i + 1]:
                    prepared_text += "X"  # Insert X between identical letters
                else:
                    prepared_text += plain_text[i + 1]
                    i += 1
            else:
                prepared_text += "X"  # Pad with X for odd length
            i += 1
        
        # Encrypt digraphs
        encrypted_text = ""
        for i in range(0, len(prepared_text), 2):
            pair = prepared_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:  # Same row
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Same column
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:  # Rectangle
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        return encrypted_text

    def playfair_decrypt(self, cipher_text: str, matrix: list) -> str:
        """Decrypt the ciphertext using the Playfair cipher."""
        # Validate and preprocess input
        cipher_text = cipher_text.replace("J", "I").upper()
        if not all(c.isalpha() for c in cipher_text):
            raise ValueError("Ciphertext must contain only letters")
        if len(cipher_text) % 2 != 0:
            raise ValueError("Ciphertext length must be even")
        
        # Decrypt digraphs
        decrypted_text = ""
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:  # Same row
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Same column
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:  # Rectangle
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
        
        # Remove padding 'X' characters
        result = ""
        i = 0
        while i < len(decrypted_text):
            if i + 1 < len(decrypted_text) and decrypted_text[i + 1] == "X":
                # Check if X is padding (between identical letters or at end)
                if i + 2 < len(decrypted_text) and decrypted_text[i] == decrypted_text[i + 2]:
                    result += decrypted_text[i]
                    i += 2  # Skip the X
                else:
                    result += decrypted_text[i:i+2]
                    i += 2
            else:
                result += decrypted_text[i]
                i += 1
        
        return result