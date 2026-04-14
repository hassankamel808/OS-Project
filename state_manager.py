class StateManager:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    def get_remaining_times(self):
        data = []
        for p in self.scheduler.get_processes():
            try:
                remaining = p.get_remaining_time()
            except:
                remaining = None
            data.append({
                "pid": p.get_pid(),
                "remaining": remaining
            })
        return data

    def print_remaining_times(self):
        print("\n--- Remaining Burst Time ---")
        for p in self.scheduler.get_processes():
            try:
                remaining = p.get_remaining_time()
            except:
                remaining = "N/A"
            print(f"P{p.get_pid()} -> {remaining}")
