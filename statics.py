import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ChartWindow:
    def __init__(self, comparison_results, selected_metrics):
        self.chart_window = tk.Toplevel()
        self.chart_window.title("Algorithm Comparison Charts")
        self.chart_window.geometry("1000x800")
        self.chart_window.configure(bg="#f0f4f8")

        self.comparison_results = comparison_results
        self.selected_metrics = selected_metrics
        self.valid_metrics = {"Steps", "Cost", "Time", "Space"}

        if not self.validate_inputs():
            return

        self.plot_comparison_chart()

    def validate_inputs(self):
        """Validate comparison_results and selected_metrics."""
        if not self.comparison_results:
            messagebox.showwarning("Invalid Input", "No comparison results provided.")
            self.chart_window.destroy()
            return False
        if not self.selected_metrics:
            messagebox.showwarning("Invalid Input", "No metrics selected.")
            self.chart_window.destroy()
            return False
        for metric in self.selected_metrics:
            if metric not in self.valid_metrics:
                messagebox.showwarning("Invalid Metric", f"Metric '{metric}' is not valid.")
                self.chart_window.destroy()
                return False
        return True

    def plot_comparison_chart(self, normalize=False):
        algorithms = [result["algorithm"] for result in self.comparison_results]
        metrics_data = {
            "Cost": [result["cost"] for result in self.comparison_results],
            "Time": [result["time"] for result in self.comparison_results],
            "Space": [result["space"] for result in self.comparison_results]
        }

        # Chỉ lấy các metric cần thiết
        selected_metrics = ["Cost", "Time", "Space"]
        selected_data = {metric: metrics_data[metric] for metric in selected_metrics}

        # Tính giá trị tối đa cho yticks
        max_value = max(max(values) for values in selected_data.values()) if selected_data.values() else 1.0
        if max_value == 0:
            max_value = 1.0  # Tránh chia cho 0
        tick_steps = max_value / 4
        yticks = [i * tick_steps for i in range(5)]

        labels = selected_metrics
        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]

        # Tính toán lưới subplot
        num_algos = len(algorithms)
        cols = min(num_algos, 2)
        rows = (num_algos + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(8 * cols, 6 * rows), subplot_kw=dict(polar=True))

        if num_algos == 1:
            axes = np.array([[axes]])
        elif cols == 1:
            axes = axes.reshape(-1, 1)
        else:
            axes = axes.reshape(rows, cols)

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

        for i, algo in enumerate(algorithms):
            row = i // cols
            col = i % cols
            ax = axes[row, col]

            values = [selected_data[metric][i] for metric in labels]
            values += values[:1]
            ax.plot(angles, values, label=algo, linewidth=2.5, color=colors[i % len(colors)])
            ax.fill(angles, values, color=colors[i % len(colors)], alpha=0.2)

            # Thêm giá trị tại các điểm
            for j, (angle, value) in enumerate(zip(angles[:-1], values[:-1])):
                display_value = f"{value:.4f}" if labels[j] == "Time" else f"{int(value)}"
                ax.text(angle, value + max_value * 0.05, display_value, ha='center', va='bottom', fontsize=9, color=colors[i % len(colors)])

            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels, fontsize=10, weight='bold')
            ax.set_yticks(yticks)
            ax.set_yticklabels(
                [f"{tick:.1f}" if tick < 1 else f"{int(tick)}" for tick in yticks],
                color='#333333',
                fontsize=10,
                fontweight='bold',
                alpha=0.8
            )
            ax.set_rlabel_position(30)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_title(algo, fontsize=12, pad=20, weight='bold')
            ax.set_ylim(0, max_value * 1.1)
            ax.text(-0.3, max_value * 0.5, algo, fontsize=13, fontweight='bold', color=colors[i % len(colors)], ha='right', va='center', rotation=90, transform=ax.transAxes)

        for i in range(len(algorithms), rows * cols):
            row = i // cols
            col = i % cols
            axes[row, col].set_visible(False)

        fig.suptitle("Radar Charts - Algorithm Comparison (Cost, Time, Space)", fontsize=16, y=1.05, weight='bold')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)