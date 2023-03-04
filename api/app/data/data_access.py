from app.data.database import db
from app.data.models import List
from app.data.cache import cache
from datetime import datetime


@cache.memoize(50)
def get_lists_by_user(current_user):
    return List.query.filter(List.user == current_user).all()


@cache.memoize(50)
def get_summary_by_user(current_user):
    lists = List.query.filter(List.user == current_user).all()
    user_summary = []
    today = datetime.today().date()

    for l in lists:
        counts = {}
        counts["list_id"] = l.list_id
        counts['list_name'] = l.name
        counts["total"] = len(l.cards)
        counts["total_completed"] = 0
        counts["total_incomplete"] = 0
        counts['d_passed'] = 0
        counts['date_count'] = []
        counts['date_labels'] = []
        counts['date_data'] = []

        for card in l.cards:
            if card.completed == 1:
                # calculate how many tasks are completed
                counts["total_completed"] += 1
                counts["date_count"].append(card.completed_datetime.date())
            else:
                # calculate how many tasks are incomplete
                counts["total_incomplete"] += 1
                if today > card.deadline:
                    # Out of the total incomplete tasks, calculate how many have passed the deadline
                    counts["d_passed"] += 1

        if counts['date_count'] != []:
            counts['date_labels'] = list(set(counts['date_count']))
        for i in counts['date_labels']:
            counts['date_data'].append(counts['date_count'].count(i))

        user_summary.append(counts)

    return user_summary
