from flask import Flask, render_template, redirect, jsonify, request, flash
from flask.helpers import url_for
import gspread

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = "f3cfe9ed8fae309f02079dbf"

# sheets init
gc = gspread.service_account("credentials.json")
sh = gc.open("FKER RSVP")
worksheet = sh.get_worksheet(0)

def get_next_avail_row():
    row_number = len(worksheet.col_values(1)) + 1
    return row_number

# def fill_row():


# TODO:
# make bool function for adding to sheets
# then if it returns true then display a new html page with success
# if it fails then put some error message
@app.route('/rsvp-form', methods=["POST"])
def form():
    if request.method == "POST":
        req = request.form
        fname = req["fname"]
        lname = req["lname"]
        other_people = req["other-names"]
        email = req["email"]
        nikkah = req["nikkah-choice"]
        mehndi = req["mehndi-choice"]
        reception = req["recep-choice"]
        if (fill_row()):
            render_template('success.html')
        else:
            flash("failed")
            return redirect('/rsvp')
        flash("congrats")
 
    return "yay"

@app.route('/')
def entry():
    return redirect('/home')

@app.route('/landing')
def landing():
    return render_template('landing.html')

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

@app.route('/accomodations')
def accomodations():
    return render_template('accomodations.html')

@app.route('/rsvp')
def rsvp():
    return render_template('rsvp.html')

@app.route('/registry')
def registry():
    return render_template('registry.html')



get_next_avail_row()

if __name__ == "__main__":
    app.run(debug=True)
