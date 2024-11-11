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

# Function to generate mock data for Meeting Notes
def generate_meeting_notes_entries(num_entries=300, household_ids_range=(1, 300)):
    meeting_types = ["introductory", "investment review", "retirement planning", "estate planning"]
    observations = [
        "Client seemed optimistic about the market",
        "Discussed concerns about inflation",
        "Noted client preference for low-risk investments",
        "Follow-up needed on estate planning",
        "Client expressed interest in more frequent updates"
    ]
    
    action_item_templates = [
        "Review portfolio performance",
        "Schedule follow-up call in two weeks",
        "Provide options for tax-advantaged accounts",
        "Send educational materials on investment strategies",
        "Update risk tolerance profile"
    ]
    
    for _ in range(num_entries):
        household_id = random.randint(*household_ids_range)
        meeting_date = fake.date_between(start_date="-3y", end_date="today")
        meeting_type = random.choice(meeting_types)
        
        # Randomly select 1-3 contacts from the household as attendees
        num_attendees = random.randint(1, 3)
        attendees = [fake.first_name() for _ in range(num_attendees)]
        
        # Randomly generate transcript and observations
        transcript = fake.paragraph(nb_sentences=5)
        observation = random.choice(observations)
        
        # Create 1-3 action items for each meeting
        action_items = [random.choice(action_item_templates) for _ in range(random.randint(1, 3))]
        action_items_str = ", ".join(action_items)  # Convert list to comma-separated string

        # Create an SQL insert statement for the MeetingNotes table
        entry = (
            f"INSERT INTO MeetingNotes (householdId, date, attendees, transcript, "
            f"meetingType, advisorObservations, actionItems) "
            f"VALUES ({household_id}, '{meeting_date}', '{', '.join(attendees)}', "
            f"'{transcript}', '{meeting_type}', '{observation}', '{action_items_str}');"
        )
        cursor.execute(entry)  # Execute SQL command for MeetingNotes

# Run generation functions and commit to database
try:
    generate_meeting_notes_entries()
    conn.commit()  # Commit all transactions
    print("Database seeded successfully with mock meeting notes.")
except Exception as e:
    conn.rollback()  # Rollback in case of any error
    print("Error seeding database:", e)
finally:
    cursor.close()
    conn.close()  # Ensure connection is closed
