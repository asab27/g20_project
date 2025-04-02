# -*- coding: utf-8 -*-

class Ticket:
    def __init__(self, ticket_id, issue, submission_date, status):
        self.ticket_id = ticket_id
        self.issue = issue
        self.submission_date = submission_date
        self.status = status

    def __repr__(self):
        return f"Ticket({self.ticket_id}, {self.issue}, {self.submission_date}, {self.status})"
