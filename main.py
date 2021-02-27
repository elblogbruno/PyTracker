import logging
import os
import secrets
import threading
import requests
import socket
import sys


from db.database import *
from datetime import datetime
from utils import *
from email_utils import *
from flask_mail import Mail, Message
from flask import Flask, jsonify, flash, request, send_file,render_template

app = Flask(__name__)
database = EmailDatabase()
app.config.from_object(__name__)

secret = secrets.token_urlsafe(32)

file_handler = logging.FileHandler(filename='app.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('LOGGER_NAME')

app.secret_key = secret
notify_email,notify_password,notify_stmp_server = get_options(logging)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER=notify_stmp_server,
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = notify_email,
	MAIL_PASSWORD = notify_password
)

mail = Mail(app)

def get_my_ip():
    return request.remote_addr

def send_on_open_email(sender, receiver, ip, tracking_code,counter):
    try:
        
        msg = Message(f"PyTracker - {receiver} has opened the email.",
          sender=notify_email,
          recipients=[sender])

        current_time = datetime.now().strftime("%H:%M:%S")

        msg.html = render_template(modify_current_html_email(receiver,ip,current_time,counter))
        
        mail.send(msg)

        app.logger.warning('Mail sent!')

    except Exception as e:
        print(e)
        app.logger.warning(e)


@app.route("/add_data")
def add_data():
     return database.add_sample_data()
     

@app.route("/get_data")
def get_data():
     return database.get_data()

@app.route("/")
def show_settings_home_menu():
     return render_template(get_current_html_template())

def process_row(row,tracking_code,ip):
    counter = int(row[2])
    print("The counter is : " +  str(counter))
    
    if counter > 1:  
        sender = row[0]
        receiver = row[1]
        send_on_open_email(sender, receiver,ip,tracking_code,counter)
    else:
        print("Receiver is the sender as the counter is 1: " +  str(row[2]))

@app.route("/image", methods=["GET"])
def render_image():
    tracking_code = int(request.args.get('tracking_code'))

    app.logger.warning("Someone has opened the email with this tracking code {}".format(tracking_code))
    
    ip = get_my_ip()
    my_ip = get_local_ip()

    app.logger.info("PyTracker server IP is {0} and receiver ip is {1}".format(my_ip,ip))
    
    if str(ip) != str(my_ip):
        app.logger.info("Searching for tracking_code {0} in csv file".format(tracking_code))
        
        found,row = database.find_row_by_tracking_code(tracking_code)
        
        if found:
            app.logger.warning("Tracking code {} was found".format(tracking_code))
            process_row(row,tracking_code,ip)
        else:
            app.logger.warning("Tracking code {} is lost and can't be tracked".format(tracking_code))

        return send_file('sprites/pi.png', mimetype='image/gif')
    else:
        app.logger.warning("Receiver is the sender as they have the same IP")
    return send_file('sprites/pi.png', mimetype='image/gif')
  



    
@app.route("/get_tracking_code_for_email")
def get_tracking_code_for_email():
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')

    #this part creates a random tracking code for current email and returns the html code to inject on the email.
    if sender and receiver:
        if check(sender) and check(receiver): 
            app.logger.warning("Creating tracking code for {0} and {1}".format(sender,receiver))
            
            tracking_code = create_tracking_code() #Creates tracking code for current email.
            
            logging.warning(f'{sender}, {receiver}')
            
            url = request.url_root

            html_code = f'<img src={url}image?tracking_code={tracking_code}></img>'   

            database.write_data(sender, receiver, 0,tracking_code) #writes the data so it can be recall in the future if server has been shutdown for example.
            
            app.logger.warning("Current tracking code: " + tracking_code)

            return jsonify(status_code="200",
                    inject_code=html_code,tracking_code=tracking_code)
        else:
            return jsonify(status_code="500")
    else:
        return jsonify(status_code="404")

if __name__ == "__main__":
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host="0.0.0.0", port=port) 
    except:
        logging.exception('error')
