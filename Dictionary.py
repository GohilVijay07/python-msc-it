# Python program to demonstrate all common dictionary functions

def show_dictionary_functions():
    # Creating a dictionary
    student = {"name": "vijay", "age": 20, "course": "MSc IT"}
    print("Original dictionary:", student)

    # Accessing values
    print("Name:", student["name"])
    print("Age:", student.get("age"))

    # Adding and updating values
    student["semester"] = 1
    student.update({"age": 21, "city": "gujarat"})
    print("After adding/updating:", student)

    # setdefault()
    student.setdefault("email", "vijay@example.com")
    print("After setdefault:", student)

    # Removing values
    student.pop("course")
    print("After pop:", student)

    student.popitem()
    print("After popitem:", student)

    # Dictionary methods
    print("Keys:", list(student.keys()))
    print("Values:", list(student.values()))
    print("Items:", list(student.items()))

    # Membership check
    print("name in student:", "name" in student)
    print("city not in student:", "city" not in student)

    # Copy and clear
    copied_student = student.copy()
    print("Copied dictionary:", copied_student)
    copied_student.clear()
    print("After clear:", copied_student)

    # fromkeys()
    new_dict = dict.fromkeys(["a", "b", "c"], 0)
    print("Fromkeys result:", new_dict)

    # Nested dictionary
    info = {"student": student, "status": "active"}
    print("Nested dictionary:", info)


if __name__ == "__main__":
    show_dictionary_functions()
