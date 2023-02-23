from pydobe.utils import IntStringDict

label_dictionary = IntStringDict(
    {
        0: "None",
        1: "Red",
        2: "Yellow",
        3: "Aqua",
        4: "Pink",
        5: "Lavender",
        6: "Peach",
        7: "Sea Foam",
        8: "Blue",
        9: "Green",
        10: "Purple",
        11: "Orange",
        12: "Brown",
        13: "Fuchsia",
        14: "Cyan",
        15: "Sandstone",
        16: "Dark Green",
    }
)

alpha_dictionary = IntStringDict(
    {5413: "Ignore", 5412: "Straight", 5414: "Premultiplied"}
)

field_separation_dictionary = IntStringDict(
    {5613: "Off", 5612: "Upper Field First", 5614: "Lower Field First"}
)

pulldown_dictionary = IntStringDict(
    {
        5813: "Off",
        5812: "WSSWW",
        5814: "SSWWW",
        5815: "SWWWS",
        5816: "WWWSS",
        5817: "WWSSW",
        5818: "WWWSW",
        5819: "WWSWW",
        5820: "WSWWW",
        5821: "SWWWW",
        5822: "WWWWS",
    }
)

time_display_dictionary = IntStringDict(
    {2013: "Frames", 2012: "Timecode"}
)

use_feet_and_frames_dictionary = IntStringDict(
    {2413: "35mm", 2412: "16mm"}
)

frames_count_dictionary = IntStringDict(
    {2612: "Start at 0", 2613: "Start at 1", 2614: "Timecode Conversion"}
)

footage_start_time_dictionary = IntStringDict(
    {2212: "Use Media Source", 2213: "00:00:00:000"}
)

gpu_accel_type_dictionary = IntStringDict(
    {1813: "CUDA", 1814: "Metal", 1815: "OPENCL", 1816: "SOFTWARE"}
)

tool_dictionary = IntStringDict(
    {9012: "Selection Tool",
     9013: "Rotation Tool",
     9015: "Orbit Around Camera POI Tool",
     9016: "Pan Camera POI Tool",
     9017: "Dolly to Camera POI Tool",
     9018: "Brush Tool",
     9019: "Clone Stamp Tool",
     9020: "Eraser Tool",
     9021: "Hand Tool",
     9022: "Zoom Tool",
     9023: "Pan Behind Tool",
     9024: "Rectangle Tool",
     9025: "Rounded Rectangle Tool",
     9026: "Ellipse Tool",
     9027: "Polygon Tool",
     9028: "Star Tool",
     9029: "Horizontal Type Tool",
     9030: "Vertical Type Tool",
     9031: "Pen Tool",
     9032: "Mask Feather Tool",
     9033: "Add Vertex Tool",
     9034: "Delete Vertex Tool",
     9035: "Convert Vertex Tool",
     9036: "Puppet Position Pin Tool",
     9037: "Puppet Starch Pin Tool",
     9038: "Puppet Bend Pin Tool",
     9040: "Puppet Overlap Pin Tool",
     9041: "Roto Brush Tool",
     9042: "Refine Edge Tool",
     9043: "Puppet Advanced Pin Tool",
     9044: "Oribit Around Cursor Tool",
     9045: "Oribit Around Scene Tool",
     9046: "Pan Under Cursor Tool",
     9047: "Dolly Towards Cursor Tool",
     9048: "Dolly To Cursor Tool"
    }
)