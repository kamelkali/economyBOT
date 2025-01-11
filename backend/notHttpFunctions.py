from datetime import datetime
from django.utils.timezone import now, make_aware


def get_cooldown_date():

    timestamp = int(now().timestamp())

    timestamp+= 84600*0.1
    new_time = datetime.fromtimestamp(timestamp)
    new_time = make_aware(new_time)
    return new_time

