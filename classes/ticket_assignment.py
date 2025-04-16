# -*- coding: utf-8 -*-

from .gclass import Gclass

class TicketAssignment(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['ticket_id', 'agent_id', 'assignment_date', 'resolution_time']
    header = 'Ticket Assignment'
    primary_keys = ['ticket_id', 'agent_id']
    def __init__(self, ticket_id=0, agent_id=0, assignment_date='', resolution_time=0):
        key = f'{ticket_id}_{agent_id}'
        if key in TicketAssignment.obj:
            return 
        super().__init__()
        self.ticket_id = int(ticket_id)
        self.agent_id = int(agent_id)
        self.assignment_date = assignment_date
        self.resolution_time = int(resolution_time)
        TicketAssignment.obj[key] = self
        TicketAssignment.lst.append(key)
