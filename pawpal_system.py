"""
PawPal logic layer.

This module contains the backend classes for representing owners, pets,
tasks, and the scheduling system that will generate a daily care plan.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Owner:
    """Represents the pet owner using the app."""

    name: str
    available_minutes: int
    preferences: List[str] = field(default_factory=list)

    def update_preferences(self, preferences: List[str]) -> None:
        """Replace the owner's scheduling preferences."""
        pass


@dataclass
class Pet:
    """Represents a pet that needs care tasks."""

    name: str
    species: str
    age: Optional[int] = None
    notes: str = ""

    def get_profile_summary(self) -> str:
        """Return a short summary of the pet."""
        pass


@dataclass
class Task:
    """Represents a care task that may be scheduled."""

    title: str
    duration_minutes: int
    priority: str
    category: str = "general"
    notes: str = ""
    is_required: bool = True

    def is_high_priority(self) -> bool:
        """Return whether this task should be treated as high priority."""
        pass

    def fits_within(self, available_minutes: int) -> bool:
        """Return whether the task fits within a time budget."""
        pass


@dataclass
class PlanItem:
    """Represents one scheduled task inside a daily plan."""

    task: Task
    scheduled_time: str
    reason: str = ""

    def get_display_text(self) -> str:
        """Return a UI-friendly description of this plan item."""
        pass


@dataclass
class DailyPlan:
    """Represents the final set of scheduled tasks for a day."""

    owner: Owner
    pet: Pet
    items: List[PlanItem] = field(default_factory=list)
    unscheduled_tasks: List[Task] = field(default_factory=list)
    total_minutes: int = 0

    def add_item(self, item: PlanItem) -> None:
        """Add a scheduled item to the plan."""
        pass

    def add_unscheduled_task(self, task: Task) -> None:
        """Track a task that could not be scheduled."""
        pass

    def get_summary(self) -> str:
        """Return a summary of the plan for display."""
        pass


class PawPalScheduler:
    """Builds a daily care plan from owner, pet, and task information."""

    def __init__(self, owner: Owner, pet: Pet, tasks: List[Task]) -> None:
        self.owner = owner
        self.pet = pet
        self.tasks = tasks

    def generate_daily_plan(self) -> DailyPlan:
        """Create a daily plan based on time, priority, and preferences."""
        pass

    def sort_tasks_by_priority(self) -> List[Task]:
        """Return tasks ordered by scheduling importance."""
        pass

    def filter_tasks_by_time(self, available_minutes: int) -> List[Task]:
        """Return tasks that can fit within the available time."""
        pass

    def explain_task_choice(self, task: Task) -> str:
        """Return an explanation for why a task was or was not chosen."""
        pass
