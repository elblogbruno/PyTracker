from email_validator import validate_email, EmailNotValidError
import csv
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

def write_data(name, email, url):
    with open('data.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, email, url])
