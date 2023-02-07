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

    def save(self, path: str = None):
        """This will save the current scene"""
        if path:
            file = File(path, **eval_script_returning_object(f'File("{path}")'))
            extend_file_object = format_to_extend(file)
            return self._eval_on_this_object(f'save({extend_file_object})')
        else:
            return self._eval_on_this_object('save()')


# ADOBE GENERAL OBJECTS

# ADOBE

class File(PydobeBaseObject):
    def __init__(self, path=None, pydobe_id=None):
        super().__init__(pydobe_id)

    def __str__(self):
        return self.full_name

    # PROPERTIES

    "The full path name"

    @property
    def full_name(self):
        return self._eval_on_this_object('fullName')

    "The file name portion of the absolute URI, without the path specification."

    @property
    def name(self):
        return self._eval_on_this_object('name')

    "The path portion of the absolute URI, without the file name"

    @property
    def path(self):
        return self._eval_on_this_object('path')