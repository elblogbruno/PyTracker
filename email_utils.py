
def modify_current_html_email(receiver,ip,current_time,open_counter):
    message = f"{receiver} has opened the email just now from IP: {ip} at {current_time}"

    if open_counter > 1:
        message = f"{receiver} has opened the email again from IP: {ip} at {current_time}"


    # Read in the file
    with open("templates/email-inlined.html", 'r') as file :
        filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('{message}', message)

     # Write the file out again
    with open("templates/email-inlined.html", 'w') as file:
        file.write(filedata)

    return get_current_html_template()


def get_current_html_template():
    return "email-inlined.html"