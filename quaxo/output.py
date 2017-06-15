import datetime
import json
from cement.core import handler, output

from cement.utils.misc import minimal_logger

LOG = minimal_logger(__name__)

class QuaxoJsonEncoder(json.JSONEncoder):
    """Serialize decimal.Decimal objects into JSON as floats."""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d")
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class OutputHandler(output.CementOutputHandler):
    class Meta:
        interface = output.IOutput
        overridable = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _setup(self, app):
        super()._setup(app)

class DefaultOutputHandler(OutputHandler):
    class Meta:
        label = 'default'

    def render(self, data, *args, **kwargs):
        return data

class JSONOutputHandler(OutputHandler):
    class Meta:
        label = 'json'

    def render(self, data, *args, **kwargs):
        del(kwargs["template"])
        return json.dumps(data, *args, cls=QuaxoJsonEncoder, **kwargs)

def load(app):
    handler.register(DefaultOutputHandler)
    handler.register(JSONOutputHandler)
