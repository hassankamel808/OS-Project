from src.core.scheduler import Scheduler
from src.models.process import Process
from typing import Optional


class PriorityPreemptiveScheduler(Scheduler):
    """
    Priority Preemptive scheduling algorithm.
    At any time, the process with the highest priority (lowest priority number) gets the CPU.
    If a new process arrives with higher priority, it preempts the current process.
    """

    def __init__(self):
        super().__init__("Priority (Preemptive)")

    def get_next_process(self, current_time) -> Optional[Process]:
        """
        Get the next process to execute based on Priority Preemptive scheduling.
        Always pick the ready process with the smallest priority number (highest priority).
        """
        # Get all processes that have arrived and aren't completed
        ready_processes = self.get_arrived_processes(current_time)

        if not ready_processes:
            self.current_process = None
            return None

        # Sort by priority (lower number = higher priority)
        # Tie-break by arrival time, then PID
        next_process = sorted(
            ready_processes,
            key=lambda p: (p.get_priority(), p.get_arrival_time(), p.get_pid())
        )[0]

        # Update current process (preemption happens automatically)
        self.current_process = next_process
        return self.current_process