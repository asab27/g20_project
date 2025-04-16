# -*- coding: utf-8 -*-

from .gclass import Gclass

class Ticket(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['ticket_id', 'issue', 'submission_date', 'status']
    header = 'Ticket'
    def __init__(self, ticket_id=0, issue='', submission_date='', status=''):
        ticket_id = Ticket.get_id(ticket_id)
        if ticket_id in Ticket.obj:
            return
        super().__init__()
        self.ticket_id = int(ticket_id)
        self.issue = issue
        self.submission_date = submission_date
        self.status = status
        Ticket.obj[self.ticket_id] = self
        Ticket.lst.append(self.ticket_id)

