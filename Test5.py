
import argparse
from cryptography.fernet import Fernet
import os 

# Steg 1: Generera och spara en krypteringsnyckel
def generate_encryption_key(key_filename):
    try:
        key = Fernet.generate_key()
        with open(key_filename, 'wb') as key_file:
            key_file.write(key)
        print(f"Krypteringsnyckeln sparad i {key_filename}")
    except Exception as e:
        print(f"Fel vid generering av nyckel: {e}")

# Steg 2: Filkryptering
# key_filename = filen där nyckeln finns
# input_filename = filen som ska krypteras
# output_filename = filen där den krypterade datan ska sparas

def encrypt_file(key_filename, input_filename, output_filename):
    try: 
    
#steg2.1: öppna nyckelfilen och läsa den.    
        with open(key_filename, "rb") as key_file:
            key = key_file.read()
            cipher_suite = Fernet(key)# använder den tidigare lästa key som parametern för att skapa 
        # en krypteringsinstans av Fernet -klassen (kallas cipher_suite)

#steg 2.2:öppna krypteringsfilen och läs dess innehåll
        with open(input_filename, "rb") as input_file:
            file_data = input_file.read()  
        
#steg 2.3 : kryptera filinnehållet
        encrypted_data = cipher_suite.encrypt(file_data)#använder Fernet-instansen (cipher_suite) för att kryptera 
    #det inlästa filinnehållet(file_data). Den returnerar det krypterade datan som nu lagras i encrypted_data
    
#steg 2.4 : skriva den kryperade datan till en ny fil
        with open(output_filename, "wb") as output_file:
            output_file.write(encrypted_data)

        print(f"Fil krypterad och sparad som: {output_filename}")
#meddelar användare om att filen har krypterats, sparats med det angivna filnamnet (output_filename).
    except FileNotFoundError as fnf_error:
        print(f"Fel: Filen {fnf_error.filename} kunde inte hittas.")
    except Exception as e:
        print(f"Ett fel inträffade under kryptering: {e}")

# Steg 3: Fildekryptering
# key_filename = filen där nyckeln finns
# input_filename = filen som ska dekrypteras
# output_filename = filen där den dekrypterade datan ska sparas

def decrypt_file(key_filename, input_filename, output_filename):
    try:
#steg 3.1: läs in filen som innehåller krypteringsnyckeln   
        with open(key_filename, "rb") as key_file:
            key = key_file.read()
            cipher_suite = Fernet(key)  # den tidigare krypteringsinstans (cipher_suite) kan nu användas för att dekryptera data 
        #som har krypterats med samma nyckel.
        
#steg 3.2 : läs in den krypterade datan från filen
        with open(input_filename, "rb") as input_file:
            encrypted_data = input_file.read()

# steg 3.3 : dekryptera den krypterade datan
        decrypted_data = cipher_suite.decrypt(encrypted_data)# tar den krypterad data som argument och returnera 
    #den ursplungliga, okrypterade datan. Den dekrypterade datan sparas i variablen decrypted_data
    
# steg 3.4 : Skriva den dekrypterade datan i en ny fil.
        with open(output_filename, "wb") as output_file:  
            output_file.write(decrypted_data)

        print(f"Fil dekrypterad och sparad som {output_filename}")  #skriver till användaren, bekräftar att filen 
    #har dekrypterats och sparats med namnet output_filename.
    except FileNotFoundError as fnf_error:
        print(f"Fel: Filen {fnf_error.filename} kunde inte hittas.")
    except Exception as e:
        print(f"Ett fel inträffade under dekryptering: {e}")
        
# Huvudprogram
def main():
    print("Krypteringsverktyget är startat.")
    parser = argparse.ArgumentParser(description="Krypteringsverktyg")

    # Argument för att generera en krypteringsnyckel
    parser.add_argument("-g", "--generate-key", type=str, help="Generera och spara en krypteringsnyckel")

    # Argument för att kryptera en fil
    parser.add_argument("-e", "--encrypt", type=str, nargs=2, help="Kryptera en fil. Ange krypteringsnyckel och filen som ska krypteras")

    # Argument för att dekryptera en fil
    parser.add_argument("-d", "--decrypt", type=str, nargs=2, help="Dekryptera en fil. Ange krypteringsnyckel och den krypterade filen")

    args = parser.parse_args()

    if args.generate_key:
        generate_encryption_key(args.generate_key)

    elif args.encrypt:
        key_filename, input_filename = args.encrypt
        output_filename = f"{input_filename}.encrypted"
        encrypt_file(key_filename, input_filename, output_filename)

    elif args.decrypt:
        key_filename, input_filename = args.decrypt
        output_filename = f"{input_filename}.decrypted"
        decrypt_file(key_filename, input_filename, output_filename)
        
    else:
        print("Inga giltiga argument angivna. Använd --help för att se tillgängliga alternativ.")

if __name__ == "__main__":
    main()
    

