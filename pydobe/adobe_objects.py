from pydobe.core import PydobeBaseObject

class File(PydobeBaseObject):
    def __init__(self,  pydobe_id=None):
        super().__init__(pydobe_id)

    def __str__(self):
        return self.full_name

    # PROPERTIES

    "The full path name"

    @property
    def full_name(self) -> str:
        return self._eval_on_this_object('fullName')

    "The file name portion of the absolute URI, without the path specification."

    @property
    def name(self) -> str:
        return self._eval_on_this_object('name')

    "The path portion of the absolute URI, without the file name"

    @property
    def path(self) -> str:
        return self._eval_on_this_object('path')
