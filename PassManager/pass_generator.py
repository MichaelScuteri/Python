import random

def generate_pass(account):
    upper = chr(random.randint(65, 90))
    lower = chr(random.randint(97, 122))
    num = str(random.randint(10, 99))
    upper2 = chr(random.randint(65, 90))
    lower2 = chr(random.randint(97, 122))
    num2 = str(random.randint(10, 99))
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+']

    symbol = random.choice(symbols)
    symbol2 = random.choice(symbols)

    password = upper + num + lower + symbol + upper2 + lower2 + num2 + symbol2

    print(f'\nPassword generated for {account}:')
    print(f'{password}\n')

def main():
    print('-------- Password Generator V1.0 ---------')
    while True:
        account = input('Enter username to generate password (type "exit" to quit): ')
        if account.lower() == 'exit':
            break
        generate_pass(account)

if __name__ == "__main__":
    main()