-- Azure SQL Database Schema for DevOpsMCP
-- Run this script on your Azure SQL Database to create the required tables

-- Create Bugs table
CREATE TABLE Bugs (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(255),
    ProjectId NVARCHAR(100),
    CreatedAt DATETIME NOT NULL DEFAULT(GETDATE()),
    ClosedAt DATETIME NULL,
    Status NVARCHAR(50)
);

-- Create indexes for performance
CREATE INDEX IX_Bugs_ProjectId ON Bugs(ProjectId);
CREATE INDEX IX_Bugs_Status ON Bugs(Status);
CREATE INDEX IX_Bugs_CreatedAt ON Bugs(CreatedAt);
CREATE INDEX IX_Bugs_ClosedAt ON Bugs(ClosedAt);

-- Optional: Insert sample data for testing
/*
INSERT INTO Bugs (Title, ProjectId, CreatedAt, ClosedAt, Status)
VALUES 
    ('Login page crash', 'PROJ001', DATEADD(DAY, -15, GETDATE()), DATEADD(DAY, -10, GETDATE()), 'Closed'),
    ('API timeout error', 'PROJ001', DATEADD(DAY, -12, GETDATE()), DATEADD(DAY, -8, GETDATE()), 'Closed'),
    ('UI alignment issue', 'PROJ001', DATEADD(DAY, -9, GETDATE()), DATEADD(DAY, -5, GETDATE()), 'Closed'),
    ('Database connection', 'PROJ002', DATEADD(DAY, -7, GETDATE()), DATEADD(DAY, -3, GETDATE()), 'Closed'),
    ('Memory leak', 'PROJ001', DATEADD(DAY, -5, GETDATE()), DATEADD(DAY, -2, GETDATE()), 'Closed'),
    ('Security vulnerability', 'PROJ001', DATEADD(DAY, -3, GETDATE()), DATEADD(DAY, -1, GETDATE()), 'Closed'),
    ('Performance degradation', 'PROJ002', DATEADD(DAY, -2, GETDATE()), NULL, 'Open');
*/
