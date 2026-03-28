# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

* Three core actions 
1. Add owner and pet information so the app knows who the care plan is for.
2. Create and update pet care tasks such as feeding, walks, medicine, and grooming.
3. View a daily care plan that shows which tasks should be done and in what order.

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For my initial UML design, I chose classes that matched the main parts of the app: the owner, the pet, the care tasks, the daily plan, and the scheduler. I used Owner to store the pet owner’s name, available time, and preferences. I used Pet to store basic pet information like name, species, age, and notes. I used Task to represent each care activity, including its title, duration, priority, category, and whether it is required.

I also included PlanItem, DailyPlan, and PawPalScheduler to handle scheduling. PlanItem represents one scheduled task with a time and a short reason. DailyPlan stores the final schedule, the total planned time, and any tasks that could not be scheduled. PawPalScheduler is responsible for the main scheduling process, such as sorting tasks by priority, checking time limits, building the plan, and explaining why tasks were chosen. This design helped separate the data classes from the class that controls the scheduling logic.

**b. Design changes**

- Did your design change during implementation?
Yes, several changes were made during implementation after reviewing the initial skeleton for missing relationships and logic issues.

- If yes, describe at least one change and why you made it.
1. Owner.preferences changed from a list to a dictionary. A flat list of strings cannot be queried for specific values. A dictionary like {"preferred_time": "morning"} lets the scheduler look up preferences directly when building explanations.

2. Added a date field to DailyPlan. Without it, plans generated on different days are indistinguishable from each other. The field defaults to today's date so it is always populated automatically.

3. Fixed the order of sort and filter in the scheduler. If filtering ran before sorting, a high-priority short task could be dropped because a low-priority long task already used up the time budget. The fix sorts tasks by priority first, then greedily picks tasks that fit the remaining time.

4. Replaced the stored total_minutes field with a computed method. A stored integer has to be manually updated every time a task is added. If anything bypasses the update, the count silently goes wrong. Computing it from the actual list of items on demand removes that risk.

5. Defined scheduled_time as a fixed "HH:MM" 24-hour format. The field was an open string with no enforced format, which would cause inconsistent display across the UI. A helper function now converts all times to the same format, starting the schedule at 08:00.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
