# -*- coding: utf-8 -*-

class TicketAssignment:
    def __init__(self, ticket_id, agent_id, assignment_date, resolution_time):
        self.ticket_id = ticket_id
        self.agent_id = agent_id
        self.assignment_date = assignment_date
        self.resolution_time = resolution_time

    def __repr__(self):
        return f"TicketAssignment({self.ticket_id}, {self.agent_id}, {self.assignment_date}, {self.resolution_time})"

