import csv
import mysql.connector
from datetime import datetime

# T4: Define valid statuses allowed by our R2 refactoring
VALID_STATUSES = {'P', 'C', 'X', 'H', 'R'}

def parse_appt_date(raw):
    """ T1: Convert '15/03/2024 09:30' -> datetime object """
    # Addresses Data Type smell by converting text to proper date objects
    try:
        return datetime.strptime(raw, '%d/%m/%Y %H:%M')
    except (ValueError, TypeError):
        return None

def split_room(raw):
    """ T2: 'Room 3 Block B' -> (3, 'Block B') """
    # Addresses Non-Atomic Fields smell by separating room number from block
    try:
        parts = raw.split(' ')
        room_no = int(parts[1])  # Extracts the number (e.g., 3)
        block = " ".join(parts[2:]) # Extracts the block (e.g., 'Block B')
        return room_no, block
    except (IndexError, ValueError):
        return 0, "Unknown"

def migrate(csv_path, db_config):
    """ Main ETL Function """
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    skipped = []
    success_count = 0

    print(f"Starting migration from {csv_path}...")

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # T4: Validate status; skip and log unknown codes to prevent FK errors
            if row['status'] not in VALID_STATUSES:
                skipped.append(row['appt_id'])
                continue
            
            appt_dt = parse_appt_date(row['appt_date']) # T1 transformation
            room_no, block = split_room(row['room'])    # T2 transformation
            
            # T3: patient_nm, patient_ph, doc_name intentionally omitted (Duplicate Data fix)
            sql = """INSERT INTO appointments 
                     (appt_id, patient_id, doc_id, appt_datetime, status, fee, discount, room_number, building_block) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, (
                row['appt_id'], row['patient_id'], row['doc_id'], 
                appt_dt, row['status'], row['fee'], row['discount'], 
                room_no, block
            ))
            success_count += 1
            
    conn.commit()
    print(f"Migration Completed Successfully!")
    print(f"Total Rows Migrated: {success_count}")
    print(f"Total Rows Skipped (Invalid Status): {len(skipped)}")
    if skipped:
        print(f"Skipped IDs: {skipped}")
        
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Update these credentials with your local MySQL setup
    config = {
        "host": "localhost",
        "user": "root",
        "password": "your_password_here",
        "database": "hospital_db"
    }
    migrate('legacy_appointments.csv', config)
