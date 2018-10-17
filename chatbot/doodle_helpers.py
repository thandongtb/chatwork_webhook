import requests
import json
import datetime

def get_schedule():
    uri = "https://doodle.com/api/v2.0/polls/wnfnss4aim4ps5se" 
    req = requests.get(uri)
    result = json.loads(req.text)
    return result

def get_calendar(weekday = 0, weekday_vietnamese_name = "thứ hai"):
    schedule = get_schedule()

    if weekday == 5 or weekday == 6:
        message = "(lay4) Cuối tuần làm gì có ai đi làm nữa hả anh. Đưa gấu đi chơi thôi (yaoming)"
    elif weekday > 6 or weekday < 0:
        message = "Hôm đó chưa có lịch đâu anh ơi. Gì mà hăng hái thế (yaoming)"
    else:
        morning = [s['name'] for s in schedule['participants'] if s['preferences'][weekday * 2] == 1]
        afternoon = [s['name'] for s in schedule['participants'] if s['preferences'][weekday * 2 + 1] == 1]

        message = "Lịch làm việc của team FML {} ạ\nBuổi sáng:\n[info]{}[/info]\nBuổi chiều:\n[info]{}[/info]\n(quaylen)".format(weekday_vietnamese_name, " ,  ".join(morning), " ,  ".join(afternoon))

    return message

def get_weekday(weekday_name):
    today_weekday = datetime.datetime.today().weekday()
    weekday_map = {
        "monday" : 0,
        "tuesday" : 1,
        "wednesday" : 2,
        "thursday" : 3,
        "friday" : 4,
        "saturday" : 5,
        "sunday" : 6,
        "today" : today_weekday,
        "yesterday" : today_weekday - 1,
        "tomorrow" : today_weekday + 1,
        "next_tomorrow" : today_weekday + 2,
    }

    weekday_vietnamese_map = {
        "monday": "thứ hai",
        "tuesday": "thứ ba",
        "wednesday": "thứ tư",
        "thursday": "thứ năm",
        "friday": "thứ sáu",
        "saturday": "thứ bảy",
        "sunday": "chủ nhật",
        "today": "hôm nay",
        "yesterday": "hôm qua",
        "tomorrow": "ngày mai",
        "next_tomorrow": "ngày kia",
    }
    return weekday_map[weekday_name], weekday_vietnamese_map[weekday_name]

def get_weekday_calendar(weekday_name):
    weekday, weekday_vietnamese_name = get_weekday(weekday_name=weekday_name)
    message = get_calendar(weekday, weekday_vietnamese_name)
    return message


