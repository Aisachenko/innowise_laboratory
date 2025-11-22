def display_menu():
    """Display the main menu"""
    print("\n--- Student Grade Analyzer ---")
    print("1. Add a new student")
    print("2. Add grades for a student")
    print("3. Generate a full report")
    print("4. Find the top student")
    print("5. Exit program")
    
def enter_student_name():
    name = input("Enter student name: ").strip()
    
    if not name:
        raise("Error: Student name cannot be empty!")    
    return name

def add_new_student(students):
    """Add a new student to the list"""
    name = input("Enter student name: ").strip()
    if not name:
        print("Error: Student name cannot be empty!")
        return
    
    name_lower = name.lower()
    if any(student["name"].lower() == name_lower for student in students):
        print(f"Student '{name}' already exists!")
        return
    
    new_student = {
        "name": name,
        "grades": []
    }
    students.append(new_student)
    print(f"Student '{name}' added successfully!")

def add_grades_for_student(students):
    """Add grades for an existing student"""
    if not students:
        print("No students available. Please add students first.")
        return
    
    name = input("Enter student name: ").strip()
    if not name:
        print("Error: Student name cannot be empty!")
        return
    
    student_found = None
    for student in students:
        if student["name"].lower() == name.lower():
            student_found = student
            break
    
    if not student_found:
        print(f"Student '{name}' not found!")
        return
    
    print(f"Adding grades for {student_found['name']}:")
    
    while True:
        grade_input = input("Enter a grade (or 'done' to finish): ").strip().lower()
        
        if grade_input == 'done':
            break
        
        try:
            grade = float(grade_input)
            if 0 <= grade <= 100:
                student_found["grades"].append(grade)
                print(f"Grade {grade} added successfully!")
            else:
                print("Invalid grade! Please enter a number between 0 and 100.")
        except ValueError:
            print("Invalid input! Please enter a valid number or 'done'.")

def calculate_average(grades):
    """Calculate average of grades, handle empty list"""
    if not grades:
        return None
    return sum(grades) / len(grades)

def show_report(students):
    """Generate and display full report"""
    if not students:
        print("No students available.")
        return
    
    print("\n--- Student Report ---")
    
    averages = []
    valid_averages = []
    
    for student in students:
        try:
            avg = calculate_average(student["grades"])
            if avg is not None:
                print(f"{student['name']}'s average grade is {avg:.1f}.")
                averages.append(avg)
                valid_averages.append(avg)
            else:
                print(f"{student['name']}'s average grade is N/A.")
                averages.append(None)
        except ZeroDivisionError:
            print(f"{student['name']}'s average grade is N/A.")
            averages.append(None)
    
    if valid_averages:
        max_avg = max(valid_averages)
        min_avg = min(valid_averages)
        overall_avg = sum(valid_averages) / len(valid_averages)
        
        print("---"*40)
        print(f"Max Average: {max_avg:.1f}")
        print(f"Min Average: {min_avg:.1f}")
        print(f"Overall Average: {overall_avg:.1f}")
    else:
        print("---"*40)
        print("No valid averages to calculate statistics.")

def find_top_performer(students):
    """Find student with highest average grade"""
    if not students:
        print("No students available.")
        return
    
    top_students = []
    top_avg = -1
    
    for student in students:
        avg = calculate_average(student["grades"])
        if avg is not None:
            if avg > top_avg:
                top_avg = avg
                top_students = [student]
            elif avg == top_avg:
                top_students.append(student)
    
    if not top_students:
        print("No students with grades available.")
        return
    
    if len(top_students) == 1:
        print(f"The student with the highest average is {top_students[0]['name']} with a grade of {top_avg:.1f}")
    else:
        names = ", ".join(student['name'] for student in top_students)
        print(f"Multiple top students with average {top_avg:.1f}: {names}")

def main():
    """Main program function"""
    students = [] 
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if not choice:
                print("Error: Please enter a choice!")
                continue
            
            if choice == '1':
                add_new_student(students)
            elif choice == '2':
                add_grades_for_student(students)
            elif choice == '3':
                show_report(students)
            elif choice == '4':
                find_top_performer(students)
            elif choice == '5':
                print("Exiting program.")
                break
            else:
                print("Invalid choice! Please enter a number between 1-5.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()