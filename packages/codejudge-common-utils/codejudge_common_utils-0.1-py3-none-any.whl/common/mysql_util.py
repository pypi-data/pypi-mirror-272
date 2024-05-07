from django.db.models import Func
from django.forms import IntegerField


class TimestampDiff(Func):
    function = 'TIMESTAMPDIFF'
    template = "TIMESTAMPDIFF(SECOND, %(expressions)s)"
    output_field = IntegerField()
