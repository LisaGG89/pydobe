from pydobe.core import PydobeBaseObject, PydobeBaseCollection, format_to_extend, eval_script_returning_object


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

    # FUNCTIONS

    def close(self, save=None):
        """This will close the current project with an option to save changes or not"""
        if save is None:
            return self._eval_on_this_object('close(CloseOptions.PROMPT_TO_SAVE_CHANGES)')
        elif save:
            return self._eval_on_this_object('close(CloseOptions.SAVE_CHANGES)')
        else:
            return self._eval_on_this_object('close(CloseOptions.DO_NOT_SAVE_CHANGES)')
