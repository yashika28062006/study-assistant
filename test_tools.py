
from tools import days_until_exam, split_study_hours

print("\n--- TEST 1: EXAM COUNTDOWN ---")

result1 = days_until_exam.invoke({
    "exam_date": "2026-12-01"
})

print(result1)


print("\n--- TEST 2: STUDY HOUR SPLITTER ---")

result2 = split_study_hours.invoke({
    "total_hours": 6,
    "subjects": "Python, DSA, Mathematics"
})

print(result2)


print("\n--- TEST 3: INVALID INPUT ---")

result3 = split_study_hours.invoke({
    "total_hours": 0,
    "subjects": "Python, DSA"
})

print(result3)

