# -*- coding: utf-8 -*-
"""
Created on Fri May  2 21:10:00 2025

@author: Miguel
"""

from flask import Flask, render_template, request, session
from classes.agent import Agent
from classes.ticket import Ticket
from classes.solution import Solution
from classes.ticket_assignment import TicketAssignment
from datafile import filename

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'


class_map = {
    "Agent": Agent,
    "Ticket": Ticket,
    "Solution": Solution,
    "TicketAssignment": TicketAssignment
}

for cls in class_map.values():
    cls.read(filename)

prev_option = ""

@app.route("/", methods=["POST", "GET"])
def index():
    global prev_option
    butshow, butedit = "enabled", "disabled"

    option = request.form.get("option") or request.args.get("option")
    classname = request.form.get("classname") or request.args.get("classname") or "Ticket"

    class_obj = class_map.get(classname)
    if not class_obj:
        return "Classe não encontrada!", 400

    if option == "edit":
        butshow, butedit = "disabled", "enabled"
    elif option == "delete":
        obj = class_obj.current()
        if obj:
            class_obj.remove(getattr(obj, class_obj.att[0]))
            if not class_obj.previous():
                class_obj.first()
    elif option == "insert":
        butshow, butedit = "disabled", "enabled"
    elif option == "cancel":
        pass
    elif prev_option == 'insert' and option == 'save':
        new_id = class_obj.get_id(0)
        values = [request.form.get(attr, '') for attr in class_obj.att[1:]]
        strobj = str(new_id) + ';' + ';'.join(values)
        obj = class_obj.from_string(strobj)
        class_obj.insert(getattr(obj, class_obj.att[0]))
        class_obj.last()
    elif option == 'edit' and prev_option == 'save':
        obj = class_obj.current()
        for attr in class_obj.att[1:]:
            setattr(obj, attr, request.form.get(attr, ''))
        class_obj.update(getattr(obj, class_obj.att[0]))
    elif option == "first":
        class_obj.first()
    elif option == "previous":
        class_obj.previous()
    elif option == "next":
        class_obj.nextrec()
    elif option == "last":
        class_obj.last()
    elif option == 'exit':
        return "<h1>Obrigado por usar este app</h1>"

    prev_option = option
    obj = class_obj.current()

    data = {}
    if obj:
        for attr in class_obj.att:
            data[attr] = getattr(obj, attr)
    else:
        for attr in class_obj.att:
            data[attr] = ""

    return render_template(f"{classname.lower()}.html",
                           butshow=butshow, butedit=butedit,
                           data=data, classname=classname,
                           ulogin=session.get("user"))

if __name__ == '__main__':
    app.run(debug=True)
