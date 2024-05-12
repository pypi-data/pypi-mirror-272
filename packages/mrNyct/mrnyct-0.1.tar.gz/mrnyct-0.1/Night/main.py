import subprocess
import sys
import socket

def req(*args):
    print('\033[2J\033[H', end='')
    print('\033[96mAttention as we are using some external libraries in our code - we have to install them first, this will require an Internet connection!\033[0m')
    v = input(f'To continue, enter any key\n\t\tTo exit \033[91m[x]\033[0m: ')
    if v.lower() == 'x':
        sys.exit()
    try:
        # Attempt to connect to a well-known website
        socket.create_connection(("www.google.com", 80))  # Just checking for internet
        subprocess.run(['pip', 'install'] + list(args))
        print('\033[2J\033[H', end='')
    except OSError:
        print("\033[91mError: Not connected to the internet.\033[0m")
        sys.exit(1)

