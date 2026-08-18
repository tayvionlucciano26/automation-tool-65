import sys

class InvalidInputError(Exception):
    pass

def validate_input(user_input):
    if not user_input:
        raise InvalidInputError('Input cannot be empty')
    if not isinstance(user_input, str):
        raise InvalidInputError('Input must be a string')
    if len(user_input) < 3:
        raise InvalidInputError('Input must be at least 3 characters long')

def main_processing_loop():
    while True:
        user_input = input('Please enter a command: ')
        try:
            validate_input(user_input)
            print(f'Processing: {user_input}')
            # Add further processing logic here
        except InvalidInputError as e:
            print(f'Error: {e}')
        except KeyboardInterrupt:
            print('\nExiting...')
            sys.exit(0)

if __name__ == '__main__':
    main_processing_loop()