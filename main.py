from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)

    mochi.add_task(Task(description="Morning walk", time_minutes=20, frequency="daily"))
    mochi.add_task(Task(description="Breakfast", time_minutes=10, frequency="daily"))
    luna.add_task(Task(description="Litter cleaning", time_minutes=15, frequency="daily"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    todays_tasks = scheduler.sort_tasks_by_pet()

    print("Today's Schedule")
    print("----------------")
    for pet_name, task in todays_tasks:
        print(f"{pet_name}: {task.description} ({task.time_minutes} minutes, {task.frequency})")


if __name__ == "__main__":
    main()
