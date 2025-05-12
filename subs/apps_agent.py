# -*- coding: utf-8 -*-
"""
Created on Mon May 12 17:26:16 2025

@author: Miguel
"""
from flask import render_template, request, session
from classes.agent import Agent

prev_option = ""

def apps_agent():
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
        obj = Agent.current()
        if obj:
            Agent.remove(obj.agent_id)
            if not Agent.previous():
                Agent.first()

    elif option == "insert":
        butshow = "disabled"
        butedit = "enabled"

    elif option == "cancel":
        pass

    elif prev_option == "insert" and option == "save":
        values = [request.form.get(attr, "") for attr in Agent.att[1:]]
        str_obj = str(Agent.get_id(0)) + ";" + ";".join(values)
        obj = Agent.from_string(str_obj)
        Agent.insert(obj.agent_id)
        Agent.last()

    elif prev_option == "edit" and option == "save":
        obj = Agent.current()
        for attr in Agent.att[1:]:
            setattr(obj, attr, request.form.get(attr, ""))
        Agent.update(obj.agent_id)

    elif option == "first":
        Agent.first()
    elif option == "previous":
        Agent.previous()
    elif option == "next":
        Agent.nextrec()
    elif option == "last":
        Agent.last()
    elif option == "exit":
        return render_template("index.html", ulogin=ulogin)

    prev_option = option
    obj = Agent.current()
    data = {attr: getattr(obj, attr, "") for attr in Agent.att} if obj else {attr: "" for attr in Agent.att}

    return render_template("agent.html", butshow=butshow, butedit=butedit, data=data,
                           classname="Agent", ulogin=ulogin, msg=msg)
