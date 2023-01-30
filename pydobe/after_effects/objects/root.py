from pydobe.after_effects.objects.ae_objects import *
from pydobe.core import _eval_script_returning_object

class Root(object):
    def __init__(self):
        super(Root, self).__init__()

    """ The application object """

    @property
    def app(self):
        return Application(**_eval_script_returning_object('app'))
