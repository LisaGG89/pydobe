from pydobe.after_effects.objects.ae_objects import *
from pydobe.core import eval_script_returning_object, is_port_open

class Root(object):
    def __init__(self):
        super(Root, self).__init__()
        is_port_open()
    """ The application object """

    @property
    def app(self):
        return Application(**eval_script_returning_object('app'))
