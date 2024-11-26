"""
This module summarizes the Bitcoin whitepaper using different models and
prompts. Calculates statistics on the summaries to see how effective each
prompt is.
"""

import pprint
import re

import requests
import numpy as np

import api

NUM_ITERATIONS = 5
URL = (
    "https://raw.githubusercontent.com/karask/satoshi-paper/master/bitcoin.md"
)

whitepaper = requests.get(URL, timeout=10).text

PROMPTS = [
    "Create an unordered list with 3 bullet points about the whitepaper",
    "Create an unordered list with 5 bullet points about the whitepaper",
    "Create an unordered list with 10 bullet points about the whitepaper",
    "Create an unordered list with 20 bullet points about the whitepaper",
    "Create an unordered list with 50 bullet points about the whitepaper",
    "Create an ordered list with 3 points about the whitepaper",
    "Create an ordered list with 5 points about the whitepaper", 
    "Create an ordered list with 10 points about the whitepaper",
    "Create an ordered list with 20 points about the whitepaper",
    "Create an ordered list with 50 points about the whitepaper",
]

def count_list_items(text):
    # Match different types of list formats:
    # - Bullet points (-, *, •)
    # - Numbered lists (1., 1), a., A., i., I.)
    bullet_pattern = r'(?m)^[ \t]*[-*•][ \t]'
    numbered_pattern = r'(?m)^[ \t]*(?:\d+\.|\d+\)|[a-zA-Z]\.|\([a-zA-Z]\)|[ivxIVX]+\.|\([ivxIVX]+\))[ \t]'
    
    bullet_count = len(re.findall(bullet_pattern, text))
    numbered_count = len(re.findall(numbered_pattern, text))
    
    return bullet_count + numbered_count

stats = {}
for i in range(NUM_ITERATIONS):
    print(f"Attempt {i+1}")
    for model_name in ["anthropic", "gemini", "openai"]:
        print(f"Testing model: {model_name}")
        ask_func = getattr(api, f"ask_{model_name}")
        if model_name not in stats:
            stats[model_name] = {}
        for prompt in PROMPTS:
            print(f"Testing prompt: {prompt}")
            if prompt not in stats[model_name]:
                stats[model_name][prompt] = {}
            response = ask_func(
                f"Summarize the given whitepaper:\n"
                f"{whitepaper}\n"
                f"{prompt}\n"
                f"Return only the summary, nothing else.")
            print(response)

            word_count = len(re.findall(r'\w+', response))
            list_items = count_list_items(response)
            print(f"List items: {list_items}")

            if "word_count" not in stats[model_name][prompt]:
                stats[model_name][prompt]["word_count"] = []
            if "list_items" not in stats[model_name][prompt]:
                stats[model_name][prompt]["list_items"] = []
            stats[model_name][prompt]["word_count"].append(word_count)
            stats[model_name][prompt]["list_items"].append(list_items)

for model_name, model_stats in stats.items():
    for prompt, prompt_stats in model_stats.items():
        word_counts = stats[model_name][prompt]["word_count"]
        list_counts = stats[model_name][prompt]["list_items"]
        
        # Calculate stats for word counts
        stats[model_name][prompt]["word_count_mean"] = np.mean(word_counts)
        stats[model_name][prompt]["word_count_std"] = np.std(word_counts)
        stats[model_name][prompt]["word_count_min"] = np.min(word_counts)
        stats[model_name][prompt]["word_count_max"] = np.max(word_counts)
        
        # Calculate stats for list items
        stats[model_name][prompt]["list_items_mean"] = np.mean(list_counts)
        stats[model_name][prompt]["list_items_std"] = np.std(list_counts)
        stats[model_name][prompt]["list_items_min"] = np.min(list_counts)
        stats[model_name][prompt]["list_items_max"] = np.max(list_counts)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(stats)
