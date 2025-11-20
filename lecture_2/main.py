def generate_profile(age):
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"
    else:
        return "Invalid age"

def main():
        
    user_name = input("Enter your full name: ")
    birth_year_str = input("Enter your birth year: ")
    birth_year = int(birth_year_str)
    current_age = 2025 - birth_year
    
    hobbies = []
    print("\nNow let's add your favorite hobbies!\n")
    
    while True:
        hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
        if hobby.lower() == "stop":
            break
        if hobby.strip():
            hobbies.append(hobby)
    
    life_stage = generate_profile(current_age)
    
    user_profile = {
        "name": user_name,
        "age": current_age,
        "stage": life_stage,
        "hobbies": hobbies
    }
    
    print("\n---")
    print("PROFILE SUMMARY")
    print(f"Name: {user_profile['name']}")
    print(f"Age: {user_profile['age']}")
    print(f"Life Stage: {user_profile['stage']}")
    
    if not user_profile['hobbies']:
        print("You didn't mention any hobbies.")
    else:
        hobby_count = len(user_profile['hobbies'])
        print(f"Favorite Hobbies ({hobby_count}):")
        for hobby in user_profile['hobbies']:
            print(f"- {hobby}")
    
    print("---")

if __name__ == "__main__":
    main()