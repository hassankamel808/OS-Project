from src.core.scheduler import Scheduler
from src.models.process import Process
from typing import Optional

class SJFNonPreemptiveScheduler(Scheduler):
    def __init__(self):
        super().__init__("Shortest Job First (Non-Preemptive)")
        self.current_running_process = None

    def get_next_process(self, current_time) -> Optional[Process]:
        if self.current_running_process and not self.current_running_process.is_completed():
            return self.current_running_process

        ready_processes = self.get_arrived_processes(current_time)

        if not ready_processes:
            self.current_running_process = None
            return None

        self.current_running_process = min(
            ready_processes,
            key=lambda p: (p.get_burst_time(), p.get_arrival_time(), p.get_pid())
        )

        return self.current_running_process