from flask import Blueprint, render_template
import json
from datetime import datetime, timedelta
from .harmony_search import HarmonySearch
from .models import save_schedule_to_db

main = Blueprint('main', __name__)

def get_nurse_schedule_config():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    shifts = ["Morning", "Afternoon", "Night"]
    nurses = {
        "Head Nurse": ["HN1", "HN2", "HN3", "HN4", "HN5", "HN6", "HN7", "H8", "H9", "H10", "H11", "H12"],
        "Junior Nurse": ["JN1", "JN2", "JN3", "JN4", "JN5", "JN6", "JN7", "JN8", "JN9", "JN10", "JN11", "J12", "J13", "J14", "J15", "J16", "J17", "J18", "J19", "J20", "J21", "J22", "J23", "J24", "J25", "J26"]
    }
    config = {
        'days': days,
        'shifts': shifts,
        'nurses': nurses,
        'min_head_nurses_per_shift': 1,
        'harmony_memory_size': 10,
        'max_iterations': 1000,
        'harmony_memory_consideration_rate': 0.9,
        'pitch_adjustment_rate': 0.3,
    }
    return config

def get_dates_for_days(start_date, days):
    day_map = {}
    current_date = start_date

    for day in days:
        day_map[day] = current_date.isoformat()
        current_date += timedelta(days=1)

    return day_map

@main.route('/')
def index():
    config = get_nurse_schedule_config()
    days = config['days']
    shifts = config['shifts']
    nurses = config['nurses']
    min_head_nurses_per_shift = config['min_head_nurses_per_shift']
    harmony_memory_size = config['harmony_memory_size']
    max_iterations = config['max_iterations']
    harmony_memory_consideration_rate = config['harmony_memory_consideration_rate']
    pitch_adjustment_rate = config['pitch_adjustment_rate']

    hs = HarmonySearch(nurses, days, shifts, min_head_nurses_per_shift, harmony_memory_size,
                       max_iterations, harmony_memory_consideration_rate, pitch_adjustment_rate)
    best_schedule = hs.run()
    save_schedule_to_db(best_schedule)

    today = datetime.now()
    start_date = today + timedelta(days=(7 - today.weekday() if today.weekday() > 0 else 0))

    dates_map = get_dates_for_days(start_date, days)

    formatted_schedule = {}
    for day, shifts in best_schedule.items():
        formatted_schedule[day] = shifts

    return render_template('index.html', schedule=json.dumps(formatted_schedule, indent=4))