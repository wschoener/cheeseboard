import uuid
from db import Session
from fitparse import FitFile
from models.run import Run
from models.fit_data import FitData
from db import Session

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="fitparse")


# HR zone thresholds as % of max HR — adjust to your own max HR
MAX_HR = 190
ZONE_BOUNDS = [0.60, 0.70, 0.80, 0.90, 1.0]


def parse_fit(filepath: str) -> Run:
    """
    Parse a .fit file and return a dict with:
      - run_data: dict of fields for the Run model
      - splits: list of dicts for Split model
      - gps_points: list of dicts for GPSPoint model
      - hr_zones: dict of zone -> seconds

    TODO: This is the heart of the project — implement the parsing logic.

    Hints:
      - fitparse gives you 'messages' of different types
      - 'record' messages = per-second GPS/HR data points
      - 'lap' messages = split/lap summaries
      - 'session' message = overall activity summary
      - All values come back as semicircles for lat/lon — divide by 11930465 to get degrees
      - Speeds are in m/s — convert to pace as: pace_s = 1609.34 / speed_ms
    """
    fitfile = FitFile(filepath)

    run_data   = {}
    fit_data: list[dict] = []
    splits     = []
    gps_points = []
    hr_seconds = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    total_distance_run = 0.0

    run_uuid = uuid.uuid4()  # generate a new UUID for this run

    run_data["run_duration"] = 0

    for message in fitfile.get_messages():
        if message.name == "activity":
            run_data["start_date_time"] = message.get_value("timestamp")
            run_data["total_timer_time"] = message.get_value("total_timer_time")

        elif message.name == "lap":
            # TODO: extract per-split pace, HR, distance, elevation
            pass

        elif message.name == "record":
            # TODO: create fit_data entries for each GPS point, including timestamp, lat/lon, speed, heart rate, 
            #       and calculate effort pace and HR zone for each point and elevation if available and step_length if available
            #       and cadence if available
            fit_data_entry = {
                "timestamp": message.get_value("timestamp"),
                "position_lat": semicircles_to_degrees(message.get_value("position_lat")),
                "position_long": semicircles_to_degrees(message.get_value("position_long")) ,
                "speed": message.get_value("speed"),
                "heart_rate": message.get_value("heart_rate"),
                "heart_rate_zone": hr_to_zone(message.get_value("heart_rate")),
                "elevation": message.get_value("altitude"),
                "step_length": message.get_value("step_length"),
                "cadence": message.get_value("cadence"),
                "power": message.get_value("power"),
                "run_id": run_uuid  # associate this FitData entry with the Run we created above
            }
            total_distance_run = message.get_value("distance")
            total_power = message.get_value("accumulated_power")
            fit_data.append(fit_data_entry)  # <-- this line was missing

            run_data["run_duration"] += 1  # assuming each record is 1 second apart, increment total run duration

        elif message.name == "activity":
            # TODO: extract activity-level information
            run_data["total_duration_s"] = message.get_value("total_timer_time")
            run_data["start_time"] = message.get_value("timestamp")


    # Calculate averages, and min/max values for the Run model based on the fit_data and splits
    pace_values = [entry["speed"] for entry in fit_data if entry.get("speed") is not None]
    hr_values = [entry["heart_rate"] for entry in fit_data if entry.get("heart_rate") is not None]

    max_hr = max(hr_values) if hr_values else None
    avg_hr = int(sum(hr_values) / len(hr_values)) if hr_values else None
    avg_pace_s = float(sum(pace_values) / float(len(pace_values))) if pace_values else None

    # after the for loop:
    with Session() as session:
        run = Run(id=run_uuid, name="My Run", distance_m=total_distance_run, total_power=total_power, start_date_time=run_data.get("start_date_time"), avg_hr=avg_hr, max_hr=max_hr, avg_pace_s=avg_pace_s, total_duration_s=run_data.get("total_timer_time"), run_duration_s=run_data.get("run_duration"))
        session.add(run)
        session.flush()  # inserts the run and makes its ID available without committing yet
        session.add_all([FitData(**entry) for entry in fit_data])
        session.commit()  # commits both run and fit_data together

    return run

def hr_to_zone(hr: int) -> int:
    """
    TODO: given a heart rate in bpm, return the zone number (1-5)
    using MAX_HR and ZONE_BOUNDS defined above.
    """
    return 0


def speed_to_pace(speed_ms: float) -> int:
    """
    TODO: convert speed in meters/second to pace in seconds/mile.
    Formula: pace_s = 1609.34 / speed_ms
    Return 0 if speed_ms is 0 or None.
    """
    
    return 0


def semicircles_to_degrees(semicircles: int) -> float | None:
    if semicircles is None:
        return None
    return semicircles * (180 / 2**31)