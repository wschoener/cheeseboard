import fitparse
import click
from rich.console import Console
from db import Session, engine
from utils.parser import parse_fit
from models.run import Run
import fitparse

console = Console()

"""
Parsed .fit file converted to readable format

SUCCESS
# File size: 90077, protocol version: 2.00, profile_version: 211.58
# File header CRC: expected=0xBF7D, calculated=0xBF7D
= TYPE=0 NAME=file_id NUMBER=0
--- type=4=activity
--- manufacturer=294=coros
--- time_created=1142081154=2026-03-10T12:45:54Z
--- product=804=804
--- product_name="COROS PACE 3"
==
= TYPE=3 NAME=developer_data_id NUMBER=207
--- manufacturer_id=294=coros
--- developer_data_index=0=0
--- application_id=0=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,71
==
= TYPE=4 NAME=device_info NUMBER=23
--- timestamp=1142081154=2026-03-10T12:45:54Z
--- manufacturer=294=coros
--- product_name="COROS PACE 3"
==
= TYPE=1 NAME=activity NUMBER=34
--- timestamp=1142078881=2026-03-10T12:08:01Z
--- total_timer_time=2227300=2227.300 s
--- local_timestamp=1142064481=1142064481
--- num_sessions=1=1
--- type=0=manual
--- event=26=activity
--- event_type=1=stop
==
= TYPE=10 NAME=event NUMBER=21
--- timestamp=1142078881=2026-03-10T12:08:01Z
--- event=0=timer
--- event_type=0=start
--- event_group=0=0
==
= TYPE=9 NAME=record NUMBER=20
--- activity_type=1=running
--- timestamp=1142078881=2026-03-10T12:08:01Z
--- distance=0=0.00 m
==
= TYPE=9 NAME=record NUMBER=20
--- activity_type=1=running
--- timestamp=1142078882=2026-03-10T12:08:02Z
--- position_lat=504500094=42.2867094 deg
--- position_long=-999275547=-83.7583088 deg
--- distance=0=0.00 m
--- heart_rate=82=82 bpm
==


etc...

= TYPE=9 NAME=record NUMBER=20
--- activity_type=1=running
--- timestamp=1142081109=2026-03-10T12:45:09Z
--- position_lat=504502889=42.2869437 deg
--- position_long=-999274525=-83.7582231 deg
--- distance=623500=6235.00 m
--- heart_rate=167=167 bpm
--- speed=2964=10.670 km/h
--- cadence=85=85 rpm
--- power=240=240 watts
--- accumulated_power=479607=479607 watts
--- stance_time=2150=215.0 ms
--- vertical_oscillation=960=96.0 mm
--- vertical_ratio=940=9.40 %
--- step_length=10400=1040.0 mm
--- 0_16_Effort_Pace=2.96300005912781=2.96300005912781
==
= TYPE=10 NAME=event NUMBER=21
--- timestamp=1142081109=2026-03-10T12:45:09Z
--- event=0=timer
--- event_type=4=stop_all
--- event_group=0=0
==
= TYPE=8 NAME=field_description NUMBER=206
--- developer_data_index=0=0
--- field_definition_number=16=16
--- fit_base_type_id=136=float32
--- field_name="Effort Pace"
--- units="m/s"
==
= TYPE=7 NAME=lap NUMBER=19
--- message_index=0=selected=0,reserved=0,mask=0
--- timestamp=1142079181=2026-03-10T12:13:01Z
--- start_time=1142078881=2026-03-10T12:08:01Z
--- total_timer_time=300000=300.000 s
--- total_elapsed_time=300000=300.000 s
--- total_distance=77217=772.17 m
--- total_calories=64=64 kcal
--- sport=1=running
--- max_heart_rate=154=154 bpm
--- min_heart_rate=82=82 bpm
--- avg_heart_rate=140=140 bpm
--- avg_temperature=24=24 deg.C
--- max_speed=2653=9.551 km/h
--- avg_speed=2574=9.266 km/h
--- avg_running_cadence=79=79 strides/min
--- avg_step_length=9700=970.0 mm
--- max_running_cadence=82=82 strides/min
--- total_descent=28=28 m
--- total_ascent=0=0 m
--- avg_power=173=173 watts
--- avg_stance_time=2640=264.0 ms
--- avg_stance_time_percent=0=0.00 %
--- avg_vertical_oscillation=990=99.0 mm
--- avg_vertical_ratio=1040=10.40 %
--- 0_16_Effort_Pace=2.95799994468689=2.95799994468689
==
= TYPE=7 NAME=lap NUMBER=19
--- message_index=1=selected=0,reserved=0,mask=1
--- timestamp=1142080805=2026-03-10T12:40:05Z
--- start_time=1142079181=2026-03-10T12:13:01Z
--- total_timer_time=1520530=1520.530 s
--- total_elapsed_time=1623270=1623.270 s
--- total_distance=466097=4660.97 m
--- total_calories=388=388 kcal
--- sport=1=running
--- max_heart_rate=175=175 bpm
--- min_heart_rate=133=133 bpm
--- avg_heart_rate=159=159 bpm
--- avg_temperature=20=20 deg.C
--- max_speed=3546=12.766 km/h
--- avg_speed=3065=11.034 km/h
--- avg_running_cadence=85=85 strides/min
--- avg_step_length=10800=1080.0 mm
--- max_running_cadence=90=90 strides/min
--- total_descent=22=22 m
--- total_ascent=28=28 m
--- avg_power=237=237 watts
--- avg_stance_time=2230=223.0 ms
--- avg_stance_time_percent=0=0.00 %
--- avg_vertical_oscillation=990=99.0 mm
--- avg_vertical_ratio=930=9.30 %
--- 0_16_Effort_Pace=2.95799994468689=2.95799994468689
==
= TYPE=7 NAME=lap NUMBER=19
--- message_index=2=selected=0,reserved=0,mask=2
--- timestamp=1142081105=2026-03-10T12:45:05Z
--- start_time=1142080805=2026-03-10T12:40:05Z
--- total_timer_time=300000=300.000 s
--- total_elapsed_time=300000=300.000 s
--- total_distance=79435=794.35 m
--- total_calories=70=70 kcal
--- sport=1=running
--- max_heart_rate=177=177 bpm
--- min_heart_rate=158=158 bpm
--- avg_heart_rate=165=165 bpm
--- avg_temperature=19=19 deg.C
--- max_speed=3356=12.082 km/h
--- avg_speed=2648=9.533 km/h
--- avg_running_cadence=80=80 strides/min
--- avg_step_length=9900=990.0 mm
--- max_running_cadence=89=89 strides/min
--- total_descent=5=5 m
--- total_ascent=13=13 m
--- avg_power=222=222 watts
--- avg_stance_time=2590=259.0 ms
--- avg_stance_time_percent=0=0.00 %
--- avg_vertical_oscillation=980=98.0 mm
--- avg_vertical_ratio=960=9.60 %
--- 0_16_Effort_Pace=2.95799994468689=2.95799994468689
==
= TYPE=2 NAME=session NUMBER=18
--- sport=1=running
--- start_time=1142078881=2026-03-10T12:08:01Z
--- timestamp=1142081109=2026-03-10T12:45:09Z
--- total_elapsed_time=2227300=2227.300 s
--- total_timer_time=2120530=2120.530 s
--- total_distance=623701=6237.01 m
--- total_calories=523=523 kcal
--- max_heart_rate=177=177 bpm
--- min_heart_rate=82=82 bpm
--- avg_heart_rate=157=157 bpm
--- avg_temperature=21=21 deg.C
--- total_ascent=41=41 m
--- total_descent=55=55 m
--- total_strides=2972=2972 strides
--- max_running_cadence=90=90 strides/min
--- avg_running_cadence=83=83 strides/min
--- avg_step_length=10600=1060.0 mm
--- max_speed=3546=12.766 km/h
--- avg_speed=2941=10.588 km/h
--- avg_power=226=226 watts
--- avg_stance_time=2340=234.0 ms
--- avg_stance_time_balance=0=0.00 %
--- avg_vertical_oscillation=990=99.0 mm
--- avg_vertical_ratio=950=9.50 %
--- 0_16_Effort_Pace=2.95799994468689=2.95799994468689
==
# CRC: expected=0x53FF, calculated=0x53FF
"""


