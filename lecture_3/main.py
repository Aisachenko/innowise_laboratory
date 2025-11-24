class StudentGradeAnalyzer:
    """Student Grade Analyzer Program"""
    
    def __init__(self):
        self.students = []
    
    def display_menu(self):
        """Display the main menu"""
        print("\n--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Generate a full report")
        print("4. Find the top student")
        print("5. Exit program")
    
    def _get_student_by_name(self, name):
        """Find student by name (case-insensitive)"""
        name_lower = name.lower()
        for student in self.students:
            if student["name"].lower() == name_lower:
                return student
        return None
    
    def _validate_grade(self, grade_str):
        """Validate and convert grade input"""
        try:
            grade = float(grade_str)
            if 0 <= grade <= 100:
                return grade
            else:
                print("Error: Grade must be between 0 and 100")
                return None
        except ValueError:
            print("Error: Please enter a valid number")
            return None
    
    def _get_student_name_input(self):
        """Get and validate student name input"""
        name = input("Enter student name: ").strip()
        if not name:
            print("Error: Student name cannot be empty!")
            return None
        return name
    
    def add_new_student(self):
        """Add a new student to the list"""
        name = self._get_student_name_input()
        if not name:
            return
        
        if self._get_student_by_name(name):
            print(f"Error: Student '{name}' already exists!")
            return
        
        new_student = {
            "name": name,
            "grades": []
        }
        self.students.append(new_student)
        print(f"Student '{name}' added successfully!")
    
    def add_grades_for_student(self):
        """Add grades for an existing student"""
        if not self.students:
            print("No students available. Please add students first.")
            return
        
        name = self._get_student_name_input()
        if not name:
            return
        
        student = self._get_student_by_name(name)
        if not student:
            print(f"Error: Student '{name}' not found!")
            return
        
        print(f"Adding grades for {student['name']}:")
        
        while True:
            grade_input = input("Enter a grade (0-100) or 'done' to finish: ").strip().lower()
            
            if grade_input == 'done':
                break
            
            grade = self._validate_grade(grade_input)
            if grade is not None:
                student["grades"].append(grade)
                print(f"Grade {grade} added successfully!")
    
    def calculate_average(self, grades):
        """Calculate average of grades, handle empty list"""
        if not grades:
            return None
        return sum(grades) / len(grades)
    
    def _get_student_statistics(self):
        """Calculate statistics for all students"""
        averages = []
        valid_averages = []
        
        for student in self.students:
            avg = self.calculate_average(student["grades"])
            averages.append(avg)
            if avg is not None:
                valid_averages.append(avg)
        
        return averages, valid_averages
    
    def show_report(self):
        """Generate and display full report"""
        if not self.students:
            print("No students available.")
            return
        
        print("\n--- Student Report ---")
        
        averages, valid_averages = self._get_student_statistics()
        
        # Display individual student averages
        for student, avg in zip(self.students, averages):
            if avg is not None:
                print(f"{student['name']}'s average grade is {avg:.1f}.")
            else:
                print(f"{student['name']}'s average grade is N/A.")
        
        # Display overall statistics
        if valid_averages:
            print("\n--- Overall Statistics ---")
            print(f"Highest average: {max(valid_averages):.1f}")
            print(f"Lowest average: {min(valid_averages):.1f}")
            print(f"Overall average: {sum(valid_averages) / len(valid_averages):.1f}")
        else:
            print("\nNo valid averages to calculate statistics.")
    
    def find_top_performer(self):
        """Find student(s) with highest average grade"""
        if not self.students:
            print("No students available.")
            return
        
        top_students = []
        top_avg = -1
        
        for student in self.students:
            avg = self.calculate_average(student["grades"])
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
            student = top_students[0]
            print(f"Top student: {student['name']} with {top_avg:.1f} average")
        else:
            names = ", ".join(student['name'] for student in top_students)
            print(f"Top students (tie): {names} with {top_avg:.1f} average")
    
    def _handle_menu_choice(self, choice):
        """Handle menu choice selection"""
        menu_actions = {
            '1': self.add_new_student,
            '2': self.add_grades_for_student,
            '3': self.show_report,
            '4': self.find_top_performer
        }
        
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice! Please enter a number between 1-5.")
    
    def run(self):
        """Main program loop"""
        print("Welcome to Student Grade Analyzer!")
        
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-5): ").strip()
            
            if not choice:
                print("Error: Please enter a choice!")
                continue
            
            if choice == '5':
                print("Thank you for using Student Grade Analyzer. Goodbye!")
                break
            
            try:
                self._handle_menu_choice(choice)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print("Please try again.")


def main():
    """Launch the Student Grade Analyzer"""
    analyzer = StudentGradeAnalyzer()
    analyzer.run()


if __name__ == "__main__":
    main()