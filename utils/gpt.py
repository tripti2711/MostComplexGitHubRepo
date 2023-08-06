#!/usr/bin/env python
# coding: utf-8


import openai
import re

def generate_gpt_response(prompt):
    # Set up OpenAI API credentials
    openai.api_key = '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'
    
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0.8
    )
    
    if 'choices' in response and len(response.choices) > 0:
        score, reason = info_extractor(response.choices[0]['message']['content'])
        return score, reason
    else:
        raise Exception("Failed to generate GPT response.")

def info_extractor(text):
    lines = text.split('\n')
    score_line = lines[0].strip()
    score_match = re.search(r'\d+', score_line)
    if score_match:
        score = int(score_match.group())
    else:
        score = 0

    # Remove the first line to get the reason
    reason = '\n'.join(lines[1:]).strip()

    return score, reason

