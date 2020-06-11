message = input("Please enter a message to get Encrypted: ")

translated = ''

i = len(message) - 1

while i >= 0:
    translated = translated + message[i]
    i = i - 1

print(translated)
