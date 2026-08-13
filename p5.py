n = int(input("Enter Number of Students (Minimum 5): "))

if n < 5:
    print("Please enter at least 5 students.")

else:
    students = []

    # Input student details
    for i in range(n):

        print("\n--- Student", i + 1, "---")

        roll = int(input("Roll No: "))
        name = input("Name: ")

        total = 0

        # Enter 5 subject marks
        subject = ["python","java","php","linux","Data Structures and Algorithms"]
        for j in range(5):
            mark = int(input("Enter your Marks in  " + subject[j] + ": "))    # ask user to enter marks for each subject   
            if mark > 100 or mark < 0:
                print("Invalid Mark")
                continue
            total = total + mark
            #  mark = int(input(subject[j] + " Marks: "))  # ask user to enter marks for each subject 
    
        percentage = total / 5

        # Grade
        if percentage >= 90:
            grade = "Distinction"
        elif percentage >= 80:
            grade = "First Division"
        elif percentage >= 70:
            grade = "Second Division"
        elif percentage >= 60:
            grade = "Pass"
        else:
            grade = "Fail"

        students.append([roll, name, total, percentage, grade])

    # Sort students by total marks
    students.sort(key=lambda x: x[2], reverse=True)

    print("\n========== Rank List ==========")

    rank = 0
    last_marks = -1

    for student in students:

        # Same marks = same rank
        if student[2] != last_marks:
            rank = rank + 1
            last_marks = student[2]

        print("\nRank:", rank)
        print("Roll No:", student[0])
        print("Name:", student[1])
        print("Total:", student[2])
        print("Percentage:", round(student[3], 2), "%")
        print("Grade:", student[4])