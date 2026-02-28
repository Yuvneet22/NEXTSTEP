from app.database import engine
from sqlalchemy import text

def try_add_column(table, col, col_type):
    with engine.connect() as conn:
        try:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}"))
            conn.commit()
            print(f"Added {col} to {table}")
        except Exception as e:
            if "already exists" in str(e):
                print(f"{col} already exists in {table}")
            else:
                print(f"Error adding {col} to {table}: {e}")

def update_schema():
    print("Starting robust schema update...")
    
    # Appointments table
    try_add_column("appointments", "razorpay_order_id", "VARCHAR")
    try_add_column("appointments", "razorpay_payment_id", "VARCHAR")
    try_add_column("appointments", "counsellor_joined", "BOOLEAN DEFAULT FALSE")
    try_add_column("appointments", "joined_at", "TIMESTAMP")
    
    # Tickets table
    try_add_column("tickets", "admin_reply", "TEXT")
    
    # Users table
    try_add_column("users", "role", "VARCHAR DEFAULT 'student'")
    
    print("Schema update complete.")

if __name__ == "__main__":
    update_schema()
