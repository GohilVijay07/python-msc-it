nums = list(map(int, input("Enter roll numbers separated by spaces: ").split()))

for i in range(1, max(nums) + 1):
    if i not in nums:
        print("Missing Roll Number:", i)