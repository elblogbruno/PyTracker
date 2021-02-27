from email_validator import validate_email, EmailNotValidError
import csv
import os
import json
import time

#Creates a random number it will be used as an identifier.
def create_tracking_code():
    return str(int(time.time()%99999))

# Define a function for 
# for validating an Email 
def check(email):  
    try:
        # Validate.
        valid = validate_email(email)

        return valid
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        print(str(e))
        return False

#Ask and writes server options
def get_options(logging):
    logging.info("Saving options.")
    if os.path.isfile('options.json'):
            logging.info("Initiating with a found options.json file.")

            with open('options.json') as json_file:
                options = json.load(json_file)

            return options['notify_email'],options['notify_password'],options['notify_stmp_server']
    else:
            notify_stmp_server = input("Tell me your email server: ")
            notify_email = input("Tell me your email: ")
            notify_password = input("Tell me your email password: ")

            options = {
                'notify_email': notify_email,
                'notify_password': notify_password,
                'notify_stmp_server': notify_stmp_server
            }

            with open('options.json', 'w') as outfile:
                json.dump(options, outfile)

            logging.info("Options saved succesfully!")

            return options['notify_email'],options['notify_password'],options['notify_stmp_server']

#Get local ip of the server.
def get_local_ip():
    import socket
    """Try to determine the local IP address of the machine."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Use Google Public DNS server to determine own IP
        sock.connect(('8.8.8.8', 80))

        return sock.getsockname()[0]
    except socket.error:
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            return '127.0.0.1'
    finally:
        sock.close() 