import zipfile
import itertools
import string

def extract_zip(zip_file,password):
    """
    Attempts to extract the zip file with a given password.
    Returns the password if successful, None otherwise.
    """
    try:
        zip_file.extractall(pwd=password.encode('utf-8'))
        return password
    except RuntimeError as e:
        if 'Bad password' in str(e):
            return None
    except Exception as e:
        return None
    
def main():
    chars = string.digits
    zip_filename = 'your_file.zip'

    try:
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            for length in range(1, 5):
                print(f"Trying passwords of length {length}...")
                for guess in itertools.product(chars, repeat=length):
                    password = ''.join(guess)
                    found_password = extract_zip(zip_ref, password)
                    if found_password:
                        print(f"\nPassword found: {found_password}")
                        zip_ref.extractall(path="uncompressed_content", pwd=found_password.encode('utf-8'))
                        print(f"Files extracted to 'uncompressed_content' directory.")
                        return
        print("Password not found within the specified character set and length range.")
    except FileNotFoundError:
        print(f"Error: The file '{zip_filename}' was not found")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()