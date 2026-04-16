import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List
import random
from src.models.process import Process

class GanttChart:
    """
    A utility class for creating Gantt charts to visualize CPU scheduling.
    """

    def __init__(self, title: str = "CPU Scheduling Gantt Chart"):
        self.title = title
        self.fig, self.ax = plt.subplots(figsize=(12, 6))

    def plot_processes(self, processes: List[Process], colors: List[str] = None):
        """
        Plot the Gantt chart for the given processes.

        Args:
            processes: List of Process objects with execution history
            colors: Optional list of colors for each process
        """
        if colors is None:
            # Generate random hex colors for each process
            colors = generate_hex_colors(len(processes))

        # Collect all execution blocks
        all_blocks = []
        process_colors = {}

        # Sort processes by first execution time for better visualization
        sorted_processes = sorted(processes, key=lambda p: p.get_execution_history()[0].get_start_time() if p.get_execution_history() else float('inf'))

        for process_idx, process in enumerate(sorted_processes):
            if not process.get_execution_history():
                continue  # Skip processes that haven't executed

            process_name = process.name
            process_colors[process_name] = colors[process_idx % len(colors)]

            for execution in process.get_execution_history():
                all_blocks.append({
                    'process': process_name,
                    'start': execution.get_start_time(),
                    'end': execution.get_end_time(),
                    'duration': execution.get_duration(),
                    'y_pos': 0
                })

        # Sort execution blocks by start time
        all_blocks.sort(key=lambda block: block['start'])

        # Plot the execution blocks
        for block in all_blocks:
            color = process_colors[block['process']]
            rect = patches.Rectangle(
                (block['start'], block['y_pos'] - 0.2),
                block['duration'],
                0.4,
                linewidth=1,
                edgecolor='black',
                facecolor=color,
                alpha=0.7
            )
            self.ax.add_patch(rect)

            # Add process label in the center of the block
            center_x = block['start'] + block['duration'] / 2
            center_y = block['y_pos']
            self.ax.text(center_x, center_y, block['process'],
                        ha='center', va='center', fontsize=10, fontweight='bold')

        # Set up the plot
        max_time = max((block['end'] for block in all_blocks), default=10)
        self.ax.set_xlim(0, max_time)
        self.ax.set_ylim(-0.5, 0.5)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('CPU')
        self.ax.set_title(self.title)

        # Set y-ticks to show a single row
        self.ax.set_yticks([0])
        self.ax.set_yticklabels(['CPU'])

        # Add grid
        self.ax.grid(True, alpha=0.3)

        # Add time labels on x-axis
        self.ax.set_xticks(range(0, max_time + 1, 1))

    def save(self, filename: str = "gantt_chart.png", dpi: int = 300):
        """
        Save the Gantt chart to a file.

        Args:
            filename: Output filename (should end with .png, .jpg, .svg, etc.)
            dpi: Resolution for raster formats
        """
        self.fig.tight_layout()
        self.fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"Gantt chart saved as {filename}")

    def show(self):
        """
        Display the Gantt chart (only works in interactive environments).
        """
        plt.show()

def create_gantt_chart(processes: List[Process], title: str = "CPU Scheduling Gantt Chart",
                      save_path: str = None) -> GanttChart:
    """
    Convenience function to create and optionally save a Gantt chart.

    Args:
        processes: List of Process objects
        title: Chart title
        save_path: If provided, save the chart to this path

    Returns:
        GanttChart object
    """
    chart = GanttChart(title)
    chart.plot_processes(processes)

    if save_path:
        chart.save(save_path)

    return chart


def generate_hex_colors(count):
    colors = []
    for _ in range(count):
        color = f"#{random.randint(0, 0xFFFFFF):06x}"
        colors.append(color)
    return colors