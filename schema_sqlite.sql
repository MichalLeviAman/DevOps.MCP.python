-- DevOpsMCP Database Schema (SQLite)
-- This script creates all tables and inserts sample data

-- Projects table
CREATE TABLE IF NOT EXISTS Projects (
    ProjectId INTEGER PRIMARY KEY AUTOINCREMENT,
    AzureProjectId TEXT NOT NULL,
    ProjectName TEXT NOT NULL,
    Description TEXT,
    IsActive INTEGER DEFAULT 1,
    CreatedOn DATETIME DEFAULT CURRENT_TIMESTAMP,
    LastSync DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- WorkItems table
CREATE TABLE IF NOT EXISTS WorkItems (
    WorkItemId INTEGER PRIMARY KEY AUTOINCREMENT,
    AzureWorkItemId INTEGER NOT NULL,
    ProjectId INTEGER NOT NULL,
    Title TEXT NOT NULL,
    WorkItemType TEXT,
    State TEXT,
    AssignedTo TEXT,
    CreatedDate DATETIME,
    ChangedDate DATETIME,
    ClosedDate DATETIME,
    Priority INTEGER,
    IterationPath TEXT,
    AreaPath TEXT,
    Tags TEXT,
    LastSync DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ProjectId) REFERENCES Projects(ProjectId)
);

-- Pipelines table
CREATE TABLE IF NOT EXISTS Pipelines (
    PipelineId INTEGER PRIMARY KEY AUTOINCREMENT,
    AzurePipelineId INTEGER NOT NULL,
    ProjectId INTEGER NOT NULL,
    PipelineName TEXT NOT NULL,
    TriggerType TEXT,
    LastRunId INTEGER,
    LastRunStatus TEXT,
    LastRunDate DATETIME,
    DurationSeconds INTEGER,
    LastSync DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ProjectId) REFERENCES Projects(ProjectId)
);

-- Commits table
CREATE TABLE IF NOT EXISTS Commits (
    CommitId INTEGER PRIMARY KEY AUTOINCREMENT,
    AzureCommitId TEXT NOT NULL,
    ProjectId INTEGER NOT NULL,
    Author TEXT,
    CommitDate DATETIME,
    Comment TEXT,
    Branch TEXT,
    AssociatedWorkItemId INTEGER,
    LastSync DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ProjectId) REFERENCES Projects(ProjectId),
    FOREIGN KEY (AssociatedWorkItemId) REFERENCES WorkItems(WorkItemId)
);

-- Bugs table (main table for bug tracking)
CREATE TABLE IF NOT EXISTS Bugs (
    BugId INTEGER PRIMARY KEY AUTOINCREMENT,
    WorkItemId INTEGER,
    AzureBugId TEXT NOT NULL,
    Severity TEXT,
    Resolution TEXT,
    FixedBy TEXT,
    FixedDate DATETIME,
    VerifiedBy TEXT,
    VerifiedDate DATETIME,
    Status TEXT,
    Notes TEXT,
    LastSync DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (WorkItemId) REFERENCES WorkItems(WorkItemId)
);

