import math
import re

def estimate_crack_time(password):
    if not password:
        return "Password cannot be empty.", 0, 0
    
    length = len(password)
    
    # Determine character pool size (k)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', password))
    
    pool_size = 0
    if has_lower: pool_size += 26
    if has_upper: pool_size += 26
    if has_digit: pool_size += 10
    if has_symbol: pool_size += 32  # Standard symbols pool
    
    if pool_size == 0:
        pool_size = 1
        
    # Total combinations (Keyspace N = pool_size ^ length)
    combinations = pool_size ** length
    
    # Modern GPU-accelerated brute-force speed (approx. 10 billion hashes/sec)
    guesses_per_second = 10_000_000_000 
    
    # Average time to crack is half of the total keyspace combinations
    seconds = (combinations / 2) / guesses_per_second
    
    return format_time(seconds), combinations, pool_size

def format_time(seconds):
    if seconds < 1:
        return "Instantaneously (less than a second)"
    
    intervals = (
        ('years', 60 * 60 * 24 * 365),
        ('days', 60 * 60 * 24),
        ('hours', 60 * 60),
        ('minutes', 60),
        ('seconds', 1),
    )
    
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f"{int(value)} {name}")
            
    return ", ".join(result[:2])  # Return the top two largest units

def check_password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short (less than 8 characters).")
        
    if re.search(r'[a-z]', password) and re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Include both uppercase and lowercase letters.")
        
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Include numbers.")
        
    if re.search(r'[^a-zA-Z0-9]', password):
        score += 1
    else:
        feedback.append("Include special symbols (e.g., !, @, #, $).")
        
    # Penalize common patterns
    common_patterns = ['12345', 'password', 'qwerty', 'admin', 'welcome', 'letmein']
    if any(p in password.lower() for p in common_patterns):
        score = max(0, score - 2)
        feedback.append("Contains a common dictionary word or predictable pattern.")
        
    strength_map = {
        0: "Very Weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong",
        5: "Extremely Strong"
    }
    
    return strength_map.get(min(score, 5)), feedback

if __name__ == "__main__":
    print("=== Password Strength & Brute-Force Estimator ===")
    pwd = input("Enter a password to test: ")
    
    strength, feedback = check_password_strength(pwd)
    crack_time, combinations, pool = estimate_crack_time(pwd)
    
    print("\n--- Analysis Results ---")
    print(f"Strength Rating: {strength}")
    print(f"Character Pool Options: {pool} possible characters")
    print(f"Total Possible Combinations: {combinations:,}")
    print(f"Estimated Crack Time (GPU Brute-Force): {crack_time}")
    
    if feedback:
        print("\nRecommendations to Improve:")
        for tip in feedback:
            print(f"- {tip}")