# -*- coding: utf-8 -*-
"""
Created on Fri May  2 21:10:00 2025

@author: Miguel
"""
from flask import Flask, render_template, request, session
from datafile import filename
from classes.ticket import Ticket
from classes.agent import Agent
from classes.solution import Solution
from classes.ticket_assignment import TicketAssignment
from classes.userlogin import Userlogin

from subs.apps_userlogin import apps_userlogin
from subs.apps_ticket import apps_ticket
from subs.apps_agent import apps_agent
from subs.apps_solution import apps_solution
from subs.apps_ticketassignment import apps_ticketassignment
from subs.apps_analytics import app_analytics

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# Carregar dados
Ticket.read(filename)
Agent.read(filename)
Solution.read(filename)
TicketAssignment.read(filename)
Userlogin.read(filename)

# Helper para obter o grupo do user
def get_user_group():
    ulogin = session.get("user")
    group = None
    if ulogin:
        user_id = Userlogin.get_user_id(ulogin)
        if user_id in Userlogin.obj:
            group = Userlogin.obj[user_id].usergroup
    return group

# Página inicial
@app.route("/")
def index():
    ulogin = session.get("user")
    group = get_user_group()
    return render_template("index.html", ulogin=ulogin, group=group, page_class="index-background")

# Login
@app.route("/login")
def login():
    return render_template("login.html", user="", password="", ulogin=session.get("user"), resul="", group=None)

@app.route("/logoff")
def logoff():
    session.pop("user", None)
    return render_template("index.html", ulogin=None, group=None)

@app.route("/chklogin", methods=["POST", "GET"])
def chklogin():
    user = request.form["user"]
    password = request.form["password"]
    resul = Userlogin.chk_password(user, password)
    if resul == "Valid":
        session["user"] = user
        group = get_user_group()
        return render_template("index.html", ulogin=user, group=group)
    return render_template("login.html", user=user, password=password, ulogin=None, resul=resul, group=None)

# Subapps
@app.route("/Userlogin", methods=["POST", "GET"])
def userlogin():
    return apps_userlogin()

@app.route("/Ticket", methods=["POST", "GET"])
def ticket():
    return apps_ticket()

@app.route("/Agent", methods=["POST", "GET"])
def agent():
    return apps_agent()

@app.route("/Solution", methods=["POST", "GET"])
def solution():
    return apps_solution()

@app.route("/TicketAssignment", methods=["POST", "GET"])
def ticket_assignment():
    return apps_ticketassignment()

@app.route("/analytics")
def analytics():
    return app_analytics()

if __name__ == "__main__":
    app.run()
