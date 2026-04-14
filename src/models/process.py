from src.models.execution import Execution

class Process:
    def __init__(self, pid: int, arrival_time: int, burst_time: int, priority: int = 0, name: str = ""):
        self.pid = pid
        self.name = name if name else f"P{pid}"
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        
        # Simulation State
        self.remaining_burst_time = burst_time
        self.has_started = False
        
        # Metrics
        self.start_time = None
        self.completion_time = None
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = None
        
        # UI/Gantt Chart Tracking
        self.execution_history = []

    def execute(self, current_time: int, time_slice: int = 1) -> int:
        # Record start metrics on the very first execution
        if not self.has_started:
            self.start_time = current_time
            self.response_time = current_time - self.arrival_time
            self.has_started = True

        actual_time_used = min(self.remaining_burst_time, time_slice)
        block_end_time = current_time + actual_time_used
        
        # Record this specific tick for the Gantt Chart
        self.execution_history.append(Execution(current_time, block_end_time))

        self.remaining_burst_time -= actual_time_used

        # Lock in final metrics if process finishes on this tick
        if self.is_completed():
            self.completion_time = block_end_time
            self.turnaround_time = self.completion_time - self.arrival_time
            self.waiting_time = self.turnaround_time - self.burst_time

        return actual_time_used

    def is_completed(self) -> bool:
        return self.remaining_burst_time == 0
        
    def reset(self):
        """Resets the process state for a new simulation run."""
        self.remaining_burst_time = self.burst_time
        self.has_started = False
        self.start_time = None
        self.completion_time = None
        self.turnaround_time = 0
        self.waiting_time = 0
        self.response_time = None
        self.execution_history = []

    # Getters required by the Scheduler and UI
    def get_pid(self): return self.pid
    def get_arrival_time(self): return self.arrival_time
    def get_burst_time(self): return self.remaining_burst_time 
    def get_priority(self): return self.priority
    def get_waiting_time(self): return self.waiting_time
    def get_turnaround_time(self): return self.turnaround_time
    def get_response_time(self): return self.response_time
    def get_execution_history(self): return self.execution_history