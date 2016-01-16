# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:30:08 2015
@author: BD

The main script to run the Online Tweets App.
"""

from flask import Flask, render_template, request, redirect
app = Flask(__name__)

import scrape  # My own
import markov # My own

app.vars = {}

@app.route("/", methods=["GET", "POST"])
def redirecting():
    return redirect("/main")
   
@app.route("/main", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("form.html")
    else:
        # request was a POST
        app.vars["a1_first_name"] = request.form['a1_first_name']
        app.vars["a1_last_name"] = request.form['a1_last_name']
        app.vars["a2_first_name"] = request.form['a2_first_name']
        app.vars["a2_last_name"] = request.form['a2_last_name'] # In unicode
        return redirect("/graph")        

@app.route("/graph", methods=["GET", "POST"])
def graph():     
    """GET TITLES
    """
    A1F = app.vars["a1_first_name"]
    A1L = app.vars["a1_last_name"]
    A2F = app.vars["a2_first_name"]
    A2L = app.vars["a2_last_name"]
    
    titles_A1 = scrape.get_titles_by_author(A1L + "+" + A2F) # List of strings
    titles_A2 = scrape.get_titles_by_author(A2L + "+" + A2F) # List of strings
    titles_combined = titles_A1 + titles_A2    
    titles_generated = markov.markov_function(titles_combined) # List of strings  
        
    """RENDER TEMPLATE
    """
    def show_x(my_list):
        length = 3
        if len(my_list) <= length:
            return my_list
        else:
            return my_list[0:length] 
        
    titles_A1 = show_x(titles_A1)
    titles_A2 = show_x(titles_A2)
            
    return render_template("graph.html",
                           titles1=titles_A1,
                           titles2=titles_A2,
                           titles3=titles_generated,
                           a1first=A1F, a1last=A1L,
                           a2first=A2F, a2last=A2L)

if __name__ == "__main__":
    app.run(debug=True)
