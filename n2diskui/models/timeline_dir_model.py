
import os
from flask import current_app as app
from typing import Tuple

class TimelineDir:
    def __init__(self, timeline_dir_path: str) -> None:
        """
        Constructor for TimelineDir Object

        Args:
            timeline_dir_path (str): The path to the n2disk timeline directory.

        Raises:
            FileNotFoundError: If the path to the timeline directory is not found. 
        """
        self.timeline_dir_path = timeline_dir_path
        if not os.path.isfile(self.timeline_dir_path):
            raise FileNotFoundError()
        self.date_range = self.generate_date_range_by_sensing_timeline_dir()
    
    def generate_date_range_by_sensing_timeline_dir(self) -> Tuple[str, str]:
        pass
