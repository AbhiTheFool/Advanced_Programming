from typing import List, Dict, Set
from collections import defaultdict
from functools import reduce

SAMPLE_LOGS: List[Dict] = [
    {"user": "CSB2101", "action": "GitHub", "duration": 45.5},
    {"user": "CSB2102", "action": "StackOverflow", "duration": 15.0},
    {"user": "CSB2101", "action": "VSCode", "duration": 120.0},
    {"user": "CSB2103", "action": "YouTube", "duration": 60.5},
    {"user": "CSB2102", "action": "GitHub", "duration": 30.0},
    {"user": "CSB2104", "action": "LeetCode", "duration": 90.0},
    {"user": "CSB2101", "action": "StackOverflow", "duration": 10.5},
    {"user": "CSB2103", "action": "Netflix", "duration": 150.0},
    {"user": "CSB2105", "action": "VSCode", "duration": 200.0},
    {"user": "CSB2104", "action": "GitHub", "duration": 25.0},
]

def total_time_per_user(logs: List[Dict]) -> Dict[str, float]:
    time_map = defaultdict(float)
    for log in logs:
        time_map[log["user"]] += log["duration"]
    return dict(time_map)

def most_active_users(logs: List[Dict], k: int) -> List[str]:
    time_map = total_time_per_user(logs)
    return [user for user, _ in sorted(time_map.items(), key=lambda x: x[1], reverse=True)[:k]]

def unique_actions(logs: List[Dict]) -> Set[str]:
    return {log["action"] for log in logs}

def total_activity_time(logs: List[Dict]) -> float:
    if not logs: return 0.0
    return reduce(lambda acc, log: acc + log["duration"], logs, 0.0)

def time_per_action(logs: List[Dict]) -> Dict[str, float]:
    action_map = defaultdict(float)
    for log in logs:
        action_map[log["action"]] += log["duration"]
    return dict(action_map)

def user_action_breakdown(logs: List[Dict]) -> Dict[str, Dict[str, float]]:
    breakdown = defaultdict(lambda: defaultdict(float))
    for log in logs:
        breakdown[log["user"]][log["action"]] += log["duration"]
    return {u: dict(actions) for u, actions in breakdown.items()}

def above_average_users(logs: List[Dict]) -> List[str]:
    if not logs: return []
    time_map = total_time_per_user(logs)
    avg_time = total_activity_time(logs) / len(time_map)
    return [user for user, total in time_map.items() if total > avg_time]

W = 58

def header(title: str) -> None:
    print(f"\n╔{'═' * W}╗")
    print(f"║  {title:<{W-2}}║")
    print(f"╚{'═' * W}╝")

def row(label: str, value: str) -> None:
    print(f"  {label:<22} {value}")

def divider() -> None:
    print(f"  {'─' * (W - 2)}")

def main() -> None:
    logs = SAMPLE_LOGS

    header("RAW ACTIVITY LOGS  (10 records)")
    print(f"  {'Roll No':<10} {'Action':<15} {'Duration (min)':>14}")
    divider()
    for log in logs:
        print(f"  {log['user']:<10} {log['action']:<15} {log['duration']:>14.1f}")

    header("1 · TOTAL SCREEN TIME PER USER  [dict + defaultdict]")
    time_map = total_time_per_user(logs)
    print(f"  {'Roll No':<10} {'Total Time (min)':>16}  Bar")
    divider()
    max_t = max(time_map.values()) if time_map else 1
    for user, total in sorted(time_map.items()):
        bar = "█" * int((total / max_t) * 30)
        print(f"  {user:<10} {total:>16.2f}  {bar}")

    header("2 · TOP-K MOST ACTIVE USERS  [sorted() + key=lambda]")
    k = 3
    top_k = most_active_users(logs, k)
    print(f"  Ranking top {k} students by cumulative screen time:\n")
    for rank, user in enumerate(top_k, start=1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "  ")
        print(f"  {medal}  #{rank}  {user:<10}  →  {time_map[user]:.2f} min")

    header("3 · UNIQUE APPS / WEBSITES  [set-comprehension]")
    actions = unique_actions(logs)
    print(f"  Total unique actions: {len(actions)}\n")
    for action in sorted(actions):
        print(f"    • {action}")

    header("4 · GRAND TOTAL SCREEN TIME  [functools.reduce()]")
    grand_total = total_activity_time(logs)
    avg_per_user = grand_total / len(time_map) if time_map else 0
    print(f"  reduce(lambda acc, log: acc + log['duration'], logs, 0.0)")
    print(f"\n  Grand total  : {grand_total:.2f} min  ({grand_total/60:.2f} hrs)")
    print(f"  Batch avg    : {avg_per_user:.2f} min per student")

    header("5 · TOTAL TIME PER APP / WEBSITE  [defaultdict]")
    action_time = time_per_action(logs)
    print(f"  {'App / Website':<15} {'Total Time (min)':>16}  Popularity Bar")
    divider()
    max_a = max(action_time.values()) if action_time else 1
    for action, t in sorted(action_time.items(), key=lambda x: -x[1]):
        bar = "▓" * int((t / max_a) * 25)
        print(f"  {action:<15} {t:>16.2f}  {bar}")

    header("6 · PER-USER ACTION BREAKDOWN  [nested defaultdict]")
    breakdown = user_action_breakdown(logs)
    for user in sorted(breakdown):
        print(f"\n  {user}")
        for action, t in sorted(breakdown[user].items(), key=lambda x: -x[1]):
            print(f"    ↳ {action:<15}  {t:.2f} min")

    header("7 · STUDENTS ABOVE BATCH AVERAGE  [reduce + comprehension]")
    above = above_average_users(logs)
    print(f"  Batch average : {avg_per_user:.2f} min\n")
    for user in above:
        diff = time_map[user] - avg_per_user
        print(f"  {user}  →  {time_map[user]:.2f} min  (+{diff:.2f} above avg)")

    header("8 · COMPLEXITY ANALYSIS")
    print(f"""
  Legend:
    N = total log entries   U = unique users   A = unique actions
    K = top-K parameter     C = actions/user

  ┌─────────────────────────────────────┬──────────────┬──────────────┐
  │ Function                            │ Time         │ Space        │
  ├─────────────────────────────────────┼──────────────┼──────────────┤
  │ total_time_per_user()               │ O(N)         │ O(U)         │
  │   └─ defaultdict O(1) per insert    │              │              │
  ├─────────────────────────────────────┼──────────────┼──────────────┤
  │ most_active_users(k)                │ O(N+U·logU)  │ O(U)         │
  │   └─ aggregate      O(N)            │              │              │
  │   └─ Timsort        O(U log U)      │              │              │
  │   └─ slice [:k]     O(K)            │              │              │
  ├─────────────────────────────────────┼──────────────┼──────────────┤
  │ unique_actions()                    │ O(N)         │ O(A)         │
  │   └─ set-comprehension O(1) insert  │              │              │
  ├─────────────────────────────────────┼──────────────┼──────────────┤
  │ total_activity_time() via reduce()  │ O(N)         │ O(1)         │
  ├─────────────────────────────────────┼──────────────┼──────────────┤
  │ time_per_action()                   │ O(N)         │ O(A)         │
  ├─────────────────────────────────────┼──────────────┼──────────────┤
  │ user_action_breakdown()             │ O(N)         │ O(U × A)     │
  ├─────────────────────────────────────┼──────────────┼──────────────┤
  │ above_average_users()               │ O(N+U·logU)  │ O(U)         │
  └─────────────────────────────────────┴──────────────┴──────────────┘
""")

if __name__ == "__main__":
    main()
