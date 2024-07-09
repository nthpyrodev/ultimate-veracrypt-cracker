import subprocess
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the VeraCrypt executable, when you installed veracrypt, it would have installed to here.
veracrypt_path = r"C:\Program Files\VeraCrypt\VeraCrypt.exe"
# Path to the encrypted volume, if its a flash drive, maybe something like "E:\" 
volume_path = r"C:\Users\username\Downloads\testing"
# Drive letter to mount the volume, you can leave it like this
drive_letter = 'v'
# Path to the file containing the list of password guesses, if it is in the same folder as this python, then you don't need a path, but it it is in a different folder, do something like this: "C:\Users\username\Downloads\testing"
password_file_path = r"wordlist.txt"

# Sleep interval in seconds between each attempt, the higher the number, the slower the guessing, you may want to set it higher if your computer is likely to crash. If you have a good computer, try setting it lower. For me, 1 second was fine though.
sleep_interval = 1  # Adjust the sleep time as needed

def try_password(password):
    command = [
        veracrypt_path,
        "/volume", volume_path,
        "/letter", drive_letter,
        "/password", password,
        "/quit",
        "/silent"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        return True
    return False

def read_passwords_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def main():
    # Initialize logging
    logger = logging.getLogger(__name__)
    
    password_guesses = read_passwords_from_file(password_file_path)
    
    logger.info(f"Starting password guessing process with {len(password_guesses)} passwords from file: {password_file_path}")
    
    for password in password_guesses:
        logger.info(f"Attempting password: {password}")
        if try_password(password):
            logger.info(f"Success! The password is: {password}")
            break
        else:
            logger.info(f"Attempt with password '{password}' failed.")
        time.sleep(sleep_interval)
    else:
        logger.info("None of the passwords worked.")

if __name__ == "__main__":
    main()
