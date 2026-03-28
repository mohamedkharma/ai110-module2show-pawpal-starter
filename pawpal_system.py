"""
PawPal logic layer.

This module contains the core backend classes for tasks, pets, owners,
and scheduling.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    """Represents a single pet care activity."""

    description: str
    time_minutes: int
    frequency: str
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.completed = False

    def is_due_today(self) -> bool:
        """Return whether the task should be included in today's plan."""
        return not self.completed


@dataclass
class Pet:
    """Stores pet details and the tasks assigned to that pet."""

    name: str
    species: str
    age: int = 0
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet."""
        self.tasks.append(task)

    def remove_task(self, description: str) -> bool:
        """Remove the first task with a matching description."""
        for index, task in enumerate(self.tasks):
            if task.description == description:
                del self.tasks[index]
                return True
        return False

    def get_pending_tasks(self) -> List[Task]:
        """Return tasks that are not yet completed."""
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Return tasks that have been completed."""
        return [task for task in self.tasks if task.completed]


@dataclass
class Owner:
    """Stores owner details and manages multiple pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Remove the first pet with a matching name."""
        for index, pet in enumerate(self.pets):
            if pet.name == pet_name:
                del self.pets[index]
                return True
        return False

    def get_pet(self, pet_name: str) -> Pet | None:
        """Return a pet by name if it exists."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across all pets."""
        pending_tasks: List[Task] = []
        for pet in self.pets:
            pending_tasks.extend(pet.get_pending_tasks())
        return pending_tasks


class Scheduler:
    """Retrieves, organizes, and manages tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Store the owner whose pets and tasks will be scheduled."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieve every task from the owner's pets."""
        return self.owner.get_all_tasks()

    def get_pending_tasks(self) -> List[Task]:
        """Retrieve all incomplete tasks from the owner's pets."""
        return self.owner.get_all_pending_tasks()

    def sort_tasks_by_time(self) -> List[Task]:
        """Return pending tasks ordered by shortest time first."""
        return sorted(self.get_pending_tasks(), key=lambda task: task.time_minutes)

    def sort_tasks_by_pet(self) -> List[tuple[str, Task]]:
        """Return pending tasks grouped into pet-task pairs."""
        pet_task_pairs: List[tuple[str, Task]] = []
        for pet in self.owner.pets:
            for task in pet.get_pending_tasks():
                pet_task_pairs.append((pet.name, task))
        return pet_task_pairs

    def build_daily_task_list(self) -> List[Task]:
        """Build a simple daily list of tasks that are due today."""
        return [task for task in self.get_pending_tasks() if task.is_due_today()]

    def mark_task_complete(self, pet_name: str, description: str) -> bool:
        """Mark a matching task as complete for a specific pet."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return False

        for task in pet.tasks:
            if task.description == description:
                task.mark_complete()
                return True
        return False
