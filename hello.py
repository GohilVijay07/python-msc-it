# Ask the user for an integer (whole number)
number = int(input("Enter a whole number: "))

# Check if the remainder when dividing by 2 is 0
if number % 2 == 0:
    print("This is an EVEN number.")
else:
    print("This is an ODD number.")