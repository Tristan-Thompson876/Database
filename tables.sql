create database School_System;
USE School_System;
SELECT * FROM students;
SELECT * FROM lecturers;
SELECT * FROM grades;
SELECT * FROM courses;
SELECT * FROM schedule;
SELECT * FROM accounts;
SELECT * FROM admins;

CREATE TABLE IF NOT EXISTS Student (
    StudentID int PRIMARY KEY, 
    UserID int, 
    StudentName varchar(255), 
    StudentEmail varchar(255), 
    UserName varchar(255)
);

CREATE TABLE Course (
    CourseCode VARCHAR(255) NOT NULL,
    CourseName VARCHAR(255) NOT NULL,
    StartDt DATE NOT NULL,
    EndDt DATE NOT NULL,
    PRIMARY KEY (CourseC)
);


CREATE TABLE IF NOT EXISTS Lecturer (
    LecturerID int PRIMARY KEY, 
    UserID int, 
    LecturerName varchar(255), 
    LecturerEmail varchar(255), 
    UserName varchar(255), 
    Department varchar(255)
);

CREATE TABLE StudentCourses (
    StudentID INT,
    CourseCode VARCHAR(255) ,
    PRIMARY KEY (StudentID, CourseCode)
);

CREATE TABLE Assignments (
    AssignmentID INT PRIMARY KEY,
    CourseCode VARCHAR(255),
    Title VARCHAR(100),
    Description TEXT,
    Submission VARCHAR(100),
    DueDate DATE
);

CREATE TABLE Calendar (
    EventID INT PRIMARY KEY,
    CourseCode VARCHAR(255),
    Title VARCHAR(100),
	StartDate DATE,
    EndDate DATE
);

CREATE TABLE CourseContent (
    CourseContentID INT PRIMARY KEY,
    CourseCode VARCHAR(255)
);

CREATE TABLE Section (
    SectionID INT,
    CourseContentID INT,
    ContentType ENUM('links', 'files', 'slides'),
    ContentPath VARCHAR(255),
    PRIMARY KEY (SectionID)
);

CREATE TABLE DiscussionForum (
    DiscussionForumID INT PRIMARY KEY,
    CourseCode VARCHAR(255),
    Name VARCHAR(100)
);

CREATE TABLE DiscussionThread (
    DiscussionThreadID INT PRIMARY KEY,
    DiscussionForumID INT,
    StudentID INT,
    Title VARCHAR(100),
    Content TEXT
);


CREATE TABLE DiscussionThreadReply (
    DiscussionThreadReplyID INT PRIMARY KEY,
    StudentID INT,
    DiscussionThreadID INT,
    Content TEXT
);

CREATE TABLE AssignmentSubmission (
    StudentID INT,
    AssignmentID INT,
    SubmissionDate DATE,
    Grade DECIMAL(5,2),
    PRIMARY KEY (StudentID, AssignmentID)
);
