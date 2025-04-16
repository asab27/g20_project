# -*- coding: utf-8 -*-


from .gclass import Gclass

class Solution(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['solution_id', 'ticket_id', 'resolution_summary', 'solved_date']
    header = 'Solution'
    def __init__(self, solution_id=0, ticket_id=0, resolution_summary='', solved_date=''):
        solution_id = Solution.get_id(solution_id)
        if solution_id in Solution.obj:
            return
        super().__init__()
        self.solution_id = int(solution_id)
        self.ticket_id = int(ticket_id)
        self.resolution_summary = resolution_summary
        self.solved_date = solved_date
        Solution.obj[self.solution_id] = self
        Solution.lst.append(self.solution_id)
