import logging
import time
import os
import secrets
import threading
import requests
import socket

from datetime import datetime

from utils import check,write_data,find_data,get_options,get_local_ip
from flask_mail import Mail, Message
from flask import Flask, jsonify, flash, request, send_file

app = Flask(__name__)

app.config.from_object(__name__)

secret = secrets.token_urlsafe(32)

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

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

current_tracking_codes = {}

def get_my_ip():
    return request.remote_addr

def send_on_open_email(sender, receiver, ip, tracking_code):
    try:
        msg = Message(f"{receiver} has opened the email",
          sender=notify_email,
          recipients=[sender])

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")

        msg.body = f"{receiver} opened the email just now from IP: {ip} at {current_time}\n\n'Sent by PyTrack'"           
        
        mail.send(msg)

        app.logger.warning('Mail sent!')

        del current_tracking_codes[tracking_code]

    except Exception as e:
        print(e)
        app.logger.warning(e)


@app.route("/image", methods=["GET"])
def render_image():
    app.logger.warning('User has opened email.')
    
    tracking_code = int(request.args.get('tracking_code'))
    
    app.logger.warning(tracking_code)
    ip = get_my_ip()

    my_ip = get_local_ip()
    print(my_ip,ip)
    
    #my_ip = requests.get('https://checkip.amazonaws.com').text.strip()
    if ip != my_ip:
        if tracking_code in current_tracking_codes:
            
            sender = current_tracking_codes[tracking_code][0]
            receiver = current_tracking_codes[tracking_code][1]
            send_on_open_email(sender, receiver,ip,tracking_code)
        else: 
            found,row = find_data(tracking_code)
            if found:
                print(row)
        return send_file('sprites/pi.png', mimetype='image/gif')
    else:
        print("receiver is the sender")
    return ""
  



def create_tracking_code():
    return str(int(time.time()%99999))
    
@app.route("/get_tracking_code_for_email")
def get_tracking_code_for_email():
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')

    #this part creates a random tracking code for current email and returns the html code to inject on the email.
    if sender and receiver:
        if check(sender) and check(receiver): 
            tracking_code = create_tracking_code()
            
            logging.warning(f'{sender}, {receiver}')
            
            url = request.url_root

            html_code = f'<img src={url}image?tracking_code={tracking_code}></img>'   

            write_data(sender, receiver, tracking_code)

            current_tracking_codes[int(tracking_code)]=[sender, receiver]
            
            app.logger.warning("Current tracking code: " + tracking_code)

            return jsonify(status_code="200",
                    inject_code=html_code)
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
