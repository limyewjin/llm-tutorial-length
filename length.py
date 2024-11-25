
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

PROMPTS = ["The summary is 100 words long.",
           "The summary is one hundred words long.",
           "The summary is at most 100 words long.",
           "The summary is at most one hundred words long.",
           "The summary is at least 100 words long.",
           "The summary is at least one hundred words long.",
           "The summary is 30 seconds long to read aloud.",
           "The summary is 60 seconds long to read aloud.",
           "The summary is 1 minute long to read aloud.",
           "The summary is short and concise.",
           "The summary is very short and concise.",
           "The summary is extremely short and concise."]

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
            print(f"Word count: {word_count}")

            if "word_count" not in stats[model_name][prompt]:
                stats[model_name][prompt]["word_count"] = []
            stats[model_name][prompt]["word_count"].append(word_count)

for model_name, model_stats in stats.items():
    for prompt, prompt_stats in model_stats.items():
        word_counts = stats[model_name][prompt]["word_count"]
        mean = np.mean(word_counts)
        std_dev = np.std(word_counts)
        min_count = np.min(word_counts)
        max_count = np.max(word_counts)

        stats[model_name][prompt]["mean"] = mean
        stats[model_name][prompt]["std_dev"] = std_dev
        stats[model_name][prompt]["min"] = min_count
        stats[model_name][prompt]["max"] = max_count

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(stats)
