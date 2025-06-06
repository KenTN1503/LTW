class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        if not text:
            return ""
        if not isinstance(key, int) or key <= 0:
            raise ValueError("Khóa phải là số nguyên dương")
        if key > len(text):
            raise ValueError("Khóa không được lớn hơn độ dài văn bản")

        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text

    def decrypt(self, text, key):
        if not text:
            return ""
        if not isinstance(key, int) or key <= 0:
            raise ValueError("Khóa phải là số nguyên dương")
        if key > len(text):
            raise ValueError("Khóa không được lớn hơn độ dài văn bản")

        # Tính số hàng và cột
        num_rows = (len(text) + key - 1) // key  # Số hàng cần thiết
        num_cols = key
        num_short_cols = key - (len(text) % key or key)  # Số cột ngắn hơn
        short_col_length = num_rows - 1 if num_short_cols > 0 else num_rows

        # Khởi tạo lưới giải mã
        grid = [''] * key
        pos = 0

        # Phân phối ký tự vào các cột
        for col in range(key):
            rows = num_rows if col < num_cols - num_short_cols else short_col_length
            grid[col] = text[pos:pos + rows]
            pos += rows

        # Đọc lại theo hàng
        decrypted_text = ''
        for row in range(num_rows):
            for col in range(key):
                if row < len(grid[col]):
                    decrypted_text += grid[col][row]
        
        return decrypted_text