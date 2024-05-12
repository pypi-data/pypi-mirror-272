from datetime import datetime
from typing import Dict, Union

from pydantic import BaseModel, Field


def _get_duration(
    start: datetime,
    end: datetime,
    human_readable: bool = False,
) -> Union[float, str]:
    duration = end - start
    if not human_readable:
        return duration

    total_seconds = int(duration.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    human_readable_res = ""
    if minutes:
        human_readable_res += f"'{minutes}' minutes and "
    human_readable_res += f"{seconds} seconds"
    return human_readable_res


class TimeFrame(BaseModel):
    start_time: datetime = Field(datetime.now(), init=False)
    end_time: datetime = Field(None, init=False)

    def end_time_frame(self) -> datetime:
        self.end_time = datetime.now()
        return self.end_time

    def get_duration(self, human_readable: bool = False) -> Union[float, str]:
        return _get_duration(
            start=self.start_time,
            end=(self.end_time or self.end_time_frame()),
            human_readable=human_readable,
        )


class Timer(BaseModel):
    time_stamps: Dict[str, datetime] = {}
    time_frames: Dict[str, TimeFrame] = {}

    def create_new_time_stamp(self, name: str) -> datetime:
        new_timestamp = datetime.now()
        self.time_stamps[name] = new_timestamp
        return new_timestamp

    def create_new_time_frame(self, name: str) -> TimeFrame:
        new_time_frame = TimeFrame()
        self.time_frames[name] = new_time_frame
        return new_time_frame

    def get_timestamp(self, name: str) -> datetime:
        return self.time_stamps.get(name, self.create_new_time_stamp(name))

    def get_time_frame(self, name: str) -> TimeFrame:
        return self.time_frames.get(name, self.create_new_time_frame(name))

    def get_duration_between_timestamps(
        self,
        timestamp_a_name: str,
        timestamp_b_name: str,
        human_readable: bool = False,
    ) -> Union[float, str]:
        return _get_duration(
            start=self.time_stamps[timestamp_a_name],
            end=self.time_stamps[timestamp_b_name],
            human_readable=human_readable,
        )
