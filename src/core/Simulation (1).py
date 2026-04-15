import time
from src.models.process import Process
from src.core.scheduler import Scheduler
from src.core.analytics import Analytics 
import threading

class Simulation:
    def __init__(self, scheduler: Scheduler, delay: float = 1.0):
        self.scheduler = scheduler
        self.delay = delay
        self.running = False
        self.paused = False
        self.processes_timeline = []

    def add_process(self, process: Process):
        self.scheduler.add_process(process)

    def add_live_process(self, name: str, burst_time: int, priority: int, pid: int) -> Process:
        current_time = self.scheduler.get_current_time()
        process = Process(
            pid=pid,
            name=name,
            arrival_time=current_time,
            burst_time=burst_time,
            priority=priority,
        )
        self.add_process(process)
        return process

    def remove_process(self, pid: int):
        self.scheduler.remove_process(pid)

    def reset(self):
        self.scheduler.hard_reset()

    def is_running(self) -> bool:
        return self.running

    def start(self):
        self.running = True
        self.paused = False

    def is_paused(self) -> bool:
        return self.paused

    def set_paused(self, paused: bool):
        self.paused = paused

    def set_speed(self, speed_factor: int):
        if speed_factor <= 0:
            self.delay = 0.001 
        else:
            self.delay = 1.0 / speed_factor

    def _run_simulation(self, useDelay: bool = True):
        while (self.running) and (not self.scheduler.all_processes_completed()):
            current_process = self.scheduler.run_tick()

            pid = current_process.get_pid() if current_process else None
            self.processes_timeline.append({"time": self.scheduler.get_current_time(), "pid": pid})

            if useDelay:
                time.sleep(self.delay)
            
            yield current_process
            
        self.running = False
        return self.running

    def get_cpu_utilization(self) -> float:
        processes = self.scheduler.get_processes()
        total_time = self.scheduler.get_current_time()
        return Analytics.cpu_utilization(processes, total_time)

    def get_throughput(self) -> float:
        completed = self.scheduler.completed_processes
        total_time = self.scheduler.get_current_time()
        return Analytics.throughput(completed, total_time)

    def has_results(self) -> bool:
        return self.scheduler.all_processes_completed()