from flask import Blueprint, render_template, redirect, url_for, request
from .search import all_commissions, check_group, search, trekkers, trekker_names
from itertools import combinations

views = Blueprint("views", __name__)

@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@views.route("/result", methods=["POST"])
def result():
    formatted_result = None
    if request.method == "POST":
        
        selected_commissions = request.form.getlist("requirements")
        required = [all_commissions[key] for key in selected_commissions]

        all_ids = {trek.ID for trek in trekkers }
        included_ids = {
            int(char_id)
            for char_id in request.form.getlist("included_chars")
        }
        nonaq_chars = all_ids - included_ids
        
        candidates = {} 
        for req in required:
            valid_groups = []
            excluded_ids = nonaq_chars 
            for group in combinations(trekkers, 3):
                if check_group(group, req, excluded_ids=excluded_ids):
                    valid_groups.append(group)
            candidates[req.name] = valid_groups
        
        result = search(required, candidates, 0, set(), {})
        if result is None:
            return render_template("result.html", error="No valid results were found")
    
        formatted_result = {
            group_name:[trekker_names[trek.ID] 
                        for trek in trekkers] 
                        for group_name, trekkers in result.items()}  # type: ignore
        
    return render_template("result.html", results=formatted_result)
