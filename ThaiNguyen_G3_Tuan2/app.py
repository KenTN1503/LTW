from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/caesar", methods=["POST"])
def caesar():
    caesar_result = ""
    caesar_action = request.form.get("action")
    caesar_text = request.form.get("text", "")
    caesar_key = int(request.form.get("key", 0))
    
    cipher = CaesarCipher()
    
    try:
        if caesar_action == "encrypt_caesar":
            caesar_result = cipher.encrypt_text(caesar_text, caesar_key)
        elif caesar_action == "decrypt_caesar":
            caesar_result = cipher.decrypt_text(caesar_text, caesar_key)
    except Exception as e:
        caesar_result = f"Lỗi: {str(e)}"
    
    return render_template("index.html", 
                         caesar_result=caesar_result,
                         caesar_text=caesar_text,
                         caesar_key=caesar_key,
                         caesar_action=caesar_action)

@app.route("/vigenere", methods=["POST"])
def vigenere():
    vigenere_result = ""
    vigenere_action = request.form.get("action")
    vigenere_text = request.form.get("text", "")
    vigenere_key = request.form.get("key", "").strip()
    
    if not vigenere_key:
        vigenere_result = "Lỗi: Vui lòng nhập khóa cho Vigenere cipher!"
    else:
        cipher = VigenereCipher()
        
        try:
            if vigenere_action == "encrypt_vigenere":
                vigenere_result = cipher.vigenere_encrypt(vigenere_text, vigenere_key)
            elif vigenere_action == "decrypt_vigenere":
                vigenere_result = cipher.vigenere_decrypt(vigenere_text, vigenere_key)
        except Exception as e:
            vigenere_result = f"Lỗi: {str(e)}"
    
    return render_template("index.html",
                         vigenere_result=vigenere_result,
                         vigenere_text=vigenere_text,
                         vigenere_action=vigenere_action,
                         vigenere_key=vigenere_key)

@app.route("/railfence", methods=["POST"])
def railfence():
    railfence_result = ""
    railfence_action = request.form.get("action")
    railfence_text = request.form.get("text", "")
    
    try:
        railfence_rails = int(request.form.get("rails", 2))
    except ValueError:
        railfence_rails = 2
    
    if railfence_rails <= 1:
        railfence_result = "Lỗi: Số rail phải lớn hơn 1!"
    else:
        cipher = RailFenceCipher()
        
        try:
            if railfence_action == "encrypt_railfence":
                railfence_result = cipher.rail_fence_encrypt(railfence_text, railfence_rails)
            elif railfence_action == "decrypt_railfence":
                railfence_result = cipher.rail_fence_decrypt(railfence_text, railfence_rails)
        except Exception as e:
            railfence_result = f"Lỗi: {str(e)}"
    
    return render_template("index.html",
                         railfence_result=railfence_result,
                         railfence_text=railfence_text,
                         railfence_action=railfence_action,
                         railfence_rails=railfence_rails)

@app.route("/playfair", methods=["POST"])
def playfair():
    playfair_result = ""
    playfair_action = request.form.get("action")
    playfair_text = request.form.get("text", "")
    playfair_key = request.form.get("key", "").strip()
    
    if not playfair_key:
        playfair_result = "Lỗi: Vui lòng nhập khóa cho Playfair cipher!"
    else:
        cipher = PlayFairCipher()
        
        try:
            matrix = cipher.create_playfair_matrix(playfair_key)
            if playfair_action == "encrypt_playfair":
                playfair_result = cipher.playfair_encrypt(playfair_text, matrix)
            elif playfair_action == "decrypt_playfair":
                playfair_result = cipher.playfair_decrypt(playfair_text, matrix)
        except Exception as e:
            playfair_result = f"Lỗi: {str(e)}"
    
    return render_template("index.html",
                         playfair_result=playfair_result,
                         playfair_text=playfair_text,
                         playfair_action=playfair_action,
                         playfair_key=playfair_key)

@app.route("/transposition", methods=["POST"])
def transposition():
    transposition_result = ""
    transposition_action = request.form.get("action")
    transposition_text = request.form.get("text", "")
    
    try:
        transposition_key = int(request.form.get("key", 1))
    except ValueError:
        transposition_key = 1
    
    if transposition_key <= 0:
        transposition_result = "Lỗi: Khóa phải là số nguyên dương!"
    else:
        cipher = TranspositionCipher()
        
        try:
            if transposition_action == "encrypt_transposition":
                transposition_result = cipher.encrypt(transposition_text, transposition_key)
            elif transposition_action == "decrypt_transposition":
                transposition_result = cipher.decrypt(transposition_text, transposition_key)
        except Exception as e:
            transposition_result = f"Lỗi: {str(e)}"
    
    return render_template("index.html",
                         transposition_result=transposition_result,
                         transposition_text=transposition_text,
                         transposition_action=transposition_action,
                         transposition_key=transposition_key)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2058, debug=True)