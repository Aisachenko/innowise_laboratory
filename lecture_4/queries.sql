-- ============================================
-- SCHOOL DATABASE: COMPLETE SQL SCRIPT
-- ============================================

-- 1. DROP EXISTING TABLES (IF ANY)
-- ============================================
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;

-- 2. CREATE TABLES
-- ============================================

-- Students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

-- Grades table
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK (grade >= 1 AND grade <= 100),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- 3. INSERT SAMPLE DATA
-- ============================================

-- Insert students
INSERT INTO students (full_name, birth_year) VALUES 
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

-- Insert grades
INSERT INTO grades (student_id, subject, grade) VALUES 
(1, 'Math', 88),
(1, 'English', 92),
(1, 'Science', 85),
(2, 'Math', 75),
(2, 'History', 83),
(2, 'English', 79),
(3, 'Science', 95),
(3, 'Math', 91),
(3, 'Art', 89),
(4, 'Math', 84),
(4, 'Science', 88),
(4, 'Physical Education', 93),
(5, 'English', 90),
(5, 'History', 85),
(5, 'Math', 88),
(6, 'Science', 72),
(6, 'Math', 78),
(6, 'English', 81),
(7, 'Art', 94),
(7, 'Science', 87),
(7, 'Math', 90),
(8, 'History', 77),
(8, 'Math', 83),
(8, 'Science', 80),
(9, 'English', 96),
(9, 'Math', 89),
(9, 'Art', 92);

-- 4. CREATE INDEXES FOR OPTIMIZATION
-- ============================================
CREATE INDEX idx_student_id ON grades(student_id);
CREATE INDEX idx_student_birth_year ON students(birth_year);
CREATE INDEX idx_grade ON grades(grade);
CREATE INDEX idx_subject ON grades(subject);

-- 5. REQUIRED QUERIES FROM THE TASK
-- ============================================

-- Query 1: All grades for a specific student (Alice Johnson)
SELECT '1. All grades for Alice Johnson' as query_title;
SELECT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE s.full_name = 'Alice Johnson';

-- Query 2: Calculate the average grade per student
SELECT '2. Average grade per student' as query_title;
SELECT s.full_name, ROUND(AVG(g.grade), 2) as avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY avg_grade DESC;

-- Query 3: List all students born after 2004
SELECT '3. Students born after 2004' as query_title;
SELECT full_name, birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year;

-- Query 4: List all subjects and their average grades
SELECT '4. Subjects and their average grades' as query_title;
SELECT subject, ROUND(AVG(grade), 2) as avg_grade
FROM grades
GROUP BY subject
ORDER BY avg_grade DESC;

-- Query 5: Find the top 3 students with the highest average grades
SELECT '5. Top 3 students with highest average grades' as query_title;
SELECT s.full_name, ROUND(AVG(g.grade), 2) as avg_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id, s.full_name
ORDER BY avg_grade DESC
LIMIT 3;

-- Query 6: Show all students who have scored below 80 in any subject
SELECT '6. Students who scored below 80 in any subject' as query_title;
SELECT DISTINCT s.full_name, g.subject, g.grade
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80
ORDER BY s.full_name, g.grade;

-- 6. ADDITIONAL VALIDATION QUERIES
-- ============================================

-- Show all students
SELECT 'All students:' as query_title;
SELECT * FROM students ORDER BY id;

-- Show all grades with student names
SELECT 'All grades with student names:' as query_title;
SELECT g.id, s.full_name, g.subject, g.grade
FROM grades g
JOIN students s ON g.student_id = s.id
ORDER BY s.full_name, g.subject;

-- Database statistics
SELECT 'Database statistics:' as query_title;
SELECT 
    (SELECT COUNT(*) FROM students) as total_students,
    (SELECT COUNT(*) FROM grades) as total_grades,
    (SELECT COUNT(DISTINCT subject) FROM grades) as total_subjects,
    (SELECT MIN(grade) FROM grades) as min_grade,
    (SELECT MAX(grade) FROM grades) as max_grade,
    (SELECT ROUND(AVG(grade), 2) FROM grades) as avg_grade;