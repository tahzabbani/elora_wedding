from flask import Flask, render_template, redirect, jsonify, request
from app import app

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
def nikkah():
    return render_template('mehndi.html')

@app.route('/reception')
def nikkah():
    return render_template('reception.html')

@app.route('/rsvp')
def nikkah():
    return render_template('rsvp.html')

@app.route('/registry')
def nikkah():
    return render_template('registry.html')