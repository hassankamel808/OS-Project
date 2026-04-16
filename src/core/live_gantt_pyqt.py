import sys
import random

try:
    from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                                 QPushButton, QLabel)
    from PyQt6.QtCore import QTimer
    from matplotlib.backends.backend_qt6agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.patches as patches
    _GUI_AVAILABLE = True
except ModuleNotFoundError:
    QApplication = None
    QWidget = object
    QVBoxLayout = object
    QHBoxLayout = object
    QPushButton = object
    QLabel = object
    QTimer = object
    FigureCanvas = object
    Figure = object
    patches = None
    _GUI_AVAILABLE = False


class LiveGanttWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Gantt Chart - Matplotlib Method")
        self.setMinimumSize(800, 400)
        
        # Main Layout
        self.layout = QVBoxLayout(self)

        # 1. Setup Matplotlib Canvas
        self.fig = Figure(figsize=(10, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # 2. Setup Controls Layout
        self.controls_layout = QHBoxLayout()
        
        self.btn_toggle = QPushButton("Start Simulation")
        self.btn_toggle.clicked.connect(self.toggle_simulation)
        
        self.btn_add = QPushButton("Add Process to Queue")
        self.btn_add.clicked.connect(self.add_random_process)
        
        self.status_label = QLabel("Status: Paused | Time: 0s | Queue: 0")
        
        self.controls_layout.addWidget(self.btn_toggle)
        self.controls_layout.addWidget(self.btn_add)
        self.controls_layout.addStretch()
        self.controls_layout.addWidget(self.status_label)
        
        self.layout.addLayout(self.controls_layout)

        # 3. Simulation State Variables
        self.current_time = 0
        self.is_running = False
        self.process_queue = []  # Pending processes: {'name', 'burst', 'color'}
        self.execution_blocks = []  # History for drawing
        self.current_active_block = None

        # 4. Setup QTimer (Ticks every 1000 ms = 1 second)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

        # Draw the initial empty chart
        self.update_plot()

    def toggle_simulation(self):
        if self.is_running:
            self.timer.stop()
            self.btn_toggle.setText("Resume Simulation")
            self.is_running = False
        else:
            self.timer.start(1000)  # 1000 milliseconds = 1 second
            self.btn_toggle.setText("Pause Simulation")
            self.is_running = True
        self.update_status()

    def add_random_process(self):
        """Simulates a user adding a process via your GUI inputs."""
        pid = len(self.process_queue) + len(self.execution_blocks) + 1
        burst_time = random.randint(3, 8)
        color = f"#{random.randint(0, 0xFFFFFF):06x}"
        
        self.process_queue.append({
            'name': f"P{pid}",
            'burst': burst_time,
            'color': color
        })
        self.update_status()

    def tick(self):
        """The core engine loop: Called every 1 second by the QTimer."""
        # 1. Check if we need to load a new process from the queue
        if self.current_active_block is None and self.process_queue:
            next_process = self.process_queue.pop(0)
            self.current_active_block = {
                'process': next_process['name'],
                'start': self.current_time,
                'duration': 0,
                'remaining': next_process['burst'],
                'color': next_process['color']
            }
            self.execution_blocks.append(self.current_active_block)

        # 2. Advance time and process duration
        if self.current_active_block:
            self.current_active_block['duration'] += 1
            self.current_active_block['remaining'] -= 1
            
            # If process finished, clear the active block
            if self.current_active_block['remaining'] <= 0:
                self.current_active_block = None

        self.current_time += 1
        
        # 3. Redraw UI
        self.update_plot()
        self.update_status()

    def update_plot(self):
        """Redraws the Matplotlib canvas with the current data."""
        self.ax.clear()  # Clear previous frame

        # Draw all blocks
        for block in self.execution_blocks:
            rect = patches.Rectangle(
                (block['start'], -0.2),  # (x, y)
                block['duration'],       # width
                0.4,                     # height
                linewidth=1,
                edgecolor='black',
                facecolor=block['color'],
                alpha=0.8
            )
            self.ax.add_patch(rect)

            # Add process text if the block is wide enough to fit it
            if block['duration'] > 0:
                center_x = block['start'] + (block['duration'] / 2)
                self.ax.text(center_x, 0, block['process'], 
                             ha='center', va='center', color='white', fontweight='bold')

        # Create a sliding window effect on the X-axis (shows last 15 seconds)
        max_x = max(15, self.current_time + 2)
        min_x = max(0, max_x - 15)
        
        self.ax.set_xlim(min_x, max_x)
        self.ax.set_ylim(-0.5, 0.5)
        self.ax.set_yticks([0])
        self.ax.set_yticklabels(['CPU'])
        self.ax.set_xlabel('Time (Seconds)')
        self.ax.set_title('Live CPU Scheduling Gantt Chart')
        self.ax.grid(True, alpha=0.3)
        
        # Ensure x-axis ticks are integers
        self.ax.set_xticks(range(int(min_x), int(max_x) + 1))

        self.canvas.draw()

    def update_status(self):
        state = "Running" if self.is_running else "Paused"
        queue_size = len(self.process_queue)
        self.status_label.setText(f"Status: {state} | Time: {self.current_time}s | In Queue: {queue_size}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LiveGanttWidget()
    window.show()
    sys.exit(app.exec())
