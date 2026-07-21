import time


class ExecutionTimeline:
    """
    Records and displays a visual execution timeline for the agent.
    """

    def __init__(self):
        self.steps = []
        self._start_time = time.time()

    def record(self, name, start, end, status="ok", icon="▶"):
        """
        Add a completed step to the timeline.
        """
        self.steps.append({
            "name": name,
            "start": start - self._start_time,
            "end": end - self._start_time,
            "duration": end - start,
            "status": status,
            "icon": icon
        })

    def print_timeline(self):
        """
        Print a visual ASCII timeline to the console.
        """
        if not self.steps:
            print("\n📊 EXECUTION TIMELINE\n  (no steps recorded)")
            return

        total_duration = max(s["end"] for s in self.steps)
        bar_width = 40

        print("\n📊 EXECUTION TIMELINE")
        print("=" * 70)
        print(f"{'Step':<20} {'Bar':<42} {'Duration':>8}")
        print("-" * 70)

        for step in self.steps:
            duration = step["duration"]
            start_frac = step["start"] / max(total_duration, 0.001)
            end_frac = step["end"] / max(total_duration, 0.001)

            start_pos = int(start_frac * bar_width)
            end_pos = max(start_pos + 1, int(end_frac * bar_width))

            bar = (
                " " * start_pos
                + "█" * (end_pos - start_pos)
                + " " * (bar_width - end_pos)
            )

            status_icon = "✅" if step["status"] == "ok" else "❌"
            label = f"{step['icon']} {step['name']}"
            print(f"{label:<20} |{bar}| {duration:>6.2f}s {status_icon}")

        print("-" * 70)
        print(f"{'Total':<20}  {total_duration:>47.2f}s")
        print(f"\nTimeline scale: |{'─' * bar_width}|")
        print(f"                0s{' ' * (bar_width - 4)}{total_duration:.1f}s")
