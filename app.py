from flask import Flask, render_template, redirect, jsonify, request
import gspread

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

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

@app.route('/rsvp-form', methods=["POST"])
def form():
    if request.method == "POST":
    
        req = request.form
        print(req)

        return redirect('rsvp')
    return 0


if __name__ == "__main__":
    app.run(debug=True)
