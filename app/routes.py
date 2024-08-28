from flask import Blueprint, render_template, request, jsonify
import json
from datetime import datetime, timedelta
from .harmony_search import HarmonySearch
from .models import save_schedule_to_db

main = Blueprint('main', __name__)


def get_dates_for_days(start_date, days):
    day_map = {}
    current_date = start_date

    for day in days:
        day_map[day] = current_date.isoformat()
        current_date += timedelta(days=1)

    return day_map


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    data = request.json

    # Parse the input from the form
    days = data['days']
    shifts = data['shifts']
    nurses = {
        "Head Nurse": data['head_nurses'],
        "Junior Nurse": data['junior_nurses']
    }
    min_head_nurses_per_shift = int(data['min_head_nurses'])
    harmony_memory_size = int(data['harmony_memory_size'])
    max_iterations = int(data['max_iterations'])
    harmony_memory_consideration_rate = float(
        data['harmony_memory_consideration_rate'])
    pitch_adjustment_rate = float(data['pitch_adjustment_rate'])

    # Initialize Harmony Search with the provided parameters
    hs = HarmonySearch(
        nurses, days, shifts, min_head_nurses_per_shift,
        harmony_memory_size, max_iterations,
        harmony_memory_consideration_rate, pitch_adjustment_rate
    )

    # Run the Harmony Search algorithm to generate the schedule
    best_schedule = hs.run()

    # Save the schedule to the database
    save_schedule_to_db(best_schedule)

    # Calculate the start date for the schedule display
    today = datetime.now()
    start_date = today + \
        timedelta(days=(7 - today.weekday() if today.weekday() > 0 else 0))
    dates_map = get_dates_for_days(start_date, days)

    # Formatting the schedule for the frontend display
    formatted_schedule = {}
    for day in days:
        formatted_schedule[day] = {}
        for shift in shifts:
            formatted_schedule[day][shift] = {
                "Head Nurse": best_schedule.get(day, {}).get(shift, {}).get('Head Nurse', []),
                "Junior Nurse": best_schedule.get(day, {}).get(shift, {}).get('Junior Nurse', [])
            }

    # Debugging: Log the formatted schedule to the console
    # print('Formatted Schedule:', json.dumps(formatted_schedule, indent=2))

    # Return the formatted schedule as a JSON response
    return jsonify({'schedule': formatted_schedule})
