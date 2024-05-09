import datetime

import datetime

class FloorInfo:
    def __init__(self,
                 floor_no: str,
                 house_no: str,
                 floor_name: str,
                 seq: int,
                 create_time: str
                 ):
        self.floor_no = floor_no
        self.house_no = house_no
        self.floor_name = floor_name
        self.seq = seq
        self.create_time = self._parse_datetime(create_time)

    @staticmethod
    def _parse_datetime(datetime_str: str) -> datetime.datetime:
        return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


