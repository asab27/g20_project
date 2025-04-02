# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 17:24:16 2025

@author: Miguel
"""

from classes.ticket import Ticket
from classes.agent import Agent
from classes.ticket_assignment import TicketAssignment
from classes.solution import Solution

def test_ticket():
    ticket = Ticket(1, "Problema na rede", "2025-03-01", "Open")
    assert ticket.ticket_id == 1
    assert ticket.issue == "Problema na rede"
    assert ticket.submission_date == "2025-03-01"
    assert ticket.status == "Open"
    print("Teste Ticket passou!")


def test_agent():
    agent = Agent(101, "Carlos Silva", "Suporte Técnico", "carlos@email.com")
    assert agent.agent_id == 101
    assert agent.name == "Carlos Silva"
    assert agent.department == "Suporte Técnico"
    assert agent.email == "carlos@email.com"
    print("Teste Agent passou!")


def test_ticket_assignment():
    assignment = TicketAssignment(1, 101, "2025-03-02", 30)
    assert assignment.ticket_id == 1
    assert assignment.agent_id == 101
    assert assignment.assignment_date == "2025-03-02"
    assert assignment.resolution_time == 30
    print("Teste TicketAssignment passou!")


def test_solution():
    solution = Solution(501, 1, "Reiniciar o router resolveu o problema", "2025-03-03")
    assert solution.solution_id == 501
    assert solution.ticket_id == 1
    assert solution.resolution_summary == "Reiniciar o router resolveu o problema"
    assert solution.solved_date == "2025-03-03"
    print("Teste Solution passou!")


if __name__ == "__main__":
    test_ticket()
    test_agent()
    test_ticket_assignment()
    test_solution()
    print("Todos os testes passaram com sucesso!")
