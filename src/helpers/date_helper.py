from datetime import datetime

class DateHelper:
    @staticmethod
    def datetime_to_timestamp(date_str, time_str):
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        return int(dt.timestamp())

    @staticmethod
    def timestamp_to_datetime(timestamp):
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    
    @staticmethod
    def get_date_from_datetime(datetime):
        return datetime.strftime(datetime, "%Y-%m-%d")
