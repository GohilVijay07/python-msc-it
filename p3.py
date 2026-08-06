password = input("Enter a password: ")
uppercase = False
lowercase = False
digit = False
special = False
repeated = False
minimum_length = len(password) >= 8
special_characters = "!@#$%^&*()-_=+[]{}|\\/:;'<>,.?"

for i in range(len(password)):
    char = password[i]
    if char.isupper():
        uppercase = True
    if char.islower():
        lowercase = True
    if char.isdigit():
        digit = True
    if char in special_characters:
        special = True

for i in range(len(password) - 1):
    if(password[i] == password[i + 1]):
        repeated = True
        break

print("Password Strength Analysis:")
print(f"Minimum Length (8+): {minimum_length}")
print(f"Uppercase Letters: {uppercase}")
print(f"Lowercase Letters: {lowercase}")
print(f"Digits: {digit}")
print(f"Special Characters: {special}")
print(f"Repeated Characters: {repeated}")

criteria_met = sum([minimum_length, uppercase, lowercase, digit, special, not repeated])
print(f"Strength Score: {criteria_met}/6")

if minimum_length and uppercase and lowercase and digit and special and not repeated:
    print("Your password is strong.")
elif criteria_met >= 4:
    print("Your password is medium. Try adding more variety.")
else:
    print("Your password does not meet the strength requirements.")