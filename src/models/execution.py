class Execution:
    """
    Represents a single continuous block of execution time for a process.
    Used to track the exact start and end times of execution slices for
    accurate Gantt chart rendering and historical tracking.
    """
    def __init__(self, start_time: int, end_time: int):
        self.start_time = start_time
        self.end_time = end_time

    def get_start_time(self) -> int:
        return self.start_time

    def get_end_time(self) -> int:
        return self.end_time

    def get_duration(self) -> int:
        return self.end_time - self.start_time

    def __str__(self) -> str:
        return f"[{self.start_time} - {self.end_time}]"

    def __repr__(self) -> str:
        return self.__str__()
