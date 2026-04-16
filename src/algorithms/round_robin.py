from src.core.scheduler import Scheduler
from src.models.process import Process
from typing import Optional
from collections import deque


class RoundRobinScheduler(Scheduler):
    """
    Round Robin scheduling algorithm.
    Each process is given a fixed time slice (quantum) to execute.
    Processes are executed in a circular queue.
    """

    def __init__(self, time_quantum: int = 2):
        """
        Initialize a new RoundRobinScheduler instance.

        Args:
            time_quantum (int): The time quantum for each process (default: 2)
        """
        super().__init__("Round Robin")
        self.time_quantum = time_quantum
        self.ready_queue = deque()
        self.quantum_timer = 0

    def reset(self):
        """Reset the scheduler state for a new simulation."""
        super().reset()
        self.ready_queue = deque()
        self.quantum_timer = 0

    def get_next_process(self, current_time) -> Optional[Process]:
        """
        Get the next process to execute based on Round Robin scheduling.
        """
        # 1. Add NEW arrivals to the queue first
        for process in self.get_arrived_processes(current_time):
            if (process not in self.ready_queue) and (process != self.current_process):
                if not process.is_completed():
                    self.ready_queue.append(process)

        # 2. Handle the current process (Preemption or Completion)
        if self.current_process:
            if self.quantum_timer >= self.time_quantum or self.current_process.is_completed():
                if not self.current_process.is_completed():
                    # NEW arrivals are already in the queue, so this goes BEHIND them
                    self.ready_queue.append(self.current_process)
                
                self.current_process = None
                self.quantum_timer = 0

        # 3. Pick the next one
        if not self.current_process and self.ready_queue:
            self.current_process = self.ready_queue.popleft()
            self.quantum_timer = 0

        return self.current_process

    def run_tick(self) -> Optional[Process]:
        """
        Override run_tick to track quantum usage properly.
        """
        # First, get/update the next process to run
        next_process = self.get_next_process(self.current_time)
        
        time_used = self.time_slice
        
        if next_process:
            self.current_process = next_process
            # Execute for one time unit
            time_used = self.current_process.execute(self.current_time, self.time_slice)
            self.quantum_timer += time_used

            if self.current_process.is_completed():
                self.completed_processes.append(self.current_process)
        else:
            self.current_process = None

        self.current_time += time_used
        return self.current_process
