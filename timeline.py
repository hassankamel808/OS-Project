class Timeline:
    def __init__(self):
        self.execution_timeline = []

    def add(self, time, process):
        pid = process.get_pid() if process else None
        self.execution_timeline.append({
            "time": time,
            "pid": pid
        })

    def get_timeline(self):
        return self.execution_timeline

    def print_timeline(self):
        print("\n--- Execution Timeline ---")
        for entry in self.execution_timeline:
            if entry["pid"] is not None:
                print(f"Time {entry['time']}: P{entry['pid']}")
            else:
                print(f"Time {entry['time']}: IDLE")
