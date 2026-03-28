from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task(description="Morning walk", time_minutes=20, frequency="daily")

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog", age=4)
    starting_count = len(pet.tasks)

    pet.add_task(Task(description="Breakfast", time_minutes=10, frequency="daily"))

    assert len(pet.tasks) == starting_count + 1
