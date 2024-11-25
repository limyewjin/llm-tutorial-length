# LLM Tutorial - Length

Let's test how we can control output length with different prompts across different models!

We test the following:

```
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
```

## Questions

- Which prompt format provides the most consistent length control?
- Do quantitative constraints (exact word counts) work better than qualitative ones (short, very short)?
- How effective are "at most" and "at least" modifiers in controlling output boundaries?
- Does specifying reading time result in consistent output lengths?

## Results

- Anthropic seems to have some form of [prompt caching](https://www.anthropic.com/news/prompt-caching) as the
  are the same across runs, so I added temperature=0.05 to add some randomness.
- "At most X words" is the most reliable across all models for enforcing upper bounds
- Exact word counts ("100 words long") are relatively consistent but tend to overshoot slightly
- Numerical specifications work better than qualitative ones ("short and concise")
- Does "at most" work? Yes, "at most" is highly effective:
  - OpenAI stays under 100 (mean: 86-91 words)
  - Gemini stays under 100 (mean: 91-96 words)
  - Claude consistently uses exactly 81 words
  - All models show remarkably low variance with "at most" constraints
- Does "at least" work? Yes, but with interesting variations:
  - All models exceed the minimum 100 words significantly
  - Gemini produces longer outputs (215-238 words)
  - Claude produces 167-193 words
  - OpenAI produces 119-157 words
- Reading Time Interpretations:
  - Models interpret "1 minute" differently:
      - Claude: 126 words (mean)
      - Gemini: 159 words (mean)
      - OpenAI: 152 words (mean)
  - "30 seconds" produces shorter but inconsistent lengths
- Qualitative Descriptors:
  - Surprisingly, "extremely short and concise" often produces longer outputs than "short and concise" for some models
  - OpenAI's interpretation of "short and concise" averages 135 words
  - Gemini's interpretation averages 114 words
  - Qualitative descriptors show the highest variance across all models
- Numeric vs Text Numbers:
  - "100 words" vs "one hundred words" produce similar results
  - Slight variations exist but not significantly different

## Recommendations for practitioners:
- Use "at most X words" for strict upper bounds
- Avoid qualitative descriptors when precise length control is needed
- Expect outputs to exceed specified lengths by 10-15% when using exact word counts
- Don't rely on reading time estimates for consistent length control
- When working across multiple models, use explicit numerical constraints for best consistency