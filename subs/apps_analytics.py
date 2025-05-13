# -*- coding: utf-8 -*-
"""
Created on Tue May 13 16:50:24 2025

@author: Miguel
"""
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
from flask import render_template, session
from datafile import filename
def plot_to_img(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def app_analytics():
    ulogin = session.get("user")

    con = sqlite3.connect(filename)

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