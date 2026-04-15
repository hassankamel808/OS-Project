from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.process import Process
from src.core.analytics import Analytics 

class Scheduler(ABC):
    """Abstract base class for all CPU scheduling algorithms."""

    def __init__(self, name):
        self.name = name
        self.time_slice = 1  
        self.processes: list[Process] = list()
        self.current_time = 0
        self.current_process: Optional[Process] = None
        self.completed_processes: list[Process] = list()

    def add_process(self, process: Process) -> None:
        self.processes.append(process)

    def add_processes(self, processes: list[Process]) -> None:
        self.processes.extend(processes)

    def get_processes(self) -> list[Process]:
        return self.processes

    def reset(self):
        self.current_time = 0
        self.current_process = None
        self.completed_processes = list()

    def hard_reset(self):
        self.reset()
        for process in self.processes:
            process.reset()

    def get_current_time(self) -> int:
        return self.current_time

    def all_processes_completed(self) -> bool:
        return all(process.is_completed() for process in self.processes)

    def get_arrived_processes(self, current_time) -> List[Process]:
        return [
            p for p in self.processes
            if (p.get_arrival_time() <= current_time) and (not p.is_completed())
        ]

    def get_average_waiting_time(self):
        return Analytics.average_waiting_time(self.processes)

    def get_average_turnaround_time(self):
        return Analytics.average_turnaround_time(self.processes)

    def calculate_metrics(self):
        return (self.get_average_waiting_time(), self.get_average_turnaround_time())

    def get_average_response_time(self):
        return Analytics.average_response_time(self.processes)

    def find_proccess_by_pid(self, pid: int) -> Optional[Process]:
        for process in self.processes:
            if process.get_pid() == pid:
                return process
        return None

    def remove_process(self, pid: int) -> None:
        process = self.find_proccess_by_pid(pid)
        if process in self.processes:
            self.processes.remove(process)
            if process in self.completed_processes:
                self.completed_processes.remove(process)

    @abstractmethod
    def get_next_process(self, current_time) -> Optional[Process]:
        pass

    def run_tick(self) -> Process:
        next_process = self.get_next_process(self.current_time)
        time_used = self.time_slice
        
        if next_process:
            self.current_process = next_process
            time_used = self.current_process.execute(self.current_time, self.time_slice)

            if self.current_process.is_completed():
                self.completed_processes.append(self.current_process)
        else:
            self.current_process = None

        self.current_time += time_used
        return self.current_process