# -*- coding: utf-8 -*-
"""
Created on Mon May 12 17:28:55 2025

@author: Miguel
"""
from flask import render_template, request, session
from classes.ticket_assignment import TicketAssignment


prev_option = ""

def apps_ticketassignment():
    global prev_option
    butshow = "enabled"
    butedit = "disabled"
    msg = ""
    ulogin = session.get("user")

    if not ulogin:
        return render_template("index.html", ulogin=None)

    option = request.form.get("option") or request.args.get("option")


    if option == "edit":
        butshow = "disabled"
        butedit = "enabled"

    elif option == "delete":
        obj = TicketAssignment.current()
        if obj:
            TicketAssignment.remove(f"{obj.ticket_id}_{obj.agent_id}")
            if not TicketAssignment.previous():
                TicketAssignment.first()

    elif option == "insert":
        butshow = "disabled"
        butedit = "enabled"

    elif option == "cancel":
        pass

    elif prev_option == "insert" and option == "save":
        values = [request.form.get(attr, "") for attr in TicketAssignment.att[1:]]
        key = TicketAssignment.get_id(0)  # not ideal, but consistent
        str_obj = request.form.get("ticket_id", "0") + ";" + ";".join(values)
        obj = TicketAssignment.from_string(str_obj)
        TicketAssignment.insert(f"{obj.ticket_id}_{obj.agent_id}")
        TicketAssignment.last()

    elif prev_option == "edit" and option == "save":
        obj = TicketAssignment.current()
        for attr in TicketAssignment.att[2:]:  # skip primary keys
            setattr(obj, attr, request.form.get(attr, ""))
        TicketAssignment.update(f"{obj.ticket_id}_{obj.agent_id}")

    elif option == "first":
        TicketAssignment.first()
    elif option == "previous":
        TicketAssignment.previous()
    elif option == "next":
        TicketAssignment.nextrec()
    elif option == "last":
        TicketAssignment.last()


    prev_option = option
    obj = TicketAssignment.current()
    data = {attr: getattr(obj, attr, "") for attr in TicketAssignment.att} if obj else {attr: "" for attr in TicketAssignment.att}

    return render_template("ticketassignment.html", butshow=butshow, butedit=butedit, data=data,
                           classname="TicketAssignment", ulogin=ulogin, msg=msg)
