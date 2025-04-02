# -*- coding: utf-8 -*-


import sqlite3

def create_database():
    conn = sqlite3.connect("data/tech_support.db")  
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Ticket (
                        ticket_id INTEGER PRIMARY KEY,
                        issue TEXT,
                        submission_date TEXT,
                        status TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Agent (
                        agent_id INTEGER PRIMARY KEY,
                        name TEXT,
                        department TEXT,
                        email TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS TicketAssignment (
                        ticket_id INTEGER,
                        agent_id INTEGER,
                        assignment_date TEXT,
                        resolution_time INTEGER,
                        FOREIGN KEY(ticket_id) REFERENCES Ticket(ticket_id),
                        FOREIGN KEY(agent_id) REFERENCES Agent(agent_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Solution (
                        solution_id INTEGER PRIMARY KEY,
                        ticket_id INTEGER UNIQUE,
                        resolution_summary TEXT,
                        solved_date TEXT,
                        FOREIGN KEY(ticket_id) REFERENCES Ticket(ticket_id))''')

    conn.commit()
    conn.close()
    print("Base de dados e tabelas criadas com sucesso.")

if __name__ == "__main__":
    create_database()
