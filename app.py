from flask import Flask, render_template, redirect, jsonify, request, flash
from flask.helpers import url_for
from flask.templating import render_template_string
from sendgrid.helpers.mail import Mail, Email, To, Content
import sendgrid
import config
import gspread
import string
import logging
import os

logging.basicConfig(filename='application.log', level=logging.INFO)
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = config.secret_key

# sheets init
gc = gspread.service_account("credentials.json")
sh = gc.open("FKER RSVP")
worksheet = sh.get_worksheet(0)

# the values were being filled in random 
# cells in the server, so this is the solution
spread_dict = {"vac":"A", "reason-ta":"B", "fname":"C", "lname":"D", "num_others": "E", "other-names":"F", "email":"G", "phone":"H", "mehndi-choice":"I", "recep-choice":"J", "fast-food":"K", "comments":"L"}

yes_content = "Hello!\n\nWe are so excited to be able to celebrate this special occasion with you! We've saved you a seat - please feel free to contact us at ejrobbani@gmail.com if you have any questions or if anything changes.\n\nCan't wait to see you in March!\n\nFahad & Elora"
no_content = "Hello!\n\nWe wish you were able to celebrate with us, but we completely understand and hope to still have your warm wishes for the future!\n\nPlease feel free to contact us at ejrobbani@gmail.com if you have any questions or if anything changes.\n\nFahad & Elora"

# this is for making sure the static files update every time
# that there's a reload, it adds a timestamp to the files
#########################
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
#########################

def check_duplicate(email):
    list_of_emails = worksheet.col_values(7)
    for sheet_email in list_of_emails:
        if email.lower().strip() == sheet_email.lower().strip():
            return False
    return True

def get_next_avail_row():
    row_number = len(worksheet.col_values(1)) + 1
    return row_number

def get_column(key):
    return spread_dict[key]

def fill_row(dict_form):
    filled = False
    # set num to integer for google sheet
    num_to_int = 0
    avail_row = get_next_avail_row()
    for key in dict_form.keys():
        if (get_column(key) == 'E'):
            num_to_int = dict_form[key]
            worksheet.update((get_column(key) + "{}").format(avail_row), int(num_to_int))
            filled = True
        elif (get_column(key) != 'E' and worksheet.update((get_column(key) + "{}").format(avail_row), dict_form[key])):
            logging.info("here is the letter:" + str(get_column(key)) + " and value:" + dict_form[key])
            filled = True
    return filled

def send_email(email, req):
    sg = sendgrid.SendGridAPIClient(api_key=config.sendgridkey)
    from_email = Email("noreply@fahadandelora.com")
    to_email = To(email)
    if (req['mehndi-choice'] == 'no' and req['recep-choice'] == 'no'):
        content = Content("text/plain", no_content)
    else:
        content = Content("text/plain", yes_content)
    subject = "Thanks for your RSVP"
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
    

@app.route('/rsvp-form', methods=["POST"])
def form():
    if request.method == "POST":
        req = request.form
        logging.info(req)
        if (check_duplicate(req['email']) == False):
            return redirect('/duplicate_email')
        # getting converted to list because of generator error
        if (fill_row(req)):
            # send email to email address in form
            send_email(req['email'], req)
            return redirect('/success')
        else:
            return redirect('/failure')
    return "yay"

@app.route('/')
def entry():
    return redirect('/home')

@app.route('/conf_fail')
def conf_fail():
    return render_template('conf_fail.html')

@app.route('/duplicate_email')
def duplicate_email():
    return render_template('duplicate_email.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/accommodations')
def accommodations():
    return render_template('accommodations.html')

@app.route('/rsvp')
def rsvp():
    return render_template('rsvp.html')

@app.route('/registry')
def registry():
    return render_template('registry.html')

@app.route('/pics')
def pics():
    return render_template('pics.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

get_next_avail_row()

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
