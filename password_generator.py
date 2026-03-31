import math
import string
import secrets
import sys


def print_welcome():
    print("=" * 70)
    print("     ENTERPRISE RANDOM PASSWORD GENERATOR")
    print("     Secure | Cryptographic | Professional")
    print("=" * 70)
    print()


def print_divider(title=""):
    if title:
        print(f"--- {title} ---")
    else:
        print("-" * 70)


def print_error(message):
    print(f"\n[ERROR] {message}\n")


def print_success(message):
    print(f"\n[SUCCESS] {message}\n")


def get_password_length():
    while True:
        print_divider("PASSWORD LENGTH")
        user_input = input("Enter password length (minimum 8, recommended 15+): ").strip()
        
        if not user_input:
            print_error("Input cannot be empty. Please enter a number.")
            continue
        
        try:
            length = int(user_input)
        except ValueError:
            print_error(f"Invalid input: '{user_input}' is not a valid integer.")
            continue
        
        if length <= 0:
            print_error("Password length must be greater than zero.")
            continue
        
        if length < 8:
            print_error(f"Password length {length} is too short. Minimum is 8 characters.")
            continue
        
        if length < 15:
            print("\n[WARNING] Passwords shorter than 15 characters are not recommended")
            print("          for modern security practices.")
            confirm = input("          Continue anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                continue
        
        return length


def get_character_options():
    print_divider("CHARACTER OPTIONS")
    
    include_symbols = get_yes_no(
        "Include symbols/punctuation? (e.g., !@#$%^&*): ",
        default="y"
    )
    
    include_numbers = get_yes_no(
        "Include numbers? (e.g., 0123456789): ",
        default="y"
    )
    
    return {
        "symbols": include_symbols,
        "numbers": include_numbers
    }


def get_yes_no(prompt, default="y"):
    while True:
        default_text = "[Y/n]" if default == "y" else "[y/N]"
        user_input = input(f"{prompt} {default_text}: ").strip().lower()
        
        if not user_input:
            return default == "y"
        
        if user_input in ['y', 'yes']:
            return True
        elif user_input in ['n', 'no']:
            return False
        else:
            print_error("Please enter 'y' for yes or 'n' for no.")


def build_character_pool(include_symbols=True, include_numbers=True):
    pool = string.ascii_letters
    
    if include_numbers:
        pool += string.digits
    
    if include_symbols:
        pool += string.punctuation
    
    return pool


def ensure_required_characters(password, include_symbols, include_numbers):
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation
    
    password_list = list(password)
    
    if include_numbers:
        if not any(c in digits for c in password_list):
            password_list[0] = secrets.choice(digits)
    
    if not any(c in letters for c in password_list):
        password_list[0] = secrets.choice(letters)
    
    if include_symbols:
        if not any(c in symbols for c in password_list):
            password_list[1] = secrets.choice(symbols)
    
    return password_list


def generate_password(length, character_pool):
    password_list = [secrets.choice(character_pool) for _ in range(length)]
    password = ''.join(password_list)
    
    return password


def calculate_entropy(password_length, pool_size):
    entropy = password_length * math.log2(pool_size)
    return entropy


def classify_strength(entropy):
    if entropy < 40:
        return "Weak"
    elif entropy < 80:
        return "Moderate"
    elif entropy < 120:
        return "Strong"
    else:
        return "Very Strong"


def display_results(password, length, pool_size, entropy, strength):
    print()
    print_divider("GENERATED PASSWORD")
    print()
    print(f"  Password:  {password}")
    print()
    print_divider("STATISTICS")
    print()
    print(f"  Length:          {length} characters")
    print(f"  Character Pool: {pool_size} possible characters")
    print(f"  Entropy:         {entropy:.2f} bits")
    print()
    print_divider("SECURITY STRENGTH")
    print()
    print(f"  Level: {strength}")
    print()
    
    print_security_recommendations(entropy, strength)
    print()


def print_security_recommendations(entropy, strength):
    print("  Recommendations:")
    
    if entropy < 80:
        print("  - Consider using a longer password for better security")
    
    if strength in ["Weak", "Moderate"]:
        print("  - Use a password manager to store this password")
        print("  - Enable two-factor authentication where possible")
    
    if strength in ["Strong", "Very Strong"]:
        print("  - This password meets enterprise security standards")
        print("  - Store securely in a password manager")


def main():
    print_welcome()
    
    length = get_password_length()
    
    options = get_character_options()
    
    character_pool = build_character_pool(
        include_symbols=options["symbols"],
        include_numbers=options["numbers"]
    )
    
    password = generate_password(length, character_pool)
    
    password = ensure_required_characters(
        password,
        include_symbols=options["symbols"],
        include_numbers=options["numbers"]
    )
    
    password = ''.join(password)
    
    entropy = calculate_entropy(length, len(character_pool))
    
    strength = classify_strength(entropy)
    
    display_results(password, length, len(character_pool), entropy, strength)
    
    print_divider("NEW PASSWORD")
    another = get_yes_no("Generate another password?", default="n")
    if another:
        print()
        main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Password generation cancelled by user.")
        print("       Thank you for using Enterprise Password Generator.")
        sys.exit(0)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)
