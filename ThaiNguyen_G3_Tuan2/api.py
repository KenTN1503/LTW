from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

# CAESAR CIPHER ALGORITHM
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    try:
        data = request.json
        plain_text = data['plain_text']
        key = int(data['key'])
        encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
        return jsonify({'encrypted_message': encrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    try:
        data = request.json
        cipher_text = data['cipher_text']
        key = int(data['key'])
        decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
        return jsonify({'decrypted_message': decrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# VIGENERE CIPHER ALGORITHM
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    try:
        data = request.json
        plain_text = data['plain_text']
        key = data['key']
        encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    try:
        data = request.json
        cipher_text = data['cipher_text']
        key = data['key']
        decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# RAILFENCE CIPHER ALGORITHM
railfence_cipher = RailFenceCipher()

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    try:
        data = request.json
        plain_text = data['plain_text']
        num_rails = int(data['num_rails'])
        
        if num_rails <= 1:
            return jsonify({'error': 'Số rail phải lớn hơn 1'}), 400
            
        encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, num_rails)
        return jsonify({'encrypted_text': encrypted_text})
    except KeyError as e:
        return jsonify({'error': f'Thiếu trường bắt buộc: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': 'num_rails phải là số nguyên hợp lệ'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    try:
        data = request.json
        cipher_text = data['cipher_text']
        num_rails = int(data['num_rails'])
        
        if num_rails <= 1:
            return jsonify({'error': 'Số rail phải lớn hơn 1'}), 400
            
        decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, num_rails)
        return jsonify({'decrypted_text': decrypted_text})
    except KeyError as e:
        return jsonify({'error': f'Thiếu trường bắt buộc: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': 'num_rails phải là số nguyên hợp lệ'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PLAYFAIR CIPHER ALGORITHM
playfair_cipher = PlayFairCipher()

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    try:
        data = request.json
        plain_text = data['plain_text']
        key = data['key']
        
        if not key:
            return jsonify({'error': 'Khóa không được để trống'}), 400
            
        matrix = playfair_cipher.create_playfair_matrix(key)
        encrypted_text = playfair_cipher.playfair_encrypt(plain_text, matrix)
        return jsonify({'encrypted_text': encrypted_text})
    except KeyError as e:
        return jsonify({'error': f'Thiếu trường bắt buộc: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    try:
        data = request.json
        cipher_text = data['cipher_text']
        key = data['key']
        
        if not key:
            return jsonify({'error': 'Khóa không được để trống'}), 400
            
        matrix = playfair_cipher.create_playfair_matrix(key)
        decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, matrix)
        return jsonify({'decrypted_text': decrypted_text})
    except KeyError as e:
        return jsonify({'error': f'Thiếu trường bắt buộc: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# TRANSPOSITION CIPHER ALGORITHM
transposition_cipher = TranspositionCipher()

@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    try:
        data = request.json
        plain_text = data['plain_text']
        key = int(data['key'])
        
        if key <= 0:
            return jsonify({'error': 'Khóa phải là số nguyên dương'}), 400
            
        encrypted_text = transposition_cipher.encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except KeyError as e:
        return jsonify({'error': f'Thiếu trường bắt buộc: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    try:
        data = request.json
        cipher_text = data['cipher_text']
        key = int(data['key'])
        
        if key <= 0:
            return jsonify({'error': 'Khóa phải là số nguyên dương'}), 400
            
        decrypted_text = transposition_cipher.decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except KeyError as e:
        return jsonify({'error': f'Thiếu trường bắt buộc: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint để lấy thông tin về các cipher có sẵn
@app.route('/api/ciphers', methods=['GET'])
def get_available_ciphers():
    ciphers = {
        'caesar': {
            'name': 'Caesar Cipher',
            'description': 'Dịch chuyển mỗi chữ cái một số vị trí cố định',
            'endpoints': {
                'encrypt': '/api/caesar/encrypt',
                'decrypt': '/api/caesar/decrypt'
            },
            'parameters': {
                'plain_text/cipher_text': 'chuỗi',
                'key': 'số nguyên (giá trị dịch chuyển)'
            }
        },
        'vigenere': {
            'name': 'Vigenere Cipher',
            'description': 'Sử dụng từ khóa để dịch chuyển các chữ cái với các khoảng cách khác nhau',
            'endpoints': {
                'encrypt': '/api/vigenere/encrypt',
                'decrypt': '/api/vigenere/decrypt'
            },
            'parameters': {
                'plain_text/cipher_text': 'chuỗi',
                'key': 'chuỗi (từ khóa)'
            }
        },
        'railfence': {
            'name': 'Rail Fence Cipher',
            'description': 'Viết văn bản theo mô hình zigzag trên nhiều rail',
            'endpoints': {
                'encrypt': '/api/railfence/encrypt',
                'decrypt': '/api/railfence/decrypt'
            },
            'parameters': {
                'plain_text/cipher_text': 'chuỗi',
                'num_rails': 'số nguyên (số rail, phải > 1)'
            }
        },
        'playfair': {
            'name': 'Playfair Cipher',
            'description': 'Mã hóa các cặp chữ cái bằng ma trận 5x5 được tạo từ từ khóa',
            'endpoints': {
                'encrypt': '/api/playfair/encrypt',
                'decrypt': '/api/playfair/decrypt'
            },
            'parameters': {
                'plain_text/cipher_text': 'chuỗi',
                'key': 'chuỗi (từ khóa)'
            }
        },
        'transposition': {
            'name': 'Transposition Cipher',
            'description': 'Sắp xếp lại các ký tự theo số cột được xác định bởi khóa',
            'endpoints': {
                'encrypt': '/api/transposition/encrypt',
                'decrypt': '/api/transposition/decrypt'
            },
            'parameters': {
                'plain_text/cipher_text': 'chuỗi',
                'key': 'số nguyên (số cột, phải > 0)'
            }
        }
    }
    return jsonify(ciphers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)