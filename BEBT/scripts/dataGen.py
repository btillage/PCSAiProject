import psycopg2
import random
from faker import Faker
from datetime import date, timedelta

# Initialize Faker instance
fake = Faker()
Faker.seed(0)

# Database connection - replace with your actual database details
conn = psycopg2.connect(
    host="localhost",            # Replace with your host, e.g., "localhost" or IP address
    database="wealth_management", # Replace with your database name
    user="your_username",         # Replace with your database username
    password="your_password"      # Replace with your database password
)

# Set up a cursor to execute SQL commands
cursor = conn.cursor()

def generate_age_range(base_age):
    age_min = base_age - random.randint(5, 10)
    age_max = base_age + random.randint(5, 10)
    return f"{age_min}-{age_max}"

def generate_household_entries(num_entries=300):
    income_brackets = ["low", "middle", "high"]
    communication_channels = ["email", "phone", "text", "in-person"]
    communication_styles = ["concise", "detailed", "visual learner"]
    risk_tolerances = ["low", "medium", "high"]
    
    for _ in range(num_entries):
        base_age = random.randint(25, 70)
        children = random.randint(0, 4)
        
        # Create an SQL insert statement for the Household table
        entry = (
            f"INSERT INTO Household (name, ageRange, profession, familySize, "
            f"incomeBracket, location, preferredCommunicationChannel, communicationStyle, riskTolerance) "
            f"VALUES ('{fake.last_name()} Family', '{generate_age_range(base_age)}', "
            f"'{fake.job()}', {children + 2}, "
            f"'{random.choice(income_brackets)}', '{fake.city()}', "
            f"'{random.choice(communication_channels)}', '{random.choice(communication_styles)}', "
            f"'{random.choice(risk_tolerances)}');"
        )
        cursor.execute(entry)  # Execute SQL command for Household

def generate_contact_entries(num_entries=300, household_ids_range=(1, 300)):
    relationships = ["primary client", "spouse", "child", "parent"]
    personalities = ["analytical", "relationship-focused", "data-driven", "pragmatic", "risk-averse"]

    for _ in range(num_entries):
        household_id = random.randint(*household_ids_range)
        age = random.randint(25, 70) if random.choice([True, False]) else random.randint(15, 24)
        
        # Create an SQL insert statement for the Contact table
        entry = (
            f"INSERT INTO Contact (householdId, age, profession, preferredName, "
            f"primaryContactMethod, relationshipToHousehold, personalityType) "
            f"VALUES ({household_id}, {age}, '{fake.job()}', '{fake.first_name()}', "
            f"'{random.choice(['email', 'phone', 'text'])}', "
            f"'{random.choice(relationships)}', '{random.choice(personalities)}');"
        )
        cursor.execute(entry)  # Execute SQL command for Contact

def generate_account_entries(num_entries=300, household_ids_range=(1, 300)):
    account_types = ["retirement", "education", "growth", "savings", "checking"]
    risk_profiles = ["low", "moderate", "high"]
    contribution_frequencies = ["monthly", "quarterly", "annually"]

    for _ in range(num_entries):
        household_id = random.randint(*household_ids_range)
        account_type = random.choice(account_types)
        balance = round(random.uniform(1000, 1000000), 2)
        creation_date = fake.date_between(start_date="-20y", end_date="today")
        
        # Custom logic for risk based on account type
        risk_profile = random.choice(risk_profiles) if account_type in ["growth", "retirement"] else "low"
        
        # Create an SQL insert statement for the Account table
        entry = (
            f"INSERT INTO Account (householdId, accountType, balance, creationDate, "
            f"riskProfile, contributionFrequency) "
            f"VALUES ({household_id}, '{account_type}', {balance}, '{creation_date}', "
            f"'{risk_profile}', '{random.choice(contribution_frequencies)}');"
        )
        cursor.execute(entry)  # Execute SQL command for Account

# Generate and insert data into the database
try:
    generate_household_entries()
    generate_contact_entries()
    generate_account_entries()
    conn.commit()  # Commit all transactions
    print("Database seeded successfully with diverse and varied entries.")
except Exception as e:
    conn.rollback()  # Rollback in case of any error
    print("Error seeding database:", e)
finally:
    cursor.close()
    conn.close()  # Ensure connection is closed
