from src.core.scheduler import Scheduler
from src.models.process import Process
from typing import Optional, Union
from collections import deque

class RoundRobinScheduler(Scheduler):
    """
    Round Robin scheduling algorithm.
    Each process is given a fixed time slice (quantum) to execute.
    Processes are executed in a circular queue.
    """

    def __init__(self, time_quantum: Union[int, float] = 2):
        if not isinstance(time_quantum, (int, float)):
            raise TypeError(f"Time quantum must be a number (int or float), got {type(time_quantum).__name__}")
        if time_quantum <= 0:
            raise ValueError(f"Time quantum must be positive (> 0), got {time_quantum}")

        super().__init__("Round Robin")
        self.time_quantum = float(time_quantum)
        self.ready_queue = deque()
        self.quantum_timer = 0.0

    def reset(self):
        """Reset the scheduler state for a new simulation."""
        super().reset()
        self.ready_queue = deque()
        self.quantum_timer = 0.0

    def get_next_process(self, current_time) -> Optional[Process]:
        """
        Get the next process to execute based on Round Robin scheduling.
        Standard OS Tie-Breaker: New arrivals enter the queue BEFORE preempted processes.
        """
        
        # STEP 1: Add NEW arrivals to the queue first
        for process in self.get_arrived_processes(current_time):
            if (process not in self.ready_queue) and (process != self.current_process):
                if not process.is_completed():
                    self.ready_queue.append(process)

        # STEP 2: Handle the current process (Preemption or Completion)
        if self.current_process:
            quantum_expired = self.quantum_timer >= self.time_quantum
            process_done = self.current_process.is_completed()

            if quantum_expired or process_done:
                if not process_done:
                    # NEW arrivals are already in the queue, so this goes BEHIND them
                    self.ready_queue.append(self.current_process)
                
                self.current_process = None
                self.quantum_timer = 0.0

        # STEP 3: Pick the next process from the front of the queue
        if not self.current_process and self.ready_queue:
            self.current_process = self.ready_queue.popleft()
            self.quantum_timer = 0.0

        return self.current_process

    def run_tick(self) -> Optional[Process]:
        """Override run_tick to track quantum usage properly."""
        next_process = self.get_next_process(self.current_time)
        time_used = self.time_slice

        if next_process:
            self.current_process = next_process
            time_used = self.current_process.execute(self.current_time, self.time_slice)
            self.quantum_timer += float(time_used)

            if self.current_process.is_completed():
                self.completed_processes.append(self.current_process)
        else:
            self.current_process = None

        self.current_time += time_used
        return self.current_process

    def get_remaining_quantum_time(self) -> float:
        """Get the remaining time in the current quantum. Useful for GUI display."""
        return max(0.0, self.time_quantum - self.quantum_timer)
