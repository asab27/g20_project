# -*- coding: utf-8 -*-
"""
Created on Mon May 12 17:16:01 2025

@author: Miguel
"""
from flask import render_template, request, session
from classes.ticket import Ticket


prev_option = ""

def apps_ticket():
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
        obj = Ticket.current()
        if obj:
            Ticket.remove(obj.ticket_id)
            if not Ticket.previous():
                Ticket.first()

    elif option == "insert":
        butshow = "disabled"
        butedit = "enabled"

    elif option == "cancel":
        pass

    elif prev_option == "insert" and option == "save":
        values = [request.form.get(attr, "") for attr in Ticket.att[1:]]
        str_obj = str(Ticket.get_id(0)) + ";" + ";".join(values)
        obj = Ticket.from_string(str_obj)
        Ticket.insert(obj.ticket_id)
        Ticket.last()

    elif prev_option == "edit" and option == "save":
        obj = Ticket.current()
        for attr in Ticket.att[1:]:
            setattr(obj, attr, request.form.get(attr, ""))
        Ticket.update(obj.ticket_id)

    elif option == "first":
        Ticket.first()
    elif option == "previous":
        Ticket.previous()
    elif option == "next":
        Ticket.nextrec()
    elif option == "last":
        Ticket.last()
    

    prev_option = option
    obj = Ticket.current()
    data = {attr: getattr(obj, attr, "") for attr in Ticket.att} if obj else {attr: "" for attr in Ticket.att}

    return render_template("ticket.html", butshow=butshow, butedit=butedit, data=data,
                           classname="Ticket", ulogin=ulogin, msg=msg)
