import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def plot_feasible_region_cloud(a_lp=None, b_lp=None, a_ilp=None, b_ilp=None):
    """2D feasible region for the cloud server problem."""
    fig, ax = plt.subplots(figsize=(8, 7))

    a_vals = np.linspace(0, 12, 400)

    # Constraint boundaries
    b_cpu = (30 - 4 * a_vals) / 8      # 4a + 8b >= 30
    b_ram = (90 - 8 * a_vals) / 32     # 8a + 32b >= 90

    ax.plot(a_vals, b_cpu, label="4a + 8b = 30 (vCPU)", color="steelblue", lw=2)
    ax.plot(a_vals, b_ram, label="8a + 32b = 90 (RAM)", color="darkorange", lw=2)

    # Shade feasible region
    b_feasible = np.maximum(np.maximum(b_cpu, b_ram), 0)
    ax.fill_between(a_vals, b_feasible, 10, alpha=0.15, color="green",
                    label="Feasible region")

    # Integer points in feasible region
    int_points = [
        (a, b) for a in range(13) for b in range(11)
        if 4 * a + 8 * b >= 30 and 8 * a + 32 * b >= 90
    ]
    if int_points:
        xs, ys = zip(*int_points)
        ax.scatter(xs, ys, s=40, color="gray", zorder=3, label="Integer points")

    # LP optimum
    if a_lp is not None and b_lp is not None:
        ax.scatter([a_lp], [b_lp], s=150, color="steelblue", zorder=5,
                   label=f"LP opt ({a_lp:.2f}, {b_lp:.2f})")

    # ILP optimum
    if a_ilp is not None and b_ilp is not None:
        ax.scatter([a_ilp], [b_ilp], s=150, color="red", marker="*", zorder=5,
                   label=f"ILP opt ({a_ilp}, {b_ilp})")

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9)
    ax.set_xlabel("a (Tip-A sunucu sayısı)", fontsize=12)
    ax.set_ylabel("b (Tip-B sunucu sayısı)", fontsize=12)
    ax.set_title("Bulut Sunucusu — Feasible Region", fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    return fig


def plot_exam_schedule(schedule: dict, course_colors: dict = None):
    """Bar chart showing which courses are in which slots."""
    if not schedule:
        return None

    slots = sorted(set(schedule.values()))
    slot_courses = {s: [] for s in slots}
    for course, slot in schedule.items():
        slot_courses[slot].append(course)

    fig, ax = plt.subplots(figsize=(max(6, len(slots) * 1.2), 4))
    colors = plt.cm.Set2.colors

    for i, slot in enumerate(slots):
        for j, course in enumerate(slot_courses[slot]):
            color = (course_colors or {}).get(course, colors[i % len(colors)])
            ax.bar(i, 1, bottom=j, color=color, edgecolor="white", linewidth=0.8)
            ax.text(i, j + 0.5, course, ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white")

    ax.set_xticks(range(len(slots)))
    ax.set_xticklabels([f"Slot {s}" for s in slots], fontsize=10)
    ax.set_ylabel("Dersler")
    ax.set_title("Sınav Takvimi", fontsize=12)
    ax.set_ylim(0, max(len(v) for v in slot_courses.values()) + 0.5)
    plt.tight_layout()
    return fig


def plot_gantt(assignment: dict, proc_times: dict, num_machines: int):
    """Simple Gantt chart for task assignment."""
    fig, ax = plt.subplots(figsize=(10, 3))
    colors = plt.cm.tab10.colors

    machine_time = {m: 0 for m in range(num_machines)}
    for task, machine in sorted(assignment.items()):
        duration = proc_times[task][machine]
        start = machine_time[machine]
        ax.barh(machine, duration, left=start,
                color=colors[task % len(colors)], edgecolor="white")
        ax.text(start + duration / 2, machine, f"J{task}",
                ha="center", va="center", fontsize=8, color="white", fontweight="bold")
        machine_time[machine] += duration

    ax.set_yticks(range(num_machines))
    ax.set_yticklabels([f"İşlemci {m}" for m in range(num_machines)])
    ax.set_xlabel("Zaman")
    ax.set_title("Görev Atama — Gantt Grafiği")
    plt.tight_layout()
    return fig
