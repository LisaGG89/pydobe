import json
import requests
import socket

HOST = "127.0.0.1"
PORT = 2000
PANEL_URL = f"http://{HOST}:{PORT}"


class PydobeBaseObject(object):
    """Base object for every mirror object from ExtendScript"""

    def __init__(self, pydobe_id: str, object_type: str):
        self.pydobe_id = pydobe_id
        self.object_type = object_type

    def _eval_on_object(
        self, extend_property: str = "", pydobe_id: str = None, index: int = None
    ):
        """Query property or execute function on ExtendScript object"""
        if extend_property:
            extend_property = f".{extend_property}"
        if index:
            index = f"[{index}]"
        else:
            index = ""
        if pydobe_id:
            line = f"$._pydobe['{pydobe_id}']{index}{extend_property};"
        else:
            line = f"$._pydobe['{self.pydobe_id}']{index}{extend_property};"
        result = eval_script_returning_object(line)
        return result

    def _execute_command(self, code: str):
        eval_script(code)


class PydobeBaseCollection(PydobeBaseObject):
    def __init__(self, pydobe_id: str, object_type: str, len_property: str):
        """Base Object for collections"""

        if pydobe_id is None:
            raise ValueError("Creating a collection from scratch is not supported")
        self.len_property = len_property
        super(PydobeBaseCollection, self).__init__(pydobe_id, object_type)

    def __getitem__(self, index: int) -> dict:
        """Builtin method for getting the value at the specific index"""

        if index < 0:
            index = str(self.__len__() + index)
        return self._eval_on_object(index=index)

    def __len__(self) -> int:
        """Builtin method for length"""

        return int(self._eval_on_object(self.len_property))

    def __iter__(self):
        """Builtin method for iterating through items"""

        value = iter([self.__getitem__(i) for i in range(len(self))])
        return value


def is_port_open():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (HOST, PORT)
    result_of_check = a_socket.connect_ex(location)
    message = f"Connection to port {PORT} could not be established. Please ensure After Effects is running."
    if result_of_check != 0:
        raise ConnectionError(message)


def eval_script_returning_object(line: str):
    """Eval the line as ExtendScript code.
    If the code returns an object, it will be stored with an id for pydobe to handle"""
    # Create ExtendScript to send
    script = f"var tmp = {line}"
    script += """\nif(typeof tmp === 'object' && tmp !== null){
            var newPydobeId = $._pydobe.generateId();
            $._pydobe[newPydobeId] = tmp;
            tmp = ExtendJSON.stringify({"isObject": true, "objectType": tmp.reflect.name, "pydobeId": newPydobeId}, internal_variables_replacer, 0, 1);
        }
        tmp"""
    # Get the resulting data
    result = eval_script(script)
    # Extract pydobe ID if object is returned
    if isinstance(result, dict) and result.get("isObject"):
        if result["objectType"] == "Array" and "=" not in line:
            data_list = convert_to_list(line)
            return data_list
        else:
            kwargs = dict(
                pydobe_id=result["pydobeId"], object_type=result["objectType"]
            )
        return kwargs
    return result


def eval_script(code: str):
    """Send ExtendScript code to adobe software, retrieve and decode the response"""

    # send code to adobe software (adding try statement to prevent error popup message locking UI)
    response = requests.post(
        PANEL_URL,
        json={
            "to_eval": "try{\n"
            + code
            + "\n}catch(e){e.error=true;ExtendJSON.stringify(e)}"
        },
    )

    # handle response
    data = response.text

    # Check if the data is an object. If it is - decode it. If not - return data as text
    try:
        decoded_data = json.loads(data)
    except json.decoder.JSONDecodeError:
        return data
    return decoded_data


def format_to_extend(obj):
    """Format the argument to ExtendScript"""
    if isinstance(obj, PydobeBaseObject):
        return f'$._pydobe["{obj.pydobe_id}"]'
    elif isinstance(obj, bool):
        return str(obj).lower()
    elif isinstance(obj, list):
        return f"[{', '.join([format_to_extend(item) for item in obj])}]"


def convert_to_list(line):
    data_list = []
    count_line = f"{line[:-1]}.length;"
    count = eval_script_returning_object(count_line)
    for index in range(count):
        value_line = f"{line[:-1]}[{index}];"
        value = eval_script_returning_object(value_line)
        data_list.append(value)
    return data_list


def create_python_object(object_type):
    subclasses = get_all_subclasses(PydobeBaseObject)
    for subclass in subclasses:
        if subclass.__name__ == object_type:
            return subclass


def get_all_subclasses(cls):
    all_subclasses = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))
    return all_subclasses
