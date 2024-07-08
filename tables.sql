USE School_System;

CREATE TABLE IF NOT EXISTS Account (
    UserID INT PRIMARY KEY,
    UserName VARCHAR(255) NOT NULL,
    Password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Student (
    StudentID int PRIMARY KEY, 
    UserID int, 
    StudentName varchar(255), 
    StudentEmail varchar(255), 
    UserName varchar(255),
    FOREIGN KEY (UserID) REFERENCES Account(UserID)
);

CREATE TABLE IF NOT EXISTS Admin (
    AdminID INT PRIMARY KEY,
    UserID INT,
    AdminName VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Account(UserID)
);

CREATE TABLE IF NOT EXISTS Course (
    CourseCode VARCHAR(255) NOT NULL,
    CourseName VARCHAR(255) NOT NULL,
    Department VARCHAR(255), -- Added Department column
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    PRIMARY KEY (CourseCode)
);

CREATE TABLE IF NOT EXISTS Enrol (
    CourseCode varchar(255) NOT NULL,
    StudentID int NOT NULL,
    PRIMARY KEY (CourseCode, StudentID),
    FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
);

CREATE TABLE IF NOT EXISTS Lecturer (
    LecturerID int PRIMARY KEY, 
    UserID int, 
    LecturerName varchar(255), 
    LecturerEmail varchar(255), 
    UserName varchar(255), 
    Department varchar(255),
    FOREIGN KEY (UserID) REFERENCES Account(UserID)
);

CREATE TABLE IF NOT EXISTS Assignedcourse (
    CourseCode varchar(255),
    LecturerID int,
    PRIMARY KEY (CourseCode, LecturerID),
    FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode),
    FOREIGN KEY (LecturerID) REFERENCES Lecturer(LecturerID)
);

CREATE TABLE IF NOT EXISTS Assignments (
    AssignmentID INT PRIMARY KEY,
    CourseCode VARCHAR(255),
    Title VARCHAR(100),
    Description TEXT,
    Submission VARCHAR(100),
    DueDate DATE,
    FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode)
);

CREATE TABLE IF NOT EXISTS Calendar (
    EventID INT PRIMARY KEY,
    CourseCode VARCHAR(255),
    Title VARCHAR(100),
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode)
);

CREATE TABLE IF NOT EXISTS CourseContent (
    CourseContentID INT PRIMARY KEY,
    CourseCode VARCHAR(255),
    FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode)
);

CREATE TABLE IF NOT EXISTS Section (
    SectionID INT PRIMARY KEY,
    CourseContentID INT,
    ContentType ENUM('links', 'files', 'slides'),
    ContentPath VARCHAR(255),
    FOREIGN KEY (CourseContentID) REFERENCES CourseContent(CourseContentID)
);

CREATE TABLE IF NOT EXISTS DiscussionForum (
    DiscussionForumID INT PRIMARY KEY,
    CourseCode VARCHAR(255),
    Name VARCHAR(100),
    FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode)
);

CREATE TABLE IF NOT EXISTS DiscussionThread (
    DiscussionThreadID INT PRIMARY KEY,
    DiscussionForumID INT,
    StudentID INT,
    Title VARCHAR(100),
    Content TEXT,
    FOREIGN KEY (DiscussionForumID) REFERENCES DiscussionForum(DiscussionForumID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
);

CREATE TABLE IF NOT EXISTS DiscussionThreadReply (
    DiscussionThreadReplyID INT PRIMARY KEY,
    StudentID INT,
    DiscussionThreadID INT,
    Content TEXT,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (DiscussionThreadID) REFERENCES DiscussionThread(DiscussionThreadID)
);

CREATE TABLE IF NOT EXISTS AssignmentSubmission (
    StudentID INT,
    AssignmentID INT,
    SubmissionDate DATE,
    Grade DECIMAL(5,2),
    PRIMARY KEY (StudentID, AssignmentID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (AssignmentID) REFERENCES Assignments(AssignmentID)
);

CREATE TABLE IF NOT EXISTS Grades (
    StudentID INT,
    CourseCode VARCHAR(255),
    Grade DECIMAL(5,2),
    PRIMARY KEY (StudentID, CourseCode),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode)
);
