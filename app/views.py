from flask import Flask, render_template, redirect, jsonify, request
import gspread
from app import app

# def add_to_sheet()


@app.route('/')
def entry():
    return redirect('/home')

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