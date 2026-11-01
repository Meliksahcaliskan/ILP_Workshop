"""
Shared visualization helpers for ILP Workshop notebooks.
All function/parameter names are in English; plot titles and axis labels are in Turkish.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from IPython.display import display, HTML

# ---------------------------------------------------------------------------
# Color-blind-friendly palette (Wong 2011, Nature Methods)
# ---------------------------------------------------------------------------
PALETTE = {
    "blue":     "#0072B2",
    "orange":   "#E69F00",
    "green":    "#009E73",
    "sky":      "#56B4E9",
    "yellow":   "#F0E442",
    "vermil":   "#D55E00",
    "purple":   "#CC79A7",
    "black":    "#000000",
    "gray":     "#999999",
    "red":      "#D62728",
    "light":    "#F7F7F7",
}

COURSE_COLORS = {
    "CSE101": PALETTE["blue"],
    "CSE102": PALETTE["sky"],
    "CSE201": PALETTE["orange"],
    "CSE202": PALETTE["yellow"],
    "CSE301": PALETTE["vermil"],
    "CSE302": PALETTE["purple"],
    "MATH101": PALETTE["green"],
    "MATH201": PALETTE["black"],
    "EE101":  "#8C564B",
    "EE201":  "#17BECF",
}

COURSE_GROUP = {
    "CSE101": "1. Sınıf", "CSE102": "1. Sınıf",
    "MATH101": "1. Sınıf", "EE101":  "1. Sınıf",
    "CSE201": "2. Sınıf", "CSE202": "2. Sınıf",
    "MATH201": "2. Sınıf", "EE201":  "2. Sınıf",
    "CSE301": "3. Sınıf", "CSE302": "3. Sınıf",
}

GROUP_COLOR = {
    "1. Sınıf": PALETTE["blue"],
    "2. Sınıf": PALETTE["orange"],
    "3. Sınıf": PALETTE["green"],
}

# ---------------------------------------------------------------------------
# Utility: solver status box
# ---------------------------------------------------------------------------

def show_status(prob):
    """Display a colored HTML box with the solver status."""
    import pulp
    status = pulp.LpStatus[prob.status]
    colors = {
        "Optimal":    ("#d4edda", "#155724"),
        "Infeasible": ("#f8d7da", "#721c24"),
        "Unbounded":  ("#fff3cd", "#856404"),
    }
    bg, fg = colors.get(status, ("#e2e3e5", "#383d41"))
    obj = pulp.value(prob.objective)
    obj_str = f" — Amaç: {obj:.4g}" if obj is not None and status == "Optimal" else ""
    html = (
        f'<div style="border-radius:6px;padding:8px 14px;background:{bg};color:{fg};'
        f'font-weight:bold;display:inline-block;font-size:14px;">'
        f'Durum: {status}{obj_str}</div>'
    )
    display(HTML(html))


# ---------------------------------------------------------------------------
# 01 — Feasible region (cloud server)
# ---------------------------------------------------------------------------

def plot_feasible_region_cloud(a_lp=None, b_lp=None, a_ilp=None, b_ilp=None,
                                infeasible_points=None):
    """
    2D feasible region for the cloud server problem.
    infeasible_points: list of (a, b) tuples to mark with red X.
    """
    fig, ax = plt.subplots(figsize=(8, 7))
    a_vals = np.linspace(0, 12, 400)

    b_cpu = (30 - 4 * a_vals) / 8
    b_ram = (90 - 8 * a_vals) / 32

    ax.plot(a_vals, b_cpu, color=PALETTE["blue"], lw=2,
            label="4a + 8b = 30 (vCPU kısıtı)")
    ax.plot(a_vals, b_ram, color=PALETTE["orange"], lw=2,
            label="8a + 32b = 90 (RAM kısıtı)")

    b_feasible = np.maximum(np.maximum(b_cpu, b_ram), 0)
    ax.fill_between(a_vals, b_feasible, 10, alpha=0.12, color=PALETTE["green"],
                    label="Feasible bölge")

    int_pts = [(a, b) for a in range(13) for b in range(10)
               if 4*a + 8*b >= 30 and 8*a + 32*b >= 90]
    if int_pts:
        xs, ys = zip(*int_pts)
        ax.scatter(xs, ys, s=35, color=PALETTE["gray"], zorder=3, label="Tam sayı noktalar")

    if a_lp is not None and b_lp is not None:
        ax.scatter([a_lp], [b_lp], s=160, color=PALETTE["blue"], zorder=5,
                   label=f"LP opt ({a_lp:.2f}, {b_lp:.2f})")

    if a_ilp is not None and b_ilp is not None:
        ax.scatter([a_ilp], [b_ilp], s=200, color=PALETTE["vermil"],
                   marker="*", zorder=5, label=f"ILP opt ({a_ilp}, {b_ilp})")

    if infeasible_points:
        for (pa, pb) in infeasible_points:
            ax.scatter([pa], [pb], s=200, color=PALETTE["red"], marker="X", zorder=6,
                       label=f"Geçersiz yuvarlama ({pa}, {pb})")

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9)
    ax.set_xlabel("a (Tip-A sunucu sayısı)", fontsize=12)
    ax.set_ylabel("b (Tip-B sunucu sayısı)", fontsize=12)
    ax.set_title("Bulut Sunucusu — Feasible Bölge", fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 02 — Conflict heatmap (course × course)
# ---------------------------------------------------------------------------

def plot_conflict_heatmap(courses, student_enrollments):
    """Ders × ders matris — hücrede ortak öğrenci sayısı."""
    n = len(courses)
    idx = {c: i for i, c in enumerate(courses)}
    mat = np.zeros((n, n), dtype=int)

    for enr in student_enrollments:
        for i, c1 in enumerate(enr):
            for c2 in enr[i+1:]:
                if c1 in idx and c2 in idx:
                    r, c = idx[c1], idx[c2]
                    mat[r, c] += 1
                    mat[c, r] += 1

    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(mat, cmap="Blues", vmin=0)
    plt.colorbar(im, ax=ax, label="Ortak öğrenci sayısı")

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(courses, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(courses, fontsize=9)

    for i in range(n):
        for j in range(n):
            if mat[i, j] > 0:
                clr = "white" if mat[i, j] > mat.max() * 0.6 else "black"
                ax.text(j, i, str(mat[i, j]), ha="center", va="center",
                        fontsize=8, color=clr)

    ax.set_title("Çakışma Isı Haritası — Ortak Öğrenci Sayısı", fontsize=12)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 02 — Calendar table
# ---------------------------------------------------------------------------

def plot_calendar_table(schedule, slot_labels, course_colors=None, course_groups=None):
    """
    schedule: {course: slot_idx}
    slot_labels: list of strings, one per slot index
    """
    if course_colors is None:
        course_colors = COURSE_COLORS

    # Group courses by slot
    used_slots = sorted(set(schedule.values()))
    slot_courses = {s: [c for c, t in schedule.items() if t == s]
                    for s in used_slots}

    rows_per_slot = max(len(v) for v in slot_courses.values()) if slot_courses else 1
    n_slots = len(used_slots)

    fig, ax = plt.subplots(figsize=(max(5, n_slots * 2), rows_per_slot * 0.9 + 1.2))
    ax.set_xlim(0, n_slots)
    ax.set_ylim(0, rows_per_slot + 0.5)
    ax.axis("off")

    for col, s in enumerate(used_slots):
        label = slot_labels[s] if s < len(slot_labels) else f"Slot {s+1}"
        ax.text(col + 0.5, rows_per_slot + 0.2, label, ha="center", va="bottom",
                fontsize=10, fontweight="bold")
        ax.axvline(col, color="lightgray", lw=0.5)
        for row, course in enumerate(slot_courses[s]):
            color = course_colors.get(course, PALETTE["gray"])
            group = (course_groups or COURSE_GROUP).get(course, "")
            rect = mpatches.FancyBboxPatch(
                (col + 0.05, rows_per_slot - row - 0.9),
                0.9, 0.8,
                boxstyle="round,pad=0.04",
                facecolor=color, edgecolor="white", linewidth=1.2,
                alpha=0.88
            )
            ax.add_patch(rect)
            ax.text(col + 0.5, rows_per_slot - row - 0.5, course,
                    ha="center", va="center", fontsize=9, fontweight="bold",
                    color="white")
            if group:
                ax.text(col + 0.5, rows_per_slot - row - 0.75, f"({group})",
                        ha="center", va="center", fontsize=6, color="white", alpha=0.9)

    ax.set_title("Sınav Takvimi", fontsize=13, pad=8)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 02 — Student × slot matrix
# ---------------------------------------------------------------------------

def plot_student_slot_matrix(schedule, student_enrollments, courses,
                              slot_labels, consec_pairs=None):
    """
    schedule: {course: slot_idx}
    consec_pairs: set of (slot_a, slot_b) pairs that are consecutive (same-day).
    """
    if consec_pairs is None:
        consec_pairs = set()

    used_slots = sorted(set(schedule.values()))
    slot_to_col = {s: i for i, s in enumerate(used_slots)}
    n_slots = len(used_slots)
    n_students = len(student_enrollments)

    # For each student: which slot(s) do they have exams in?
    student_slots = []
    for enr in student_enrollments:
        s_slots = {schedule[c]: c for c in enr if c in schedule}
        student_slots.append(s_slots)

    fig, ax = plt.subplots(figsize=(max(5, n_slots * 1.5), max(4, n_students * 0.45 + 1)))
    ax.set_xlim(0, n_slots)
    ax.set_ylim(0, n_students)
    ax.axis("off")

    for col, s in enumerate(used_slots):
        label = slot_labels[s] if s < len(slot_labels) else f"Slot {s+1}"
        ax.text(col + 0.5, n_students + 0.05, label, ha="center", va="bottom",
                fontsize=8, fontweight="bold", rotation=30)

    for row, s_slots in enumerate(student_slots):
        y = n_students - row - 1
        s_list = sorted(s_slots.keys())

        # Detect consecutive exams (same day)
        consecutive = set()
        for i in range(len(s_list)):
            for j in range(i+1, len(s_list)):
                if (s_list[i], s_list[j]) in consec_pairs or (s_list[j], s_list[i]) in consec_pairs:
                    consecutive.add(s_list[i])
                    consecutive.add(s_list[j])

        for col, s in enumerate(used_slots):
            has_exam = s in s_slots
            if has_exam:
                if len(s_slots) > 1 and s_slots.get(s):  # sanity: 2 exams same slot?
                    if sum(1 for k in s_slots if k == s) > 1:
                        cell_color = PALETTE["red"]
                    elif s in consecutive:
                        cell_color = "#FFAA44"
                    else:
                        cell_color = PALETTE["sky"]
                elif s in consecutive:
                    cell_color = "#FFAA44"
                else:
                    cell_color = PALETTE["sky"]
            else:
                cell_color = PALETTE["light"]

            rect = plt.Rectangle((col + 0.05, y + 0.05), 0.9, 0.85,
                                  facecolor=cell_color, edgecolor="white", linewidth=0.8)
            ax.add_patch(rect)
            if has_exam:
                course = s_slots[s]
                ax.text(col + 0.5, y + 0.47, course,
                        ha="center", va="center", fontsize=6.5, fontweight="bold",
                        color="white" if cell_color != PALETTE["light"] else "black")

    # Student labels (S0, S1, ...)
    for row in range(n_students):
        y = n_students - row - 1
        ax.text(-0.05, y + 0.47, f"Ö{row+1}", ha="right", va="center", fontsize=7)

    legend_patches = [
        mpatches.Patch(color=PALETTE["sky"], label="Sınav var"),
        mpatches.Patch(color="#FFAA44", label="Art arda sınav"),
        mpatches.Patch(color=PALETTE["red"], label="Çakışma (OLMAMALI)"),
        mpatches.Patch(color=PALETTE["light"], label="Sınav yok"),
    ]
    ax.legend(handles=legend_patches, loc="upper right",
              bbox_to_anchor=(1.0, -0.02), fontsize=8, ncol=4)
    ax.set_title("Öğrenci × Sınav Slotu Matrisi", fontsize=12, pad=10)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 03 — Knapsack: AKTS bar comparison
# ---------------------------------------------------------------------------

def plot_knapsack_comparison(greedy_sel, ilp_sel, courses, akts, value, names):
    """Side-by-side horizontal AKTS bars for greedy vs ILP."""
    limit = 14
    fig, axes = plt.subplots(2, 1, figsize=(9, 3.5), sharex=True)
    colors_list = [PALETTE["blue"], PALETTE["orange"], PALETTE["green"], PALETTE["sky"]]
    course_color = {c: colors_list[i] for i, c in enumerate(courses)}

    for ax, sel, label in zip(axes,
                               [greedy_sel, ilp_sel],
                               ["Greedy", "ILP (Optimal)"]):
        pos = 0
        for c in sel:
            ax.barh(0, akts[c], left=pos, color=course_color[c],
                    edgecolor="white", height=0.5)
            ax.text(pos + akts[c]/2, 0, f"{names[c]}\n({akts[c]} AKTS)",
                    ha="center", va="center", fontsize=8, color="white", fontweight="bold")
            pos += akts[c]
        if pos < limit:
            ax.barh(0, limit - pos, left=pos, color="#DDDDDD",
                    edgecolor="white", height=0.5)
            ax.text(pos + (limit-pos)/2, 0, f"Boş\n({limit-pos} AKTS)",
                    ha="center", va="center", fontsize=8, color="#888")
        total_val = sum(value[c] for c in sel)
        ax.set_yticks([0])
        ax.set_yticklabels([f"{label}\n(fayda={total_val})"], fontsize=9)
        ax.axvline(limit, color="red", linestyle="--", lw=1.5, label="14 AKTS limiti")
        ax.set_xlim(0, limit + 0.5)
        ax.grid(False)

    axes[1].set_xlabel("Toplam AKTS", fontsize=10)
    axes[0].set_title("Greedy vs ILP — AKTS Kullanımı Karşılaştırması", fontsize=11)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 03 — Knapsack: value/AKTS efficiency bar chart
# ---------------------------------------------------------------------------

def plot_efficiency_chart(courses, value, akts, names):
    """Bar chart of value/AKTS efficiency ratio."""
    ratios = {c: value[c] / akts[c] for c in courses}
    sorted_c = sorted(courses, key=lambda c: ratios[c], reverse=True)
    colors_list = [PALETTE["blue"], PALETTE["orange"], PALETTE["green"], PALETTE["sky"]]
    course_color = {c: colors_list[i] for i, c in enumerate(courses)}

    fig, ax = plt.subplots(figsize=(7, 3.5))
    bars = ax.bar(range(len(sorted_c)),
                  [ratios[c] for c in sorted_c],
                  color=[course_color[c] for c in sorted_c],
                  edgecolor="white")
    ax.set_xticks(range(len(sorted_c)))
    ax.set_xticklabels([f"{c}\n{names[c]}" for c in sorted_c], fontsize=8)
    for bar, c in zip(bars, sorted_c):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{ratios[c]:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_ylabel("Fayda / AKTS oranı", fontsize=10)
    ax.set_title("Ders Verimliliği — Greedy bu sıraya göre seçer", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 03 — Knapsack: 2D feasibility scatter (Ek Görev 3)
# ---------------------------------------------------------------------------

def plot_2d_knapsack_feasibility(courses, akts, hours, value, akts_limit, hour_limit):
    """Scatter all 2^n combinations on (total_akts, total_hours); color=total_value."""
    from itertools import combinations as combs

    points = []
    for r in range(len(courses) + 1):
        for subset in combs(courses, r):
            ta = sum(akts[c] for c in subset)
            th = sum(hours[c] for c in subset)
            tv = sum(value[c] for c in subset)
            points.append((ta, th, tv, subset))

    xs  = [p[0] for p in points]
    ys  = [p[1] for p in points]
    vs  = [p[2] for p in points]

    fig, ax = plt.subplots(figsize=(7, 6))
    sc = ax.scatter(xs, ys, c=vs, cmap="YlOrRd", s=80, edgecolors="gray",
                    linewidths=0.5, zorder=3)
    plt.colorbar(sc, ax=ax, label="Toplam Fayda")

    # Feasible region box
    rect = mpatches.FancyBboxPatch((0, 0), akts_limit, hour_limit,
                                    boxstyle="square,pad=0",
                                    linewidth=2, edgecolor=PALETTE["blue"],
                                    facecolor="none", linestyle="--", zorder=2)
    ax.add_patch(rect)
    ax.text(akts_limit/2, -0.5, f"≤ {akts_limit} AKTS",
            ha="center", va="top", fontsize=9, color=PALETTE["blue"])
    ax.text(-0.5, hour_limit/2, f"≤ {hour_limit} saat",
            ha="right", va="center", fontsize=9, color=PALETTE["blue"], rotation=90)

    # Highlight best feasible point
    feasible = [(p[2], p[3]) for p in points if p[0] <= akts_limit and p[1] <= hour_limit]
    if feasible:
        best_v, best_subset = max(feasible)
        bx = sum(akts[c] for c in best_subset)
        by = sum(hours[c] for c in best_subset)
        ax.scatter([bx], [by], s=250, color=PALETTE["vermil"], marker="*", zorder=5,
                   label=f"En iyi: {'+'.join(best_subset) or '∅'}, fayda={best_v}")
        ax.annotate(f"+".join(best_subset) or "∅", (bx, by),
                    textcoords="offset points", xytext=(8, 5), fontsize=9,
                    color=PALETTE["vermil"])

    ax.set_xlabel("Toplam AKTS", fontsize=11)
    ax.set_ylabel("Toplam Haftalık Saat", fontsize=11)
    ax.set_title("Tüm Kombinasyonlar — 2 Boyutlu Knapsack", fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 04 — Gantt chart (with C_max dashed line)
# ---------------------------------------------------------------------------

def plot_gantt(assignment, proc_times, num_machines, c_max_val=None, title=None):
    """Gantt chart. assignment: {job: machine}. c_max_val: dashed vertical line."""
    colors_list = [PALETTE["blue"], PALETTE["orange"], PALETTE["green"], PALETTE["sky"],
                   PALETTE["vermil"], PALETTE["purple"], PALETTE["black"], PALETTE["gray"]]

    fig, ax = plt.subplots(figsize=(10, 2.5 + 0.5 * num_machines))
    machine_time = {m: 0 for m in range(num_machines)}

    for job in sorted(assignment.keys()):
        machine = assignment[job]
        duration = proc_times[job][machine]
        start = machine_time[machine]
        color = colors_list[job % len(colors_list)]
        ax.barh(machine, duration, left=start, color=color,
                edgecolor="white", linewidth=1.2, height=0.6)
        ax.text(start + duration/2, machine, f"G{job}",
                ha="center", va="center", fontsize=9, color="white", fontweight="bold")
        machine_time[machine] += duration

    if c_max_val is not None:
        ax.axvline(c_max_val, color=PALETTE["red"], linestyle="--", lw=2, zorder=5)
        ax.text(c_max_val + 0.1, num_machines - 0.5,
                f"C_max={c_max_val:.1f}", color=PALETTE["red"], fontsize=9)

    ax.set_yticks(range(num_machines))
    ax.set_yticklabels([f"İşlemci {m}" for m in range(num_machines)], fontsize=9)
    ax.set_xlabel("Zaman", fontsize=10)
    ax.set_title(title or "Görev Atama — Gantt Grafiği", fontsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# (legacy) Exam schedule bar chart — kept for backward compatibility
# ---------------------------------------------------------------------------

def plot_exam_schedule(schedule, course_colors=None):
    if course_colors is None:
        course_colors = COURSE_COLORS
    if not schedule:
        return None
    slots = sorted(set(schedule.values()))
    slot_courses = {s: [c for c, t in schedule.items() if t == s] for s in slots}
    fig, ax = plt.subplots(figsize=(max(6, len(slots)*1.4), 4))
    for i, slot in enumerate(slots):
        for j, course in enumerate(slot_courses[slot]):
            color = course_colors.get(course, PALETTE["gray"])
            ax.bar(i, 1, bottom=j, color=color, edgecolor="white", linewidth=0.8)
            ax.text(i, j + 0.5, course, ha="center", va="center",
                    fontsize=9, fontweight="bold", color="white")
    ax.set_xticks(range(len(slots)))
    ax.set_xticklabels([f"Slot {s+1}" for s in slots], fontsize=10)
    ax.set_ylabel("Dersler")
    ax.set_title("Sınav Takvimi", fontsize=12)
    ax.set_ylim(0, max(len(v) for v in slot_courses.values()) + 0.5)
    plt.tight_layout()
    return fig
