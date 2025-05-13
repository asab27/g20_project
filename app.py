# -*- coding: utf-8 -*-
"""
Created on Fri May  2 21:10:00 2025

@author: Miguel
"""
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
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

def plot_to_img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route("/analytics")
def analytics():
    ulogin = session.get("user")

    con = sqlite3.connect('data/tech_support.db')

    # Tickets
    tickets_df = pd.read_sql_query("SELECT * FROM Ticket", con)
    tickets_df['submission_date'] = pd.to_datetime(tickets_df['submission_date'], errors='coerce')

    # Status
    status_counts = tickets_df['status'].value_counts()
    status_counts_dict = status_counts.to_dict()

    # Mês
    monthly = tickets_df.dropna(subset=['submission_date'])
    monthly_counts = (
        monthly
        .groupby(monthly['submission_date'].dt.to_period('M'))
        .size()
        .to_dict()
    )

    # Tempo médio de resolução
    assign_df = pd.read_sql_query("SELECT * FROM TicketAssignment", con)
    avg_resolution_time = assign_df['resolution_time'].mean()
    con.close()

    # Gerar gráficos
    fig1, ax1 = plt.subplots()
    status_counts.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title("Tickets por Status")
    ax1.set_xlabel("Status")
    ax1.set_ylabel("Contagem")
    img_status = plot_to_img(fig1)
    plt.close(fig1)

    fig2, ax2 = plt.subplots()
    pd.Series(monthly_counts).sort_index().plot(kind='line', marker='o', ax=ax2)
    ax2.set_title("Tickets por Mês")
    ax2.set_xlabel("Mês")
    ax2.set_ylabel("Total")
    img_monthly = plot_to_img(fig2)
    plt.close(fig2)

    return render_template(
        "analytics.html",
        ulogin=ulogin,
        status_counts=status_counts_dict,
        monthly_counts=monthly_counts,
        avg_resolution_time=round(avg_resolution_time, 2) if not pd.isna(avg_resolution_time) else None,
        img_status=img_status,
        img_monthly=img_monthly
    )

if __name__ == "__main__":
    app.run()
