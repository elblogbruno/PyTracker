# PyTracker

This is a very basic mail tracking service which I developed for my personal use and it is motivated by https://github.com/prashantsengar/mTracker created by Prashant Sengar.

It consist of a python server and a work in progress outlook plugin that contacts the server and adds a tracking code to the email, so you know when someone has oppened it!


## How to use it:

You are welcome to contribute to this repository. Get started with the following steps:

- Clone the repo

`git clone https://github.com/elblogbruno/PyTracker.git`

- Install the requirements

 `pip install -r requirements.txt`

- Edit the email address, password, SMPT address and port in the main.py file, this is the email that will sent you notifications when user has oppened the email.

- Now you are good to go. Run the main file

`python main.py` or `python3 main.py`

The flask app will run on localhost.

By the moment you can call this url for example  (changing sender and receiver for the corresponding email)

http://localhost:5000/get_tracking_code_for_email?sender=[sender]&receiver=[receiver]

which will get you the code you need to inject on the email.

if your email is "example@example.com" you are the sender, and then for example "example1@gmail.com" is the receiver you want to track if he opoens the email, the url will be:


http://localhost:5000/get_tracking_code_for_email?sender=example@example.com&receiver=example1@gmail.com


I want this to be done automatically by the plugin in the near future.

## To-do

There's a lot to do here. Everyone is welcome to make it better.

- [ ] Make chrome extension that works for
  
  - [ ] Gmail

  - [ ] Hotmail

  - [ ] Yahoo mail

- [ ] Others

  - [ ] Outlook