@click.command("import")
@click.argument("filepath", type=click.Path(exists=True))
def import_cmd(filepath):
    """Import a .fit file and store it in the database."""

    console.print(f"[bold]Parsing[/bold] {filepath}...")

    fitfile = fitparse.FitFile(filepath)

    # Iterate over all messages of type "record"
    # (other types include "device_info", "file_creator", "event", etc)
    logged_run = Run(name="My Run")  # TODO: get name from user input or fit file metadata

    with Session() as session:
        session.add(logged_run)
        session.commit()  # commit to get an ID for the run, which we need for the foreign key in Splits, HRZone, and GPSPoints

    # new_run_messages = fitfile.get_messages()
    # for record in new_run_messages:
    #     console.print(f"Message type: {record.name}, fields: {record.fields}")

    # for record in fitfile.get_messages("record"):

        # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
        # for data in record:
            # print(data.name, data.value, data.units)

            # Print the name and value of the data (and the units if it has any)
            # if data.units:
                # console.print(" * {}: {} ({})".format(data.name, data.value, data.units))
            # else:
                # console.print(" * {}: {}".format(data.name, data.value))
            
            

        # console.print("---")
    # TODO: call parse_fit(filepath) to get parsed data
    # TODO: create a Run, its Splits, HRZone, and GPSPoints
    # TODO: save everything to the DB via Session
    # TODO: print a success summary using rich

    console.print("[green]Done![/green]")
