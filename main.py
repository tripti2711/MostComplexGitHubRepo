#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request
from utils.backend import repository_complexity_evaluation
from utils.gpt import generate_gpt_response

app = Flask(__name__, template_folder = 'templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the GitHub username from the form data
    username = request.form['username']

    try:
        # Fetch user repositories
        most_complex_repo, reason = repository_complexity_evaluation(username)
        print(most_complex_repo,reason)
        return render_template('result.html', repository=most_complex_repo, reason=reason)

    except Exception as e:
        print('error occurred')

if __name__ == '__main__':
    app.run(debug=True)
