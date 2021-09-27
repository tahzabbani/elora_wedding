from flask import Flask, render_template, redirect, jsonify, request, flash
from flask.helpers import url_for
import gspread
import string

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
# forgot what this was for? and need to 
# see how to set this outside of this file
app.config['SECRET_KEY'] = "f3cfe9ed8fae309f02079dbf"

# sheets init
gc = gspread.service_account("credentials.json")
sh = gc.open("FKER RSVP")
worksheet = sh.get_worksheet(0)

def get_next_avail_row():
    row_number = len(worksheet.col_values(1)) + 1
    return row_number

def fill_row(dict_vals):
    filled = False
    avail_row = get_next_avail_row()
    for idx, i in enumerate(string.ascii_uppercase):
        worksheet.update((i + "{}").format(avail_row), dict_vals[idx])
        print(idx)
        if ((idx + 1) == len(dict_vals)):
            filled = True
            break
    return filled

# TODO:
# make bool function for adding to sheets
# then if it returns true then display a new html page with success
# if it fails then put some error message
@app.route('/rsvp-form', methods=["POST"])
def form():
    if request.method == "POST":
        req = request.form
        print(req)
        # getting converted to list because of generator error
        if (fill_row(list(req.values()))):
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

@app.route('/nikkah')
def nikkah():
    return render_template('nikkah.html')

@app.route('/mehndi')
def mehndi():
    return render_template('mehndi.html')

@app.route('/reception')
def reception():
    return render_template('reception.html')

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
    app.run(debug=True)
