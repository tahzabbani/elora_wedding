from flask import Flask, render_template, redirect, jsonify, request, flash
from flask.helpers import url_for
import gspread
import string
import logging
import os

logging.basicConfig(filename='application.log', level=logging.INFO)
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
# forgot what this was for? and need to 
# see how to set this outside of this file
app.config['SECRET_KEY'] = "f3cfe9ed8fae309f02079dbf"

# sheets init
gc = gspread.service_account("credentials.json")
sh = gc.open("FKER RSVP")
worksheet = sh.get_worksheet(0)

# the values were being filled in random 
# cells in the server, so this is the solution
spread_dict = {"vac":"A", "reason-ta":"B", "fname":"C", "lname":"D", "other-names":"E", "email":"F", "mehndi-choice":"G", "recep-choice":"H", "fast-food":"I", "comments":"J"}


# this is for making sure the style updates every time
# that there's a reload, it adds a timestamp to the style.css
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

def get_next_avail_row():
    row_number = len(worksheet.col_values(1)) + 1
    return row_number

def get_column(key):
    return spread_dict[key]

def fill_row(dict_form):
    filled = False
    avail_row = get_next_avail_row()
    for key in dict_form.keys():
        if (worksheet.update((get_column(key) + "{}").format(avail_row), dict_form[key])):
            logging.info("here is the letter:" + str(get_column(key)) + " and value:" + dict_form[key])
            filled = True
    return filled

# TODO:
# make bool function for adding to sheets
# then if it returns true then display a new html page with success
# if it fails then put some error message
@app.route('/rsvp-form', methods=["POST"])
def form():
    if request.method == "POST":
        req = request.form
        logging.info(req)
        # getting converted to list because of generator error
        if (fill_row(req)):
            flash("congrats")
            return redirect('/success')
        else:
            flash("sorry")
            return redirect('/rsvp')
 
    return "yay"

@app.route('/')
def entry():
    return redirect('/home')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/events')
def nikkah():
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



get_next_avail_row()

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
