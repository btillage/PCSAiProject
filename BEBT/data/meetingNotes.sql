-- Create MeetingNotes table
CREATE TABLE MeetingNotes (
    id SERIAL PRIMARY KEY,
    householdId INT,
    date DATE,
    attendees TEXT,              -- List of contacts as JSON or comma-separated names/IDs
    transcript TEXT,
    meetingType VARCHAR(50),     -- e.g., "introductory", "investment review", "retirement planning"
    advisorObservations TEXT,    -- Notes or observations made by the advisor
    actionItems TEXT,            -- JSON or comma-separated list of action items
    FOREIGN KEY (householdId) REFERENCES Household(id)
);
