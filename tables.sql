CREATE TABLE Account (
    UserID INT PRIMARY KEY,
    Username VARCHAR(50),
    Password VARCHAR(50)
);

CREATE TABLE Admin (
    AdminID INT PRIMARY KEY,
    UserID INT,
    AdminName VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES Account(UserID)
);

CREATE TABLE Lecturer (
    LecturerID INT PRIMARY KEY,
    UserID INT,
    LecturerName VARCHAR(50),
    LecturerEmail VARCHAR(100),
    FOREIGN KEY (UserID) REFERENCES Account(UserID)
);

CREATE TABLE Student (
    StudentID INT PRIMARY KEY,
    UserID INT,
    StudentName VARCHAR(50),
    StudentEmail VARCHAR(100),
    FOREIGN KEY (UserID) REFERENCES Account(UserID)
);

CREATE TABLE Course (
    CourseC VARCHAR(100)  PRIMARY KEY,
    LecturerID INT,
    CourseName VARCHAR(100),
    StartDt DATE,
    EndDt DATE,
    FOREIGN KEY (LecturerID) REFERENCES Lecturer(LecturerID)
);

CREATE TABLE StudentCourses (
    StudentID INT,
    CourseC VARCHAR(100) ,
    PRIMARY KEY (StudentID, CourseC),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (CourseC) REFERENCES Course(CourseC)
);

CREATE TABLE Assignments (
    AssignmentID INT PRIMARY KEY,
    CourseC VARCHAR(100),
    Title VARCHAR(100),
    Description TEXT,
    Submission VARCHAR(100),
    DueDate DATE,
    FOREIGN KEY (CourseC) REFERENCES Course(CourseC)
);

CREATE TABLE Calendar (
    EventID INT PRIMARY KEY,
    CourseC VARCHAR(100),
    Title VARCHAR(100),
	StartDt DATE,
    EndDt DATE,
    FOREIGN KEY (CourseC) REFERENCES Course(CourseC)
);

CREATE TABLE CourseContent (
    CourseContentID INT PRIMARY KEY,
    CourseC VARCHAR(100),
    FOREIGN KEY (CourseC) REFERENCES Course(CourseC)
);

CREATE TABLE Section (
    SectionID INT,
    CourseContentID INT,
    ContentType ENUM('links', 'files', 'slides'),
    ContentPath VARCHAR(255),
    PRIMARY KEY (SectionID),
    FOREIGN KEY (CourseContentID) REFERENCES CourseContent(CourseContentID)
);

CREATE TABLE DiscussionForum (
    DiscussionForumID INT PRIMARY KEY,
    CourseC VARCHAR(100),
    Name VARCHAR(100),
    FOREIGN KEY (CourseC) REFERENCES Course(CourseC)
);

CREATE TABLE DiscussionThread (
    DiscussionThreadID INT PRIMARY KEY,
    DiscussionForumID INT,
    StudentID INT,
    Title VARCHAR(100),
    Content TEXT,
    FOREIGN KEY (DiscussionForumID) REFERENCES DiscussionForum(DiscussionForumID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID)
);


CREATE TABLE DiscussionThreadReply (
    DiscussionThreadReplyID INT PRIMARY KEY,
    StudentID INT,
    DiscussionThreadID INT,
    Content TEXT,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (DiscussionThreadID) REFERENCES DiscussionThread(DiscussionThreadID)
);

CREATE TABLE AssignmentSubmission (
    StudentID INT,
    AssignmentID INT,
    SubmissionDate DATE,
    Grade DECIMAL(5,2),
    PRIMARY KEY (StudentID, AssignmentID),
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (AssignmentID) REFERENCES Assignments(AssignmentID)
);
