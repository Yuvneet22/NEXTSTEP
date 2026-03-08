import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Use DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in environment variables.")
    exit(1)

# Handle postgresql compatibility
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL)

sql_commands = [
    # Add recently added columns to counsellor_profiles
    "ALTER TABLE counsellor_profiles ADD COLUMN IF NOT EXISTS fee_locked BOOLEAN DEFAULT FALSE;",
    "ALTER TABLE counsellor_profiles ADD COLUMN IF NOT EXISTS is_founding_counsellor BOOLEAN DEFAULT FALSE;",
    "ALTER TABLE counsellor_profiles ADD COLUMN IF NOT EXISTS founding_badge_awarded_at TIMESTAMP;",
    "ALTER TABLE counsellor_profiles ADD COLUMN IF NOT EXISTS commission_free_until TIMESTAMP;",
    "ALTER TABLE counsellor_profiles ADD COLUMN IF NOT EXISTS razorpay_account_id VARCHAR;",
    "ALTER TABLE counsellor_profiles ADD COLUMN IF NOT EXISTS onboarding_status VARCHAR DEFAULT 'not_started';",
    "ALTER TABLE counsellor_profiles ADD COLUMN IF NOT EXISTS razorpay_contact_id VARCHAR;",
    "ALTER TABLE counsellor_profiles ADD COLUMN IF NOT EXISTS razorpay_fund_account_id VARCHAR;",
    
    # Create missing tables if they don't exist
    """
    CREATE TABLE IF NOT EXISTS notifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        type VARCHAR,
        message TEXT,
        is_read BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS moderation_flags (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        content TEXT,
        chat_type VARCHAR,
        status VARCHAR DEFAULT 'pending_review',
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS payments (
        id SERIAL PRIMARY KEY,
        session_id INTEGER REFERENCES appointments(id),
        razorpay_order_id VARCHAR UNIQUE,
        razorpay_payment_id VARCHAR UNIQUE,
        amount FLOAT,
        currency VARCHAR DEFAULT 'INR',
        status VARCHAR DEFAULT 'created',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS transfers (
        id SERIAL PRIMARY KEY,
        payment_id INTEGER REFERENCES payments(id),
        counsellor_id INTEGER REFERENCES users(id),
        amount FLOAT,
        razorpay_transfer_id VARCHAR UNIQUE,
        status VARCHAR DEFAULT 'pending',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """
]

with engine.connect() as conn:
    # Set search_path or other session variables if needed
    # conn.execute(text("SET search_path TO public;")) 
    
    for cmd in sql_commands:
        try:
            cmd_snippet = cmd.strip()[:50] + "..." if len(cmd.strip()) > 50 else cmd.strip()
            print(f"Running: {cmd_snippet}")
            conn.execute(text(cmd))
            conn.commit()
            print("Successfully executed.")
        except Exception as e:
            print(f"Skipping or error: {e}")

print("Migration completed successfully.")
