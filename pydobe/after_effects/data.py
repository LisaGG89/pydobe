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
