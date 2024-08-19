import sqlite3


def create_tables():
    conn = sqlite3.connect('nurse_schedule.db')
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS days (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shift TEXT UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS nurses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nurse_id TEXT UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_id INTEGER,
            shift_id INTEGER,
            head_nurse_id TEXT,
            junior_nurse_id TEXT,
            FOREIGN KEY(day_id) REFERENCES days(id),
            FOREIGN KEY(shift_id) REFERENCES shifts(id),
            FOREIGN KEY(head_nurse_id) REFERENCES nurses(nurse_id),
            FOREIGN KEY(junior_nurse_id) REFERENCES nurses(nurse_id)
        )
    ''')

    conn.commit()
    conn.close()


def save_schedule_to_db(schedule):
    conn = sqlite3.connect('nurse_schedule.db')
    c = conn.cursor()

    # Create tables if they don't exist
    create_tables()

    # Insert schedule data into the table
    for day, shifts in schedule.items():
        for shift, nurses in shifts.items():
            # Insert or ignore days and shifts
            c.execute("INSERT OR IGNORE INTO days (day) VALUES (?)", (day,))
            c.execute("INSERT OR IGNORE INTO shifts (shift) VALUES (?)", (shift,))

            # Get IDs for days and shifts
            c.execute("SELECT id FROM days WHERE day=?", (day,))
            day_id = c.fetchone()[0]

            c.execute("SELECT id FROM shifts WHERE shift=?", (shift,))
            shift_id = c.fetchone()[0]

            # Insert nurses
            for nurse in nurses["Head Nurse"] + nurses["Junior Nurse"]:
                c.execute(
                    "INSERT OR IGNORE INTO nurses (nurse_id) VALUES (?)", (nurse,))

            # Insert schedule
            for nurse in nurses["Head Nurse"]:
                c.execute("INSERT INTO schedule (day_id, shift_id, head_nurse_id) VALUES (?, ?, ?)",
                          (day_id, shift_id, nurse))

            for nurse in nurses["Junior Nurse"]:
                c.execute("INSERT INTO schedule (day_id, shift_id, junior_nurse_id) VALUES (?, ?, ?)",
                          (day_id, shift_id, nurse))

    conn.commit()
    conn.close()