-- SyncLog table
CREATE TABLE IF NOT EXISTS SyncLog (
    SyncId INTEGER PRIMARY KEY AUTOINCREMENT,
    SyncDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Source TEXT,
    EntityType TEXT,
    RecordsFetched INTEGER,
    RecordsUpdated INTEGER,
    DurationSeconds INTEGER,
    IsSuccess INTEGER,
    ErrorMessage TEXT
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS IX_WorkItems_ProjectId ON WorkItems(ProjectId);
CREATE INDEX IF NOT EXISTS IX_WorkItems_State ON WorkItems(State);
CREATE INDEX IF NOT EXISTS IX_Bugs_Status ON Bugs(Status);
CREATE INDEX IF NOT EXISTS IX_Bugs_FixedDate ON Bugs(FixedDate);
CREATE INDEX IF NOT EXISTS IX_Bugs_WorkItemId ON Bugs(WorkItemId);
CREATE INDEX IF NOT EXISTS IX_Commits_ProjectId ON Commits(ProjectId);
CREATE INDEX IF NOT EXISTS IX_Pipelines_ProjectId ON Pipelines(ProjectId);

-- Insert Projects data
INSERT INTO Projects (ProjectId, AzureProjectId, ProjectName, Description, IsActive, CreatedOn, LastSync) VALUES
(1, '62981f7a-c8dd-48b0-913f-e56319498f28', 'HotRetailSys', 'Core retail operations project synchronized from Azure DevOps.', 1, '2025-11-10 15:05:58', '2025-11-10 15:05:58'),
(2, '4c978215-0830-4de9-9784-54c043b8de10', 'PaymentsGateway', 'Payment processing services & integrations.', 1, '2025-11-10 15:05:58', '2025-11-10 15:05:58'),
(3, 'a7f3d912-5b6c-4e8a-9d2f-1c4b8e7a3f90', 'MobileApp', 'Cross-platform mobile application for customers.', 1, '2025-09-15 10:30:00', '2025-11-23 10:30:00'),
(4, 'e9b2c5d8-4a1f-4c3e-8b7d-2f5a9c6e1d40', 'DataWarehouse', 'Enterprise data warehouse and BI platform.', 1, '2025-08-20 14:15:00', '2025-11-23 14:15:00'),
(5, 'f1a8b4c3-7e2d-4f9a-b5c8-3d6e2a9f7b10', 'CloudInfra', 'Cloud infrastructure and DevOps automation.', 1, '2025-10-01 09:00:00', '2025-11-23 09:00:00'),
(6, 'b4e7f2c9-3a1d-4f5e-9c8b-7d2a6e4f1b30', 'AltshulerCustomers', 'Customer management and CRM system for Altshuler Shaham.', 1, '2025-01-15 08:00:00', '2025-11-26 08:00:00');

-- Insert WorkItems data
INSERT INTO WorkItems (WorkItemId, AzureWorkItemId, ProjectId, Title, WorkItemType, State, AssignedTo, CreatedDate, ChangedDate, ClosedDate, Priority, IterationPath, AreaPath, Tags, LastSync) VALUES
(1, 12034, 1, 'API: Fix null reference in StockController', 'Bug', 'Closed', 'michal@amandigital.local', '2025-10-27 15:05:58', '2025-10-29 15:05:58', '2025-10-29 15:05:58', 1, 'HotRetailSys\Sprint 27', 'HotRetailSys\Backend', 'backend;api;bug', '2025-11-10 15:05:58'),
(2, 12078, 1, 'Task: Add logging filter to WebApiBack', 'Task', 'Closed', 'dev1@amandigital.local', '2025-10-31 15:05:58', '2025-11-01 15:05:58', '2025-11-01 15:05:58', 2, 'HotRetailSys\Sprint 27', 'HotRetailSys\Backend', 'logging;filters;devops', '2025-11-10 15:05:58'),
(3, 12122, 1, 'User Story: As a manager, see fixed bugs trend', 'User Story', 'Active', 'pm@amandigital.local', '2025-11-03 15:05:58', '2025-11-09 15:05:58', NULL, 2, 'HotRetailSys\Sprint 28', 'HotRetailSys\Analytics', 'bi;analytics;reports', '2025-11-10 15:05:58'),
(4, 33011, 2, 'Bug: Refund rounding issue on VAT', 'Bug', 'Active', 'sharon@amandigital.local', '2025-11-05 15:05:58', '2025-11-10 15:05:58', NULL, 1, 'PaymentsGateway\Sprint 12', 'PaymentsGateway\Core', 'finance;bug;urgent', '2025-11-10 15:05:58'),
(5, 33045, 2, 'Task: Add CI pipeline for checkout service', 'Task', 'Closed', 'devops@amandigital.local', '2025-11-02 15:05:58', '2025-11-03 15:05:58', '2025-11-03 15:05:58', 2, 'PaymentsGateway\Sprint 11', 'PaymentsGateway\DevOps', 'pipeline;ci;yaml', '2025-11-10 15:05:58'),
(6, 45012, 3, 'Bug: Crash on iOS when opening profile', 'Bug', 'Closed', 'avi@amandigital.local', '2025-09-20 10:00:00', '2025-09-25 10:00:00', '2025-09-25 10:00:00', 1, 'MobileApp\Sprint 15', 'MobileApp\iOS', 'mobile;ios;crash', '2025-11-23 10:00:00'),
(7, 45023, 3, 'Feature: Add biometric authentication', 'Feature', 'Closed', 'ron@amandigital.local', '2025-10-05 12:00:00', '2025-10-20 12:00:00', '2025-10-20 12:00:00', 2, 'MobileApp\Sprint 17', 'MobileApp\Security', 'security;auth', '2025-11-23 12:00:00'),
(8, 45034, 3, 'Bug: Image upload fails on Android', 'Bug', 'Active', 'dana@amandigital.local', '2025-11-15 14:30:00', '2025-11-20 14:30:00', NULL, 1, 'MobileApp\Sprint 19', 'MobileApp\Android', 'android;upload', '2025-11-23 14:30:00'),
(9, 67001, 4, 'Bug: ETL job timeout on large datasets', 'Bug', 'Closed', 'yael@amandigital.local', '2025-08-25 09:00:00', '2025-09-10 09:00:00', '2025-09-10 09:00:00', 1, 'DataWarehouse\Sprint 8', 'DataWarehouse\ETL', 'etl;performance', '2025-11-23 09:00:00'),
(10, 67012, 4, 'Task: Optimize fact table indexes', 'Task', 'Closed', 'eli@amandigital.local', '2025-10-10 11:00:00', '2025-10-15 11:00:00', '2025-10-15 11:00:00', 2, 'DataWarehouse\Sprint 10', 'DataWarehouse\Database', 'optimization;index', '2025-11-23 11:00:00'),
(11, 67023, 4, 'Bug: Dashboard query returns wrong totals', 'Bug', 'Active', 'tomer@amandigital.local', '2025-11-18 16:00:00', '2025-11-22 16:00:00', NULL, 1, 'DataWarehouse\Sprint 11', 'DataWarehouse\BI', 'dashboard;sql', '2025-11-23 16:00:00'),
(12, 89001, 5, 'Bug: Terraform state lock timeout', 'Bug', 'Closed', 'shai@amandigital.local', '2025-10-08 08:00:00', '2025-10-12 08:00:00', '2025-10-12 08:00:00', 1, 'CloudInfra\Sprint 5', 'CloudInfra\IaC', 'terraform;devops', '2025-11-23 08:00:00'),
(13, 89012, 5, 'Task: Migrate to Kubernetes 1.28', 'Task', 'Closed', 'lior@amandigital.local', '2025-11-01 10:00:00', '2025-11-10 10:00:00', '2025-11-10 10:00:00', 2, 'CloudInfra\Sprint 6', 'CloudInfra\K8s', 'kubernetes;upgrade', '2025-11-23 10:00:00'),
(14, 89023, 5, 'Bug: Monitoring alerts not firing', 'Bug', 'Active', 'maya@amandigital.local', '2025-11-20 13:00:00', '2025-11-22 13:00:00', NULL, 1, 'CloudInfra\Sprint 6', 'CloudInfra\Monitoring', 'alerts;prometheus', '2025-11-23 13:00:00'),
(15, 78001, 6, 'Bug: Customer search returns duplicate records', 'Bug', 'Closed', 'rachel@amandigital.local', '2025-02-10 09:00:00', '2025-02-15 09:00:00', '2025-02-15 09:00:00', 1, 'AltshulerCustomers\Sprint 3', 'AltshulerCustomers\Search', 'search;duplicate', '2025-11-26 09:00:00'),
(16, 78012, 6, 'Bug: Email validation fails on international domains', 'Bug', 'Closed', 'omer@amandigital.local', '2025-03-20 10:30:00', '2025-03-25 10:30:00', '2025-03-25 10:30:00', 2, 'AltshulerCustomers\Sprint 5', 'AltshulerCustomers\Validation', 'email;validation', '2025-11-26 10:30:00'),
(17, 78023, 6, 'Bug: Customer merge creates orphaned records', 'Bug', 'Closed', 'tal@amandigital.local', '2025-04-15 11:00:00', '2025-04-20 11:00:00', '2025-04-20 11:00:00', 1, 'AltshulerCustomers\Sprint 7', 'AltshulerCustomers\DataIntegrity', 'merge;data', '2025-11-26 11:00:00'),
(18, 78034, 6, 'Bug: Export to Excel truncates long notes', 'Bug', 'Closed', 'nir@amandigital.local', '2025-05-10 12:00:00', '2025-05-15 12:00:00', '2025-05-15 12:00:00', 2, 'AltshulerCustomers\Sprint 9', 'AltshulerCustomers\Export', 'excel;export', '2025-11-26 12:00:00'),
(19, 78045, 6, 'Bug: Customer portal login timeout', 'Bug', 'Closed', 'shira@amandigital.local', '2025-06-05 13:30:00', '2025-06-10 13:30:00', '2025-06-10 13:30:00', 1, 'AltshulerCustomers\Sprint 11', 'AltshulerCustomers\Auth', 'login;timeout', '2025-11-26 13:30:00'),
(20, 78056, 6, 'Bug: Phone number formatting inconsistent', 'Bug', 'Closed', 'dor@amandigital.local', '2025-07-12 14:00:00', '2025-07-18 14:00:00', '2025-07-18 14:00:00', 2, 'AltshulerCustomers\Sprint 13', 'AltshulerCustomers\Format', 'phone;format', '2025-11-26 14:00:00'),
(21, 78067, 6, 'Bug: Customer notes not saving properly', 'Bug', 'Active', 'yael@amandigital.local', '2025-08-20 15:00:00', '2025-11-20 15:00:00', NULL, 1, 'AltshulerCustomers\Sprint 15', 'AltshulerCustomers\Notes', 'save;notes', '2025-11-26 15:00:00'),
(22, 78078, 6, 'Bug: Advanced search filters not persisting', 'Bug', 'Active', 'moshe@amandigital.local', '2025-09-15 16:00:00', '2025-11-18 16:00:00', NULL, 2, 'AltshulerCustomers\Sprint 17', 'AltshulerCustomers\Search', 'filters;persistence', '2025-11-26 16:00:00'),
(23, 78089, 6, 'Bug: Customer dashboard loading slowly', 'Bug', 'Active', 'chen@amandigital.local', '2025-10-10 09:30:00', '2025-11-15 09:30:00', NULL, 1, 'AltshulerCustomers\Sprint 19', 'AltshulerCustomers\Performance', 'dashboard;performance', '2025-11-26 09:30:00'),
(24, 78090, 6, 'Bug: Bulk update fails on large datasets', 'Bug', 'New', 'avi@amandigital.local', '2025-11-01 10:00:00', '2025-11-01 10:00:00', NULL, 1, 'AltshulerCustomers\Sprint 21', 'AltshulerCustomers\BulkOps', 'bulk;update', '2025-11-26 10:00:00'),
(25, 78091, 6, 'Bug: Customer segmentation logic incorrect', 'Bug', 'New', 'liora@amandigital.local', '2025-11-10 11:00:00', '2025-11-10 11:00:00', NULL, 2, 'AltshulerCustomers\Sprint 21', 'AltshulerCustomers\Segmentation', 'segment;logic', '2025-11-26 11:00:00');

-- Insert Pipelines data
INSERT INTO Pipelines (PipelineId, AzurePipelineId, ProjectId, PipelineName, TriggerType, LastRunId, LastRunStatus, LastRunDate, DurationSeconds, LastSync) VALUES
(1, 501, 1, 'HotRetailSys.CI', 'CI', 8751, 'Succeeded', '2025-11-09 15:05:58', 382, '2025-11-10 15:05:58'),
(2, 742, 2, 'PaymentsGateway.Release', 'Scheduled', 2291, 'Failed', '2025-11-08 15:05:58', 611, '2025-11-10 15:05:58'),
(3, 301, 3, 'MobileApp.iOS.Build', 'CI', 4523, 'Succeeded', '2025-11-22 14:00:00', 295, '2025-11-23 14:00:00'),
(4, 302, 3, 'MobileApp.Android.Build', 'CI', 4524, 'Succeeded', '2025-11-22 14:30:00', 312, '2025-11-23 14:30:00'),
(5, 601, 4, 'DataWarehouse.ETL.Daily', 'Scheduled', 9821, 'Succeeded', '2025-11-23 02:00:00', 1847, '2025-11-23 08:00:00'),
(6, 801, 5, 'CloudInfra.Terraform.Apply', 'Manual', 1205, 'Succeeded', '2025-11-21 16:00:00', 421, '2025-11-23 16:00:00'),
(7, 701, 6, 'AltshulerCustomers.CI', 'CI', 5632, 'Succeeded', '2025-11-25 10:00:00', 285, '2025-11-26 10:00:00');

-- Insert Commits data
INSERT INTO Commits (CommitId, AzureCommitId, ProjectId, Author, CommitDate, Comment, Branch, AssociatedWorkItemId, LastSync) VALUES
(1, 'c44b1ab0', 1, 'dev2@amandigital.local', '2025-10-28 15:05:58', 'Fix NRE in StockController; add null checks', 'main', 1, '2025-11-10 15:05:58'),
(2, '1a9f77de', 1, 'dev1@amandigital.local', '2025-11-01 15:05:58', 'Add RequestLoggingFilter + GlobalExceptionFilter', 'main', 2, '2025-11-10 15:05:58'),
(3, '77b3e2aa', 2, 'devops@amandigital.local', '2025-11-03 15:05:58', 'Add checkout-service CI pipeline yaml', 'main', 5, '2025-11-10 15:05:58'),
(4, 'a3f9c2b1', 3, 'avi@amandigital.local', '2025-09-24 10:00:00', 'Fix iOS profile crash with nil check', 'main', 6, '2025-11-23 10:00:00'),
(5, 'b8d4e1a7', 3, 'ron@amandigital.local', '2025-10-19 12:00:00', 'Implement Face ID and Touch ID support', 'feature/biometric', 7, '2025-11-23 12:00:00'),
(6, 'f2c8a9d3', 4, 'yael@amandigital.local', '2025-09-08 09:00:00', 'Optimize ETL batch size and timeout settings', 'main', 9, '2025-11-23 09:00:00'),
(7, 'e7b3c4f1', 4, 'eli@amandigital.local', '2025-10-14 11:00:00', 'Add clustered indexes on fact tables', 'main', 10, '2025-11-23 11:00:00'),
(8, 'd9a2f5e8', 5, 'shai@amandigital.local', '2025-10-11 08:00:00', 'Fix terraform state locking with DynamoDB', 'main', 12, '2025-11-23 08:00:00'),
(9, 'c1b7e3a9', 5, 'lior@amandigital.local', '2025-11-09 10:00:00', 'Upgrade K8s cluster to version 1.28', 'main', 13, '2025-11-23 10:00:00'),
(10, 'a5e9b2c4', 6, 'rachel@amandigital.local', '2025-02-14 09:00:00', 'Fix duplicate customer search results', 'main', 15, '2025-11-26 09:00:00'),
(11, 'b7f3d1a8', 6, 'tal@amandigital.local', '2025-04-19 11:00:00', 'Resolve customer merge orphan records', 'main', 17, '2025-11-26 11:00:00'),
(12, 'c9e2a5f6', 6, 'shira@amandigital.local', '2025-06-09 13:30:00', 'Fix customer portal login timeout', 'main', 19, '2025-11-26 13:30:00');

-- Insert Bugs data (55+ records with realistic distribution)
INSERT INTO Bugs (BugId, WorkItemId, AzureBugId, Severity, Resolution, FixedBy, FixedDate, VerifiedBy, VerifiedDate, Status, Notes, LastSync) VALUES
-- Closed bugs (recent)
(1, 1, '12034', 'High', 'Fixed null reference in StockController', 'michal', '2025-11-10 12:06:57', 'noa', '2025-11-11 12:06:57', 'Closed', 'Verified in QA, deployed successfully.', '2025-11-11 12:06:57'),
(2, 2, '12078', 'Medium', 'Added logging filter to WebApiBack', 'dev1', '2025-11-08 12:06:57', NULL, NULL, 'Closed', 'Resolved log duplication issue.', '2025-11-11 12:06:57'),
(3, 5, '33045', 'Low', 'Resolved minor configuration issue in CI pipeline', 'devops', '2025-11-09 12:06:57', 'pm', '2025-11-10 12:06:57', 'Closed', 'Confirmed fix in build logs.', '2025-11-11 12:06:57'),
(4, 1, '12079', 'High', 'Updated API route mapping to fix 404 issue', 'michal', '2025-11-10 12:10:20', 'noa', '2025-11-11 12:10:20', 'Closed', 'API routing issue resolved in production.', '2025-11-11 12:10:20'),
(5, 2, '12080', 'Medium', 'Improved retry policy for DB connection', 'daniel', '2025-11-09 12:10:20', 'sara', '2025-11-10 12:10:20', 'Closed', 'Stabilized connection errors during sync.', '2025-11-11 12:10:20'),
(6, 3, '12123', 'Low', 'UI text fix on login page', 'noa', '2025-11-08 12:10:20', NULL, NULL, 'Closed', 'Fixed typo in login page label.', '2025-11-11 12:10:20'),
(7, 4, '12124', 'Critical', 'Patched SQL injection vulnerability', 'david', '2025-11-09 12:10:20', 'michal', '2025-11-10 12:10:20', 'Closed', 'Security fix approved by code review.', '2025-11-11 12:10:20'),
(8, 5, '12125', 'Medium', 'Resolved task duplication on dashboard', 'yossi', '2025-11-07 12:10:20', 'noa', '2025-11-09 12:10:20', 'Closed', 'UI duplication eliminated.', '2025-11-11 12:10:20'),
(9, 1, '12126', 'High', 'Corrected async deadlock in TaskBL', 'david', '2025-11-08 12:10:20', 'pm', '2025-11-11 12:10:20', 'Closed', 'Deadlock scenario eliminated under load.', '2025-11-11 12:10:20'),
(10, 2, '12127', 'Critical', 'Fixed failed authentication token refresh', 'michal', '2025-11-10 12:10:20', NULL, NULL, 'Closed', 'Token renewal now stable.', '2025-11-11 12:10:20'),
(11, 3, '12128', 'Low', 'Removed redundant log spam from middleware', 'devops', '2025-11-06 12:10:20', NULL, NULL, 'Closed', 'Cleaner logs for release 8.1', '2025-11-11 12:10:20'),
(12, 3, '12141', 'Medium', 'Updated scheduler logic', 'michal', '2025-11-09 12:10:20', NULL, NULL, 'Closed', 'Scheduler now runs reliably.', '2025-11-11 12:10:20'),
(13, 4, '12142', 'High', 'Optimized query with missing index', 'noa', '2025-11-08 12:10:20', NULL, NULL, 'Closed', 'Performance improved significantly.', '2025-11-11 12:10:20'),
(14, 2, '12143', 'Low', 'Fixed email header casing', 'yossi', '2025-11-07 12:10:20', NULL, NULL, 'Closed', 'Minor cosmetic fix.', '2025-11-11 12:10:20'),
(15, 5, '12144', 'Critical', 'Rebuilt CI/CD trigger definitions', 'devops', '2025-11-10 12:10:20', NULL, NULL, 'Closed', 'Fixed missing trigger chain.', '2025-11-11 12:10:20'),
(16, 1, '12145', 'Medium', 'Patched serialization error', 'daniel', '2025-11-08 12:10:20', 'sara', '2025-11-11 12:10:20', 'Closed', 'Serialization validated with test cases.', '2025-11-11 12:10:20'),

-- Active bugs (open issues)
(17, 3, '12122', 'Critical', NULL, NULL, NULL, NULL, NULL, 'Active', 'Trend chart for fixed bugs not showing recent data.', '2025-11-11 12:06:57'),
(18, 4, '33011', 'High', NULL, NULL, NULL, NULL, NULL, 'Active', 'Rounding issue in VAT refund calculation still reproduces.', '2025-11-11 12:06:57'),
(19, 4, '12129', 'Medium', NULL, NULL, NULL, NULL, NULL, 'Active', 'Pipeline step fails on deploy to staging.', '2025-11-11 12:10:20'),
(20, 5, '12130', 'High', NULL, NULL, NULL, NULL, NULL, 'Active', 'Data mismatch between DevOps summary and local DB.', '2025-11-11 12:10:20'),
(21, 3, '12131', 'Critical', NULL, NULL, NULL, NULL, NULL, 'Active', 'Memory spike on large build execution.', '2025-11-11 12:10:20'),
(22, 2, '12132', 'Medium', NULL, NULL, NULL, NULL, NULL, 'Active', 'Task completion email sent twice.', '2025-11-11 12:10:20'),
(23, 1, '12133', 'Low', NULL, NULL, NULL, NULL, NULL, 'Active', 'Graph rendering delay on summary charts.', '2025-11-11 12:10:20'),
(24, 4, '12134', 'High', NULL, NULL, NULL, NULL, NULL, 'Active', 'Branch status not updating on commit.', '2025-11-11 12:10:20'),
(25, 5, '12135', 'Critical', NULL, NULL, NULL, NULL, NULL, 'Active', 'API call to /sync/projects fails under load.', '2025-11-11 12:10:20'),

-- New bugs (not yet assigned/started)
(26, 3, '12136', 'High', NULL, NULL, NULL, NULL, NULL, 'New', 'DevOps webhook returns 500 intermittently.', '2025-11-11 12:10:20'),
(27, 4, '12137', 'Medium', NULL, NULL, NULL, NULL, NULL, 'New', 'Unexpected null value from GetProjectUsers.', '2025-11-11 12:10:20'),
(28, 5, '12138', 'Low', NULL, NULL, NULL, NULL, NULL, 'New', 'Tooltip not visible in bug overview grid.', '2025-11-11 12:10:20'),
(29, 1, '12139', 'Critical', NULL, NULL, NULL, NULL, NULL, 'New', 'User cannot reassign closed bugs via UI.', '2025-11-11 12:10:20'),
(30, 2, '12140', 'High', NULL, NULL, NULL, NULL, NULL, 'New', 'Duplicate notifications on reopened bugs.', '2025-11-11 12:10:20'),

-- Additional bugs for MobileApp (Project 3)
(31, 6, '45012', 'Critical', 'Fixed iOS crash with proper null handling', 'avi', '2025-09-25 10:00:00', 'ron', '2025-09-26 10:00:00', 'Closed', 'Critical crash on iOS 17 resolved.', '2025-11-23 10:00:00'),
(32, 7, '45020', 'Medium', 'Implemented biometric authentication', 'ron', '2025-10-20 12:00:00', 'avi', '2025-10-22 12:00:00', 'Closed', 'Face ID and Touch ID working perfectly.', '2025-11-23 12:00:00'),
(33, 8, '45034', 'High', NULL, NULL, NULL, NULL, NULL, 'Active', 'Image upload fails on Android 14 devices.', '2025-11-23 14:30:00'),
(34, 6, '45015', 'Low', 'Fixed button alignment on profile screen', 'dana', '2025-09-28 11:00:00', NULL, NULL, 'Closed', 'UI adjustment for iPhone SE.', '2025-11-23 11:00:00'),
(35, 7, '45025', 'Medium', 'Added offline mode for auth', 'ron', '2025-10-25 13:00:00', 'avi', '2025-10-27 13:00:00', 'Closed', 'Auth works offline with cached credentials.', '2025-11-23 13:00:00'),
(36, 8, '45038', 'Critical', NULL, NULL, NULL, NULL, NULL, 'Active', 'App crashes when selecting gallery on Samsung.', '2025-11-22 15:00:00'),
(37, 6, '45018', 'High', 'Fixed memory leak in image cache', 'avi', '2025-10-02 14:00:00', 'dana', '2025-10-05 14:00:00', 'Closed', 'Memory usage reduced by 40%.', '2025-11-23 14:00:00'),
(38, 7, '45028', 'Medium', 'Added biometric fallback to PIN', 'ron', '2025-11-01 16:00:00', NULL, NULL, 'Closed', 'PIN entry available when biometric fails.', '2025-11-23 16:00:00'),

-- Additional bugs for DataWarehouse (Project 4)
(39, 9, '67001', 'Critical', 'Optimized ETL batch processing', 'yael', '2025-09-10 09:00:00', 'eli', '2025-09-12 09:00:00', 'Closed', 'ETL now handles 10M rows without timeout.', '2025-11-23 09:00:00'),
(40, 10, '67012', 'Medium', 'Added clustered indexes on fact tables', 'eli', '2025-10-15 11:00:00', 'yael', '2025-10-17 11:00:00', 'Closed', 'Query performance improved 5x.', '2025-11-23 11:00:00'),
(41, 11, '67023', 'High', NULL, NULL, NULL, NULL, NULL, 'Active', 'Dashboard shows incorrect YTD totals.', '2025-11-23 16:00:00'),
(42, 9, '67005', 'Medium', 'Fixed date dimension missing weekends', 'tomer', '2025-09-15 10:00:00', 'eli', '2025-09-18 10:00:00', 'Closed', 'Date dimension now includes all days.', '2025-11-23 10:00:00'),
(43, 10, '67015', 'Low', 'Updated dim_customer with email field', 'yael', '2025-10-20 12:00:00', NULL, NULL, 'Closed', 'Customer dimension extended.', '2025-11-23 12:00:00'),
(44, 11, '67025', 'Critical', NULL, NULL, NULL, NULL, NULL, 'Active', 'Revenue report double counts transactions.', '2025-11-21 14:00:00'),
(45, 9, '67008', 'High', 'Fixed NULL handling in aggregations', 'eli', '2025-09-22 11:00:00', 'tomer', '2025-09-25 11:00:00', 'Closed', 'NULL values now excluded from SUM properly.', '2025-11-23 11:00:00'),
(46, 10, '67018', 'Medium', 'Optimized star schema joins', 'yael', '2025-10-28 13:00:00', 'eli', '2025-10-30 13:00:00', 'Closed', 'Reports load 3x faster now.', '2025-11-23 13:00:00'),

-- Additional bugs for CloudInfra (Project 5)
(47, 12, '89001', 'Critical', 'Fixed Terraform state lock with DynamoDB', 'shai', '2025-10-12 08:00:00', 'lior', '2025-10-14 08:00:00', 'Closed', 'State locking now uses DynamoDB consistently.', '2025-11-23 08:00:00'),
(48, 13, '89012', 'Medium', 'Upgraded Kubernetes to 1.28', 'lior', '2025-11-10 10:00:00', 'shai', '2025-11-12 10:00:00', 'Closed', 'K8s cluster upgraded without downtime.', '2025-11-23 10:00:00'),
(49, 14, '89023', 'High', NULL, NULL, NULL, NULL, NULL, 'Active', 'Prometheus alerts not triggering on high CPU.', '2025-11-23 13:00:00'),
(50, 12, '89004', 'Medium', 'Fixed EKS node autoscaling', 'maya', '2025-10-18 09:00:00', 'shai', '2025-10-20 09:00:00', 'Closed', 'Autoscaling now responds to load correctly.', '2025-11-23 09:00:00'),
(51, 13, '89015', 'Low', 'Updated Helm charts to v3.13', 'lior', '2025-11-15 11:00:00', NULL, NULL, 'Closed', 'Helm charts updated and tested.', '2025-11-23 11:00:00'),
(52, 14, '89026', 'Critical', NULL, NULL, NULL, NULL, NULL, 'Active', 'Grafana dashboard shows stale metrics.', '2025-11-22 15:00:00'),
(53, 12, '89007', 'High', 'Fixed VPC peering connection', 'shai', '2025-10-25 10:00:00', 'maya', '2025-10-27 10:00:00', 'Closed', 'VPC peering now routes traffic correctly.', '2025-11-23 10:00:00'),
(54, 13, '89018', 'Medium', 'Implemented pod disruption budgets', 'lior', '2025-11-18 12:00:00', 'shai', '2025-11-19 12:00:00', 'Closed', 'PDBs prevent service disruption during updates.', '2025-11-23 12:00:00'),
(55, 14, '89028', 'High', NULL, NULL, NULL, NULL, NULL, 'New', 'CloudWatch costs exceeding budget by 200%.', '2025-11-23 14:00:00'),

-- AltshulerCustomers bugs (Project 6) - Full year distribution
-- January-February 2025 (Closed bugs)
(56, 15, '78001', 'High', 'Fixed duplicate customer search with distinct query', 'rachel', '2025-02-15 09:00:00', 'omer', '2025-02-16 09:00:00', 'Closed', 'Search now returns unique customers only.', '2025-11-26 09:00:00'),
(57, 15, '78002', 'Medium', 'Optimized search index for better performance', 'rachel', '2025-02-20 10:00:00', 'tal', '2025-02-22 10:00:00', 'Closed', 'Search response time improved by 60%.', '2025-11-26 10:00:00'),
(58, 15, '78003', 'Critical', 'Fixed SQL injection in search query', 'rachel', '2025-02-25 11:00:00', 'security', '2025-02-26 11:00:00', 'Closed', 'Security vulnerability patched.', '2025-11-26 11:00:00'),

-- March 2025 (Closed bugs)
(59, 16, '78012', 'Medium', 'Added support for international email domains', 'omer', '2025-03-25 10:30:00', 'nir', '2025-03-27 10:30:00', 'Closed', 'Email validation now handles all TLDs.', '2025-11-26 10:30:00'),
(60, 16, '78013', 'Low', 'Updated email regex pattern', 'omer', '2025-03-28 11:00:00', NULL, NULL, 'Closed', 'Email validation more robust.', '2025-11-26 11:00:00'),

-- April 2025 (Closed bugs)
(61, 17, '78023', 'High', 'Fixed customer merge orphan records', 'tal', '2025-04-20 11:00:00', 'rachel', '2025-04-22 11:00:00', 'Closed', 'Merge operation now maintains referential integrity.', '2025-11-26 11:00:00'),
(62, 17, '78024', 'Critical', 'Added transaction rollback on merge failure', 'tal', '2025-04-25 12:00:00', 'omer', '2025-04-27 12:00:00', 'Closed', 'Database consistency maintained on errors.', '2025-11-26 12:00:00'),
(63, 17, '78025', 'Medium', 'Improved merge conflict detection', 'tal', '2025-04-28 13:00:00', 'nir', '2025-04-30 13:00:00', 'Closed', 'Merge conflicts detected before processing.', '2025-11-26 13:00:00'),

-- May 2025 (Closed bugs)
(64, 18, '78034', 'Medium', 'Fixed Excel export truncation issue', 'nir', '2025-05-15 12:00:00', 'shira', '2025-05-17 12:00:00', 'Closed', 'Notes field now supports up to 32K characters.', '2025-11-26 12:00:00'),
(65, 18, '78035', 'Low', 'Added CSV export option', 'nir', '2025-05-20 13:00:00', 'dor', '2025-05-22 13:00:00', 'Closed', 'Users can now export to CSV format.', '2025-11-26 13:00:00'),
(66, 18, '78036', 'High', 'Fixed special characters encoding in export', 'nir', '2025-05-25 14:00:00', 'rachel', '2025-05-27 14:00:00', 'Closed', 'UTF-8 encoding properly handled.', '2025-11-26 14:00:00'),

-- June 2025 (Closed bugs)
(67, 19, '78045', 'High', 'Fixed customer portal login timeout', 'shira', '2025-06-10 13:30:00', 'tal', '2025-06-12 13:30:00', 'Closed', 'Session timeout increased to 30 minutes.', '2025-11-26 13:30:00'),
(68, 19, '78046', 'Critical', 'Patched authentication bypass vulnerability', 'shira', '2025-06-15 14:00:00', 'security', '2025-06-16 14:00:00', 'Closed', 'Critical security fix deployed.', '2025-11-26 14:00:00'),
(69, 19, '78047', 'Medium', 'Added remember me functionality', 'shira', '2025-06-20 15:00:00', 'omer', '2025-06-22 15:00:00', 'Closed', 'Users can stay logged in for 7 days.', '2025-11-26 15:00:00'),

-- July 2025 (Closed bugs)
(70, 20, '78056', 'Medium', 'Standardized phone number formatting', 'dor', '2025-07-18 14:00:00', 'nir', '2025-07-20 14:00:00', 'Closed', 'All phone numbers now in +972-XX-XXXXXXX format.', '2025-11-26 14:00:00'),
(71, 20, '78057', 'Low', 'Added international phone number support', 'dor', '2025-07-22 15:00:00', 'shira', '2025-07-24 15:00:00', 'Closed', 'System supports all country codes.', '2025-11-26 15:00:00'),
(72, 20, '78058', 'High', 'Fixed phone validation for mobile numbers', 'dor', '2025-07-28 16:00:00', 'rachel', '2025-07-30 16:00:00', 'Closed', 'Mobile numbers validated correctly.', '2025-11-26 16:00:00'),

-- August 2025 (Active bugs)
(73, 21, '78067', 'High', NULL, NULL, NULL, NULL, NULL, 'Active', 'Customer notes not saving when clicking outside field.', '2025-11-26 15:00:00'),
(74, 21, '78068', 'Critical', NULL, NULL, NULL, NULL, NULL, 'Active', 'Auto-save causes data loss on concurrent edits.', '2025-11-26 15:30:00'),
(75, 21, '78069', 'Medium', NULL, NULL, NULL, NULL, NULL, 'Active', 'Rich text formatting lost when saving notes.', '2025-11-26 16:00:00'),

-- September 2025 (Active bugs)
(76, 22, '78078', 'Medium', NULL, NULL, NULL, NULL, NULL, 'Active', 'Advanced search filters reset on page refresh.', '2025-11-26 16:00:00'),
(77, 22, '78079', 'Low', NULL, NULL, NULL, NULL, NULL, 'Active', 'Filter presets not loading for new users.', '2025-11-26 16:30:00'),
(78, 22, '78080', 'High', NULL, NULL, NULL, NULL, NULL, 'Active', 'Date range filter returns incorrect results.', '2025-11-26 17:00:00'),

-- October 2025 (Active bugs)
(79, 23, '78089', 'High', NULL, NULL, NULL, NULL, NULL, 'Active', 'Customer dashboard loads slowly with 1000+ records.', '2025-11-26 09:30:00'),
(80, 23, '78088', 'Critical', NULL, NULL, NULL, NULL, NULL, 'Active', 'Dashboard crashes when loading large datasets.', '2025-11-26 10:00:00'),
(81, 23, '78087', 'Medium', NULL, NULL, NULL, NULL, NULL, 'Active', 'Chart rendering blocks UI thread.', '2025-11-26 10:30:00'),

-- November 2025 (New bugs)
(82, 24, '78090', 'High', NULL, NULL, NULL, NULL, NULL, 'New', 'Bulk update fails on datasets with 500+ records.', '2025-11-26 10:00:00'),
(83, 24, '78092', 'Critical', NULL, NULL, NULL, NULL, NULL, 'New', 'Bulk delete removes wrong customers.', '2025-11-26 10:30:00'),
(84, 24, '78093', 'Medium', NULL, NULL, NULL, NULL, NULL, 'New', 'Bulk import CSV validation too strict.', '2025-11-26 11:00:00'),

-- November 2025 (New bugs - continued)
(85, 25, '78091', 'Medium', NULL, NULL, NULL, NULL, NULL, 'New', 'Customer segmentation logic excludes valid customers.', '2025-11-26 11:00:00'),
(86, 25, '78094', 'Low', NULL, NULL, NULL, NULL, NULL, 'New', 'Segment preview shows incorrect count.', '2025-11-26 11:30:00'),
(87, 25, '78095', 'High', NULL, NULL, NULL, NULL, NULL, 'New', 'Dynamic segments not updating in real-time.', '2025-11-26 12:00:00');

-- Insert SyncLog data
INSERT INTO SyncLog (SyncId, SyncDate, Source, EntityType, RecordsFetched, RecordsUpdated, DurationSeconds, IsSuccess, ErrorMessage) VALUES
(1, '2025-11-08 15:05:58', 'Azure DevOps API', 'WorkItem', 45, 45, 12, 1, NULL),
(2, '2025-11-08 16:05:58', 'Azure DevOps API', 'Bug', 8, 7, 5, 1, NULL),
(3, '2025-11-08 17:05:58', 'Azure DevOps API', 'Pipeline', 2, 2, 3, 1, NULL),
(4, '2025-11-08 18:05:58', 'Azure DevOps API', 'Commit', 19, 19, 9, 1, NULL),
(5, '2025-11-08 19:05:58', 'Azure DevOps API', 'WorkItem', 12, 11, 6, 0, 'Timeout on iteration path query');
