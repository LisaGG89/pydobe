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
