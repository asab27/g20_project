# -*- coding: utf-8 -*-


class Agent:
    def __init__(self, agent_id, name, department, email):
        self.agent_id = agent_id
        self.name = name
        self.department = department
        self.email = email

    def __repr__(self):
        return f"Agent({self.agent_id}, {self.name}, {self.department}, {self.email})"
