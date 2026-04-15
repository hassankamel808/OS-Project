class Analytics:
    @staticmethod
    def average_waiting_time(processes):
        if not processes:
            return 0.0
        return sum(p.get_waiting_time() for p in processes) / len(processes)

    @staticmethod
    def average_turnaround_time(processes):
        if not processes:
            return 0.0
        return sum(p.get_turnaround_time() for p in processes) / len(processes)

    @staticmethod
    def average_response_time(processes):
        responded = [p for p in processes if p.get_response_time() is not None]
        if not responded:
            return 0.0
        return sum(p.get_response_time() for p in responded) / len(responded)

    @staticmethod
    def cpu_utilization(processes, total_time):
        if total_time == 0:
            return 0.0
        busy_time = sum(p.burst_time for p in processes)
        return (busy_time / total_time) * 100

    @staticmethod
    def throughput(completed_processes, total_time):
        if total_time == 0:
            return 0.0
        return len(completed_processes) / total_time