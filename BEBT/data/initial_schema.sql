-- initial_schema.sql: Define the structure of the tables

DROP TABLE IF EXISTS Household, Contact, Account;

CREATE TABLE Household (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    ageRange VARCHAR(50),
    profession VARCHAR(50),
    familySize INT,
    incomeBracket VARCHAR(50),
    location VARCHAR(50),
    preferredCommunicationChannel VARCHAR(50),
    communicationStyle VARCHAR(50),
    riskTolerance VARCHAR(50)
);

CREATE TABLE Contact (
    id SERIAL PRIMARY KEY,
    householdId INT,
    age INT,
    profession VARCHAR(50),
    preferredName VARCHAR(100),
    primaryContactMethod VARCHAR(50),
    relationshipToHousehold VARCHAR(50),
    personalityType VARCHAR(50),
    FOREIGN KEY (householdId) REFERENCES Household(id)
);

CREATE TABLE Account (
    id SERIAL PRIMARY KEY,
    householdId INT,
    accountType VARCHAR(50),
    balance DECIMAL(15, 2),
    creationDate DATE,
    riskProfile VARCHAR(50),
    contributionFrequency VARCHAR(50),
    FOREIGN KEY (householdId) REFERENCES Household(id)
);
