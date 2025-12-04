import sqlite3
import os

def create_database_from_sql():
    """Creates database from SQL file"""
    
    # Remove existing database (if starting fresh)
    if os.path.exists('school.db'):
        os.remove('school.db')
        print("Old database removed")
    
    # Create database connection
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    print("Creating database 'school.db' from queries.sql...")
    
    try:
        # Read SQL file
        with open('queries.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Execute the entire SQL script
        cursor.executescript(sql_script)
        conn.commit()
        
        print("✓ Database successfully created and populated!")
        print(f"  Total students: {cursor.execute('SELECT COUNT(*) FROM students').fetchone()[0]}")
        print(f"  Total grades: {cursor.execute('SELECT COUNT(*) FROM grades').fetchone()[0]}")
        
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()
    
    return True

def execute_task_queries():
    """Executes and displays results of task queries"""
    if not os.path.exists('school.db'):
        print("Error: Database 'school.db' not found!")
        print("Please run create_database_from_sql() first")
        return
    
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    print("\n" + "=" * 70)
    print("EXECUTING REQUIRED QUERIES FROM TASK:")
    print("=" * 70)
    
    # Queries from the task
    queries = [
        ("1. All grades for Alice Johnson",
         """SELECT s.full_name, g.subject, g.grade 
            FROM students s 
            JOIN grades g ON s.id = g.student_id 
            WHERE s.full_name = 'Alice Johnson'"""),
        
        ("\n2. Average grade per student",
         """SELECT s.full_name, ROUND(AVG(g.grade), 2) as avg_grade 
            FROM students s 
            JOIN grades g ON s.id = g.student_id 
            GROUP BY s.id, s.full_name 
            ORDER BY avg_grade DESC"""),
        
        ("\n3. Students born after 2004",
         """SELECT full_name, birth_year 
            FROM students 
            WHERE birth_year > 2004 
            ORDER BY birth_year"""),
        
        ("\n4. Subjects and their average grades",
         """SELECT subject, ROUND(AVG(grade), 2) as avg_grade 
            FROM grades 
            GROUP BY subject 
            ORDER BY avg_grade DESC"""),
        
        ("\n5. Top 3 students with highest average grades",
         """SELECT s.full_name, ROUND(AVG(g.grade), 2) as avg_grade 
            FROM students s 
            JOIN grades g ON s.id = g.student_id 
            GROUP BY s.id, s.full_name 
            ORDER BY avg_grade DESC 
            LIMIT 3"""),
        
        ("\n6. Students who scored below 80 in any subject",
         """SELECT DISTINCT s.full_name, g.subject, g.grade 
            FROM students s 
            JOIN grades g ON s.id = g.student_id 
            WHERE g.grade < 80 
            ORDER BY s.full_name, g.grade""")
    ]
    
    for title, query in queries:
        print(title)
        print("-" * 50)
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                # Get column names
                column_names = [description[0] for description in cursor.description]
                print(" | ".join(str(name) for name in column_names))
                print("-" * 50)
                
                for row in results:
                    print(" | ".join(str(value) for value in row))
            else:
                print("No data found")
                
        except Exception as e:
            print(f"Query execution error: {e}")
    
    conn.close()

def show_database_summary():
    """Shows database summary information"""
    if not os.path.exists('school.db'):
        print("Database not found!")
        return
    
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    print("\n" + "=" * 70)
    print("DATABASE SUMMARY:")
    print("=" * 70)
    
    try:
        # Show all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        print(f"\nTables in database ({len(tables)}):")
        for table in tables:
            print(f"  • {table[0]}")
        
        # Show students count
        print(f"\nStudents in database:")
        cursor.execute("SELECT id, full_name, birth_year FROM students ORDER BY full_name")
        students = cursor.fetchall()
        for student in students:
            print(f"  {student[0]}. {student[1]} (born {student[2]})")
        
        # Show grade statistics
        print(f"\nGrade statistics:")
        cursor.execute("""
            SELECT 
                COUNT(*) as total_grades,
                MIN(grade) as min_grade,
                MAX(grade) as max_grade,
                ROUND(AVG(grade), 2) as avg_grade,
                COUNT(DISTINCT subject) as subjects_count
            FROM grades
        """)
        stats = cursor.fetchone()
        print(f"  • Total grades: {stats[0]}")
        print(f"  • Subjects: {stats[4]}")
        print(f"  • Minimum grade: {stats[1]}")
        print(f"  • Maximum grade: {stats[2]}")
        print(f"  • Average grade: {stats[3]}")
        
        # Show grade distribution
        print(f"\nGrade distribution:")
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN grade >= 90 THEN 'A (90-100)'
                    WHEN grade >= 80 THEN 'B (80-89)'
                    WHEN grade >= 70 THEN 'C (70-79)'
                    WHEN grade >= 60 THEN 'D (60-69)'
                    ELSE 'F (below 60)'
                END as grade_range,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM grades), 1) as percentage
            FROM grades
            GROUP BY grade_range
            ORDER BY MIN(grade) DESC
        """)
        distribution = cursor.fetchall()
        for row in distribution:
            print(f"  • {row[0]}: {row[1]} grades ({row[2]}%)")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        conn.close()

def run_sql_file_directly():
    """Executes SQL file directly using SQLite command line"""
    print("\n" + "=" * 70)
    print("EXECUTING SQL FILE DIRECTLY")
    print("=" * 70)
    
    if not os.path.exists('queries.sql'):
        print("Error: queries.sql file not found!")
        return
    
    if os.path.exists('school.db'):
        os.remove('school.db')
    
    # Execute SQL file using system command
    try:
        import subprocess
        result = subprocess.run(['sqlite3', 'school.db', '.read queries.sql'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ SQL file executed successfully!")
            
            # Connect to show results
            conn = sqlite3.connect('school.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM students")
            students = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM grades")
            grades = cursor.fetchone()[0]
            
            print(f"  Students: {students}")
            print(f"  Grades: {grades}")
            
            conn.close()
        else:
            print("✗ Error executing SQL file:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("SQLite3 command line tool not found.")
        print("Please install SQLite3 or use the Python method.")

def export_query_results():
    """Exports query results to CSV files"""
    if not os.path.exists('school.db'):
        print("Database not found!")
        return
    
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()
    
    import csv
    
    # Export students
    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()
    
    with open('students.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Full Name', 'Birth Year'])
        writer.writerows(students)
    
    # Export grades
    cursor.execute("""
        SELECT g.id, s.full_name, g.subject, g.grade
        FROM grades g
        JOIN students s ON g.student_id = s.id
        ORDER BY s.full_name, g.subject
    """)
    grades = cursor.fetchall()
    
    with open('grades.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Student Name', 'Subject', 'Grade'])
        writer.writerows(grades)
    
    conn.close()
    
    print(f"✓ Data exported to CSV files:")
    print(f"  • students.csv: {len(students)} records")
    print(f"  • grades.csv: {len(grades)} records")

def main():
    """Main function"""
    print("=" * 70)
    print("SCHOOL DATABASE MANAGEMENT SYSTEM")
    print("=" * 70)
    
    print("\nOptions:")
    print("1. Create database from SQL file")
    print("2. Execute task queries")
    print("3. Show database summary")
    print("4. Export data to CSV")
    print("5. Execute SQL file directly (requires SQLite3 CLI)")
    print("6. Run all operations")
    
    try:
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == '1':
            create_database_from_sql()
        elif choice == '2':
            execute_task_queries()
        elif choice == '3':
            show_database_summary()
        elif choice == '4':
            export_query_results()
        elif choice == '5':
            run_sql_file_directly()
        elif choice == '6':
            # Run all operations
            print("\n" + "=" * 70)
            print("RUNNING ALL OPERATIONS")
            print("=" * 70)
            
            if create_database_from_sql():
                show_database_summary()
                execute_task_queries()
                export_query_results()
        else:
            print("Invalid choice. Please enter 1-6.")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
    
    print("\n" + "=" * 70)
    print("OPERATION COMPLETE")
    print("=" * 70)
    print("Files created/modified:")
    print("  • school.db (SQLite database)")
    print("  • queries.sql (SQL queries)")
    if os.path.exists('students.csv'):
        print("  • students.csv (exported data)")
    if os.path.exists('grades.csv'):
        print("  • grades.csv (exported data)")

if __name__ == "__main__":
    main()