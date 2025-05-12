# -*- coding: utf-8 -*-
"""
Created on Mon May 12 17:27:14 2025

@author: Miguel
"""
from flask import render_template, request, session
from classes.solution import Solution

prev_option = ""

def apps_solution():
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
        obj = Solution.current()
        if obj:
            Solution.remove(obj.solution_id)
            if not Solution.previous():
                Solution.first()

    elif option == "insert":
        butshow = "disabled"
        butedit = "enabled"

    elif option == "cancel":
        pass

    elif prev_option == "insert" and option == "save":
        values = [request.form.get(attr, "") for attr in Solution.att[1:]]
        str_obj = str(Solution.get_id(0)) + ";" + ";".join(values)
        obj = Solution.from_string(str_obj)
        Solution.insert(obj.solution_id)
        Solution.last()

    elif prev_option == "edit" and option == "save":
        obj = Solution.current()
        for attr in Solution.att[1:]:
            setattr(obj, attr, request.form.get(attr, ""))
        Solution.update(obj.solution_id)

    elif option == "first":
        Solution.first()
    elif option == "previous":
        Solution.previous()
    elif option == "next":
        Solution.nextrec()
    elif option == "last":
        Solution.last()
    elif option == "exit":
        return render_template("index.html", ulogin=ulogin)

    prev_option = option
    obj = Solution.current()
    data = {attr: getattr(obj, attr, "") for attr in Solution.att} if obj else {attr: "" for attr in Solution.att}

    return render_template("solution.html", butshow=butshow, butedit=butedit, data=data,
                           classname="Solution", ulogin=ulogin, msg=msg)
