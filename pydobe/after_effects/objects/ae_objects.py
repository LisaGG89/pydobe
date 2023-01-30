from pydobe.core import PydobeBaseObject, PydobeBaseCollection, _format_to_extend, _eval_script_returning_object


# OBJECTS

class Application(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)

    # PROPERTIES

    """ This is the current active project. """

    @property
    def project(self):
        kwargs = self._eval_on_this_object('project')
        return Project(**kwargs) if kwargs else None


class Project(PydobeBaseObject):
    def __init__(self, pydobe_id=None):
        super().__init__(pydobe_id)
