from collections import UserDict


class IntStringDict(UserDict):
    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            pass
        try:
            for k, v in self.data.items():
                if v == key:
                    return k
        except KeyError:
            pass
        raise KeyError(key)

    def __setitem__(self, key, value):
        if type(key).__name__ == "int":
            self.data[key] = value
        elif type(key).__name__ == "str":
            self.data[value] = key

def hex_to_rgb(hex, float=False):
    hex_value = hex.lstrip('#')
    colour_value_list = list(int(hex_value[i:i + 2], 16) for i in (0, 2, 4))
    if float:
        colour_value_list = rgb_int_to_float(colour_value_list)
    return colour_value_list


def rgb_int_to_float(rgb):
    rgb_float = []
    for x in rgb:
        rgb_float.append(x / 255)
    return rgb_float


def format_colour(value):
    if type(value) == str:
        return hex_to_rgb(value, float=True)
    else:
        if type(value[0]) == int:
            return rgb_int_to_float(value)
        elif type(value[0]) == float:
            return value