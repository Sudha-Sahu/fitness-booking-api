from datetime import datetime
import pytz

def ist_to_utc(dt_str):
    ist = pytz.timezone('Asia/Kolkata')
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    localized = ist.localize(dt)
    return localized.astimezone(pytz.utc)

def utc_to_timezone(dt, tz_str):
    return dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(tz_str))
