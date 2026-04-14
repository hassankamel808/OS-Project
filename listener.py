import threading


class LiveProcessListener:
    def __init__(self, simulation):
        self.simulation = simulation
        self.running = False

    def start(self):
        self.running = True
        thread = threading.Thread(target=self._listen, daemon=True)
        thread.start()

    def stop(self):
        self.running = False

    def _listen(self):
        while self.running:
            try:
                user_input = input("Add process (pid name burst priority): ")
                if not user_input:
                    continue

                parts = user_input.split()
                if len(parts) != 4:
                    print("Invalid input format")
                    continue

                pid, name, burst, priority = parts

                process = self.simulation.add_live_process(
                    name=name,
                    burst_time=int(burst),
                    priority=int(priority),
                    pid=int(pid),
                )

                print(f"Added Process P{process.get_pid()}")

            except Exception as e:
                print("Error:", e)
