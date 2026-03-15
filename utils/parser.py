from fitparse import FitFile
from models.run import Run

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
    splits     = []
    gps_points = []
    hr_seconds = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for message in fitfile.get_messages():
        if message.name == "session":
            # TODO: extract total distance, duration, avg HR, max HR,
            #       elevation gain, start time, sport type
            pass

        elif message.name == "lap":
            # TODO: extract per-split pace, HR, distance, elevation
            pass

        elif message.name == "record":
            # TODO: extract per-second lat, lon, elevation, HR, speed, distance
            # TODO: use HR to increment hr_seconds for the right zone
            pass

    return Run(name="My Run")  # placeholder until we implement the parsing logic


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


def semicircles_to_degrees(semicircles: int) -> float:
    """Convert .fit file semicircle coordinates to degrees."""
    return semicircles * (180 / 2**31)