# -*- coding: utf-8 -*-


class Solution:
    def __init__(self, solution_id, ticket_id, resolution_summary, solved_date):
        self.solution_id = solution_id
        self.ticket_id = ticket_id
        self.resolution_summary = resolution_summary
        self.solved_date = solved_date

    def __repr__(self):
        return f"Solution({self.solution_id}, {self.ticket_id}, {self.resolution_summary}, {self.solved_date})"

