-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.30 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for uni_db
CREATE DATABASE IF NOT EXISTS `uni_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `uni_db`;


-- Dumping structure for table uni_db.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `username` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `password` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `role` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table uni_db.users: ~2 rows (approximately)
INSERT INTO `users` (`id`, `name`, `username`, `password`, `role`) VALUES
	(2, 'admin', 'admin123', '1234', 'Admin'),
	(3, 'user11', 'test', '1234', 'Student'),
	(4, 'prof11', 'prof', '1234', 'Professor');

-- Dumping structure for table uni_db.class_timetable
CREATE TABLE IF NOT EXISTS `class_timetable` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_code` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `course_name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `day_of_week` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `location` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `semester_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table uni_db.class_timetable: ~3 rows (approximately)
INSERT INTO `class_timetable` (`id`, `course_code`, `course_name`, `day_of_week`, `start_time`, `end_time`, `location`, `semester_id`) VALUES
	(1, 'CSE101', 'Introduction to Computer Science', 'Monday', '09:00:00', '10:30:00', 'Room 101', NULL),
	(2, 'MTH201', 'Calculus II', 'Tuesday', '11:00:00', '12:30:00', 'Room 203', NULL),
	(3, 'ENG301', 'Advanced English Writing', 'Wednesday', '13:00:00', '14:30:00', 'Room 305', NULL);



-- Dumping structure for table uni_db.programs
CREATE TABLE IF NOT EXISTS `programs` (
  `program_id` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `credits_required` int DEFAULT '40',
  PRIMARY KEY (`program_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table uni_db.programs: ~2 rows (approximately)
INSERT INTO `programs` (`program_id`, `Name`, `credits_required`) VALUES
	(1, 'Bachelor of Computer Science', 40),
	(2, 'Bachelor of Law', 40);

-- Dumping structure for table uni_db.courses
CREATE TABLE IF NOT EXISTS `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `program_id` int DEFAULT NULL,
  `course_code` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `credits` int DEFAULT '4',
  PRIMARY KEY (`id`),
  KEY `FK_courses_programs` (`program_id`),
  CONSTRAINT `FK_courses_programs` FOREIGN KEY (`program_id`) REFERENCES `programs` (`program_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table uni_db.courses: ~5 rows (approximately)
INSERT INTO `courses` (`id`, `name`, `program_id`, `course_code`, `credits`) VALUES
	(1, 'Programming Fundamentals', 1, 'PF302', 4),
	(2, 'Database Design', 1, 'DD101', 4),
	(3, 'Introduction to Calculus', 1, 'IC303', 4),
	(4, 'Fundamentals of Communication', 2, 'FC444', 4),
	(5, 'Software Quality Assurance', 1, 'SQA44', 4);

-- Dumping structure for table uni_db.course_enrollment
CREATE TABLE IF NOT EXISTS `course_enrollment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_course_enrollment_courses` (`course_id`),
  KEY `FK_course_enrollment_users` (`student_id`),
  CONSTRAINT `FK_course_enrollment_courses` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `FK_course_enrollment_users` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table uni_db.course_enrollment: ~3 rows (approximately)

-- Dumping structure for table uni_db.examstimetable
CREATE TABLE IF NOT EXISTS `examstimetable` (
  `exam_id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `exam_date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `student_id` int DEFAULT NULL,
  PRIMARY KEY (`exam_id`),
  KEY `FK_examstimetable_courses` (`course_id`),
  KEY `FK_examstimetable_users` (`student_id`),
  CONSTRAINT `FK_examstimetable_courses` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `FK_examstimetable_users` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table uni_db.examstimetable: ~5 rows (approximately)

-- Dumping structure for table uni_db.feedback
CREATE TABLE IF NOT EXISTS `feedback` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `feedback` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `course_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_feedback_courses` (`course_id`),
  KEY `FK_feedback_users` (`student_id`),
  CONSTRAINT `FK_feedback_courses` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `FK_feedback_users` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table uni_db.feedback: ~2 rows (approximately)


-- Dumping structure for table uni_db.results
CREATE TABLE IF NOT EXISTS `results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_id` int DEFAULT NULL,
  `student_id` int DEFAULT NULL,
  `total_marks` int DEFAULT NULL,
  `marks_recieved` int DEFAULT NULL,
  `grade` char(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_results_courses` (`course_id`),
  KEY `FK_results_users` (`student_id`),
  CONSTRAINT `FK_results_courses` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`),
  CONSTRAINT `FK_results_users` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table uni_db.results: ~3 rows (approximately)

-- Dumping structure for table uni_db.student_programs
CREATE TABLE IF NOT EXISTS `student_programs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `program_id` int DEFAULT NULL,
  `semesters_completed` int DEFAULT '1',
  `credits_required` int DEFAULT '40',
  `semesters_required` int DEFAULT '8',
  PRIMARY KEY (`id`),
  KEY `FK_student_programs_programs` (`program_id`),
  KEY `FK_student_programs_users` (`student_id`),
  CONSTRAINT `FK_student_programs_programs` FOREIGN KEY (`program_id`) REFERENCES `programs` (`program_id`),
  CONSTRAINT `FK_student_programs_users` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table uni_db.student_programs: ~0 rows (approximately)


/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
