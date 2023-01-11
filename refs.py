from datetime import datetime, timedelta

PRODUCTION_ITEMS=["","Wood","Steel","Plastic","Seeds","Sand","Ore"] # list of producable materials


def time_in_future(mins) -> float:
    return (datetime.now() + timedelta(minutes=mins)).timestamp() # given x minutes in future, return epoch time for that future time
def rem_num(string) -> str:
    return ''.join(i for i in string if not i.isdigit())

