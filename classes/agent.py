# -*- coding: utf-8 -*-


from .gclass import Gclass

class Agent(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['agent_id', 'name', 'department', 'email']
    header = 'Agent'
    def __init__(self, agent_id=0, name='', department='', email=''):
        agent_id = Agent.get_id(agent_id)
        if agent_id in Agent.obj:
           return
        super().__init__()
        self.agent_id = int(agent_id)
        self.name = name
        self.department = department
        self.email = email
        Agent.obj[self.agent_id] = self
        Agent.lst.append(self.agent_id)
