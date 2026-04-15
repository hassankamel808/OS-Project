from src.core.scheduler import Scheduler
from src.models.process import Process
from typing import Optional


class PriorityNonPreemptiveScheduler(Scheduler):
    """
    Priority Non-Preemptive scheduling algorithm.
    Processes are executed based on priority (lower value = higher priority).
    Once a process starts executing, it runs to completion.
    """

    def __init__(self):
        super().__init__("Priority (Non-Preemptive)")

    def get_next_process(self, current_time) -> Optional[Process]:
        """
        Get the next process to execute based on Priority Non-Preemptive scheduling.
        """
        # Continue running current process if it exists and isn't complete
        if self.current_process and not self.current_process.is_completed():
            return self.current_process

        # Get all processes that have arrived and haven't completed
        ready_processes = self.get_arrived_processes(current_time)

        if not ready_processes:
            self.current_process = None
            return None

        # Select process with highest priority (lowest number)
        # Tie-break by arrival time, then PID
        self.current_process = min(
            ready_processes,
            key=lambda p: (p.get_priority(), p.get_arrival_time(), p.get_pid()),
        )

        return self.current_process