from datetime import date, datetime, timedelta

def generate_plan(subjects):
    """
    Creates a simple weighted study plan.
    Hard subjects receive more minutes than easy subjects.
    Chapters are distributed from today until each subject's exam date.
    """
    difficulty_weight = {"Easy": 1, "Medium": 1.3, "Hard": 1.7}
    expanded = []

    for s in subjects:
        chapters = [c.strip() for c in s["chapters"].split(",") if c.strip()]
        if not chapters:
            continue

        exam = datetime.strptime(s["exam_date"], "%Y-%m-%d").date()
        start = date.today()
        days = max((exam - start).days, 1)
        daily_minutes = max(int(float(s["hours_per_day"]) * 60), 15)
        weight = difficulty_weight.get(s["difficulty"], 1)

        for chapter in chapters:
            expanded.append({
                "subject": s["name"],
                "chapter": chapter,
                "exam": exam,
                "days": days,
                "minutes": max(15, int(daily_minutes * weight / len(chapters)))
            })

    plan = []
    for item in expanded:
        # Spread chapters across the available days.
        chapter_index = expanded.index(item)
        target = item["exam"] - timedelta(days=(chapter_index % max(item["days"], 1)))
        if target < date.today():
            target = date.today()

        plan.append({
            "subject": item["subject"],
            "chapter": item["chapter"],
            "date": target.isoformat(),
            "minutes": min(item["minutes"], 180)
        })

    # Sort chronologically
    return sorted(plan, key=lambda x: (x["date"], x["subject"]))
