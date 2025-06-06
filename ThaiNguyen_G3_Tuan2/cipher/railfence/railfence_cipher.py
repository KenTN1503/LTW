class RailFenceCipher:
    def __init__(self):
        pass
    
    def rail_fence_encrypt(self, plain_text, num_rails):
        if num_rails <= 1:
            return plain_text
            
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: down, -1: up
        
        for char in plain_text:
            rails[rail_index].append(char)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        
        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text
    
    def rail_fence_decrypt(self, cipher_text, num_rails):
        if num_rails <= 1:
            return cipher_text
            
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1
        
        # Calculate length of each rail
        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        
        # Distribute cipher text into rails
        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(list(cipher_text[start:start + length]))
            start += length
        
        # Reconstruct plain text
        plain_text = []
        rail_index = 0
        direction = 1
        
        for _ in range(len(cipher_text)):
            plain_text.append(rails[rail_index][0])
            rails[rail_index] = rails[rail_index][1:]
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        
        return ''.join(plain_text)