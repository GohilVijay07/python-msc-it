nums = input("Enter your values: ")

duplicates = []

for ch in nums:
    if ch not in duplicates:
        if nums.count(ch) > 1:
            duplicates.append(ch)

for d in duplicates:
    print(d)