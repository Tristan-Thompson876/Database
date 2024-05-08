
CREATE TABLE Account (
    UserID INT PRIMARY KEY,
    Username VARCHAR(255),
    Password VARCHAR(255)
); 

CREATE TABLE Admin(
    AdminID INT PRIMARY KEY,
    AdminName VARCHAR(255)
); 

CREATE TABLE Lecturer (
    LecturerID INT PRIMARY KEY,
    LecturerName VARCHAR(255),
    LecturerEmail VARCHAR(255)
); 

CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    StudentName VARCHAR(255),
    StudentEmail VARCHAR(255)
);

CREATE TABLE Course (
    CourseC INT PRIMARY KEY,
    CourseName INT PRIMARY KEY,
    StartDt VARCHAR(255),
    EndDt VARCHAR(255)
);
CREATE TABLE Enrollment (
    CourseC INT PRIMARY KEY,
    FOREIGN KEY (CourseC) REFERENCES Course(CourseC),
    StudentID INT
);

CREATE TABLE Assignments (
    AssignmentID INT PRIMARY KEY,
    UserID INT,
    FOREIGN KEY(UserID) REFERENCES Account(UserID),
    Title VARCHAR(255),
    Description VARCHAR(255),
    Submission VARCHAR(255),
    Grades VARCHAR(255),
    dueDate VARCHAR(255)
); 

CREATE TABLE Calendar (
    EventID INT PRIMARY KEY,
    CourseID VARCHAR(255),
    Title VARCHAR(255),
    SDate VARCHAR(255),
    EDate VARCHAR(255)
);

CREATE TABLE Section(
    SectionID INT PRIMARY KEY,
    Links VARCHAR(255),
    CMaterials VARCHAR(255)
); 

CREATE TABLE DiscussionForum (
    DiscussionID INT PRIMARY KEY,
    CourseC INT,
    FOREIGN KEY (CourseC) REFERENCES Course(CourseC), 
    Name VARCHAR(255)
)

CREATE TABLE DiscussionThread (
    DiscussionID INT, 
    FOREIGN KEY (DiscussionID) REFERENCES DiscussionForum(DiscussionID),
    ThreadID INT PRIMARY KEY,
    Title VARCHAR(255),
    Content VARCHAR(255)
)
