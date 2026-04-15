from src.core.scheduler import Scheduler
from src.models.process import Process
from typing import Optional

class SJFPreemptiveScheduler(Scheduler):
    def __init__(self):
        super().__init__("Shortest Job First (Preemptive)")

    def get_next_process(self, current_time) -> Optional[Process]:
        ready_processes = self.get_arrived_processes(current_time)

        if not ready_processes:
            return None

        return min(
            ready_processes,
            key=lambda p: (p.get_burst_time(), p.get_arrival_time(), p.get_pid())
        )