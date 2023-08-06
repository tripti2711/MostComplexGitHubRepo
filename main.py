#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request
from utils.backend import repository_complexity_evaluation
from utils.gpt import generate_gpt_response
from langchain.langchain import LangChain

app = Flask(__name__, template_folder = 'templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the GitHub url from the form data
    github_url = request.form['githubUrl']

    try:
        # Fetch user repositories
        most_complex_repo, score, reason = repository_complexity_evaluation(github_url)
        print(most_complex_repo,score,reason)
        return render_template('result.html', repository=most_complex_repo, score=score, reason=reason)

    except Exception as e:
        print('error occurred')

if __name__ == '__main__':
    app.run(debug=True)
