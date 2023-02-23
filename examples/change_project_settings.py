import pydobe

# Retrieve project object
project = pydobe.objects.app.project

# Set project settings
project.bits_per_channel = 8
project.working_space = "ACEScg ACES Working Space AMPAS S-2014-004"
project.time_display_type = "Frames"
project.frames_use_feet_frames = False
project.frames_count_type = "Start at 0"
