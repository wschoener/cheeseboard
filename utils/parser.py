from anyio import run
import uuid
from db import Session
from fitparse import FitFile
from models.run import Run
from models.runner import Runner
from models.running_data import FitData
from db import Session

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="fitparse")


def parse_fit(filepath: str, runner: Runner) -> Run:
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
    running_data: list[dict] = []
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
            # TODO: create running_data entries for each GPS point, including timestamp, lat/lon, speed, heart rate, 
            #       and calculate effort pace and HR zone for each point and elevation if available and step_length if available
            #       and cadence if available
            running_data_entry = {
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
            running_data.append(running_data_entry)  # <-- this line was missing

            calculate_time_in_zones(run_data, message.get_value("heart_rate"), runner)

            run_data["run_duration"] += 1  # assuming each record is 1 second apart, increment total run duration

        elif message.name == "activity":
            # TODO: extract activity-level information
            run_data["total_duration_s"] = message.get_value("total_timer_time")
            run_data["start_time"] = message.get_value("timestamp")


    # Calculate averages, and min/max values for the Run model based on the running_data and splits
    pace_values = [entry["speed"] for entry in running_data if entry.get("speed") is not None]
    hr_values = [entry["heart_rate"] for entry in running_data if entry.get("heart_rate") is not None]

    max_hr = max(hr_values) if hr_values else None
    avg_hr = int(sum(hr_values) / len(hr_values)) if hr_values else None
    avg_pace_s = float(sum(pace_values) / float(len(pace_values))) if pace_values else None

    # after the for loop:
    with Session() as session:
        run = Run(
            id=run_uuid,
            name="My Run",
            runner_id=runner.id,
            distance_m=total_distance_run,
            total_power=total_power,
            start_date_time=run_data.get("start_date_time"),
            avg_hr=avg_hr,
            max_hr=max_hr,
            avg_pace_s=avg_pace_s,
            total_duration_s=run_data.get("total_timer_time"),
            run_duration_s=run_data.get("run_duration"),
            time_in_zone_1=run_data.get("time_in_zone_1"),
            time_in_zone_2=run_data.get("time_in_zone_2"),
            time_in_zone_3=run_data.get("time_in_zone_3"),
            time_in_zone_4=run_data.get("time_in_zone_4"),
            time_in_zone_5=run_data.get("time_in_zone_5"),
        )
        session.add(run)
        session.flush()  # inserts the run and makes its ID available without committing yet
        session.add_all([FitData(**entry) for entry in running_data])
        session.commit()  # commits both run and running_data together

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

def calculate_time_in_zones(run_data: dict, hr: int, runner: Runner) -> None:
    """
    Look at heart rate in message, compare to runner's HR zones, and increment time in the appropriate zone in run_data.
    """
    if hr is None:
        return

    if runner.hr_zone_1_stop and hr <= runner.hr_zone_1_stop:
        run_data["time_in_zone_1"] = run_data.get("time_in_zone_1", 0) + 1
    elif runner.hr_zone_2_stop and hr <= runner.hr_zone_2_stop:
        run_data["time_in_zone_2"] = run_data.get("time_in_zone_2", 0) + 1
    elif runner.hr_zone_3_stop and hr <= runner.hr_zone_3_stop:
        run_data["time_in_zone_3"] = run_data.get("time_in_zone_3", 0) + 1
    elif runner.hr_zone_4_stop and hr <= runner.hr_zone_4_stop:
        run_data["time_in_zone_4"] = run_data.get("time_in_zone_4", 0) + 1
    elif runner.hr_zone_5_stop and hr <= runner.hr_zone_5_stop:
        run_data["time_in_zone_5"] = run_data.get("time_in_zone_5", 0) + 1
