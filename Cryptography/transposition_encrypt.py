import pyperclip

def main():
    uMessage = input("Please Enter a Message to Get Encrypted: ")
    keyMsg = 10
    cipherText = encryptMessage(keyMsg, uMessage)
    print(cipherText + "|")
    pyperclip.copy(cipherText)


def encryptMessage(key, message):
    cipherText = [''] * key
    for col in range(key):
        pointer = col
        while pointer < len(message):
            cipherText[col] += message[pointer]
            pointer += key
        return ''.join(cipherText)


if __name__ == '__main__':
    main()
