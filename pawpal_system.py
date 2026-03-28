"""
PawPal logic layer.

This module contains the backend classes for representing owners, pets,
tasks, and the scheduling system that will generate a daily care plan.
"""

from dataclasses import dataclass, field
from datetime import date as _date
from typing import Dict, List, Optional


@dataclass
class Owner:
    """Represents the pet owner using the app."""

    name: str
    available_minutes: int
    # Keys: "preferred_time" ("morning"/"afternoon"/"evening"),
    #       "avoid_category" (list of category strings), etc.
    preferences: Dict[str, object] = field(default_factory=dict)

    def update_preferences(self, preferences: Dict[str, object]) -> None:
        """Replace the owner's scheduling preferences."""
        self.preferences = preferences


@dataclass
class Pet:
    """Represents a pet that needs care tasks."""

    name: str
    species: str
    age: Optional[int] = None
    notes: str = ""

    def get_profile_summary(self) -> str:
        """Return a short summary of the pet."""
        age_str = f", age {self.age}" if self.age is not None else ""
        notes_str = f" ({self.notes})" if self.notes else ""
        return f"{self.name} the {self.species}{age_str}{notes_str}"


@dataclass
class Task:
    """Represents a care task that may be scheduled."""

    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    category: str = "general"
    notes: str = ""
    is_required: bool = True

    def is_high_priority(self) -> bool:
        """Return whether this task should be treated as high priority."""
        return self.priority == "high"

    def fits_within(self, available_minutes: int) -> bool:
        """Return whether the task fits within a time budget."""
        return self.duration_minutes <= available_minutes


@dataclass
class PlanItem:
    """Represents one scheduled task inside a daily plan.

    scheduled_time uses "HH:MM" 24-hour format (e.g. "08:30").
    """

    task: Task
    scheduled_time: str  # "HH:MM" 24-hour, e.g. "08:30"
    reason: str = ""

    def get_display_text(self) -> str:
        """Return a UI-friendly description of this plan item."""
        return (
            f"{self.scheduled_time} — {self.task.title} "
            f"({self.task.duration_minutes} min) [{self.task.priority}]"
            + (f"\n  {self.reason}" if self.reason else "")
        )


@dataclass
class DailyPlan:
    """Represents the final set of scheduled tasks for a day."""

    owner: Owner
    pet: Pet
    date: str = field(default_factory=lambda: _date.today().isoformat())
    items: List[PlanItem] = field(default_factory=list)
    unscheduled_tasks: List[Task] = field(default_factory=list)

    def add_item(self, item: PlanItem) -> None:
        """Add a scheduled item to the plan."""
        self.items.append(item)

    def add_unscheduled_task(self, task: Task) -> None:
        """Track a task that could not be scheduled."""
        self.unscheduled_tasks.append(task)

    def get_total_minutes(self) -> int:
        """Return total scheduled minutes, computed from items."""
        return sum(item.task.duration_minutes for item in self.items)

    def get_summary(self) -> str:
        """Return a summary of the plan for display."""
        lines = [
            f"Daily plan for {self.pet.name} — {self.date}",
            f"Owner: {self.owner.name} | Total time: {self.get_total_minutes()} min",
            "",
        ]
        if self.items:
            lines.append("Scheduled:")
            for item in self.items:
                lines.append(f"  {item.get_display_text()}")
        if self.unscheduled_tasks:
            lines.append("\nNot scheduled (time or priority):")
            for task in self.unscheduled_tasks:
                lines.append(f"  - {task.title} ({task.duration_minutes} min, {task.priority})")
        return "\n".join(lines)


_PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}
# Starting time for the first scheduled task (minutes from midnight)
_START_MINUTE = 8 * 60  # 08:00


def _minutes_to_hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


class PawPalScheduler:
    """Builds a daily care plan from owner, pet, and task information."""

    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task]) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks = tasks
        self.last_plan: Optional[DailyPlan] = None

    def generate_daily_plan(self) -> DailyPlan:
        """Create a daily plan based on time, priority, and preferences.

        Order of operations: sort by priority first, then greedily pick
        tasks that fit in the remaining time budget. This ensures a
        high-priority short task is never dropped in favour of a lower-
        priority long one that happened to be evaluated first.
        """
        plan = DailyPlan(owner=self.owner, pet=self.pet)
        sorted_tasks = self.sort_tasks_by_priority()

        remaining = self.owner.available_minutes
        cursor = _START_MINUTE  # rolling clock pointer (minutes from midnight)

        for task in sorted_tasks:
            if task.fits_within(remaining):
                reason = self.explain_task_choice(task)
                item = PlanItem(
                    task=task,
                    scheduled_time=_minutes_to_hhmm(cursor),
                    reason=reason,
                )
                plan.add_item(item)
                remaining -= task.duration_minutes
                cursor += task.duration_minutes
            else:
                plan.add_unscheduled_task(task)

        self.last_plan = plan
        return plan

    def sort_tasks_by_priority(self) -> List[Task]:
        """Return tasks ordered high → medium → low, required tasks first."""
        return sorted(
            self.tasks,
            key=lambda t: (_PRIORITY_RANK.get(t.priority, 0), t.is_required),
            reverse=True,
        )

    def filter_tasks_by_time(self, available_minutes: int) -> List[Task]:
        """Return a greedy subset of tasks (already sorted) that fit the budget."""
        result: List[Task] = []
        remaining = available_minutes
        for task in self.sort_tasks_by_priority():
            if task.fits_within(remaining):
                result.append(task)
                remaining -= task.duration_minutes
        return result

    def explain_task_choice(self, task: Task) -> str:
        """Return an explanation for why a task was included in the plan."""
        parts = []
        if task.is_required:
            parts.append("required task")
        if task.is_high_priority():
            parts.append("high priority")
        preferred_time = self.owner.preferences.get("preferred_time")
        if preferred_time:
            parts.append(f"owner prefers {preferred_time} care")
        if not parts:
            parts.append(f"{task.priority} priority, fits in available time")
        return "; ".join(parts).capitalize() + "."
