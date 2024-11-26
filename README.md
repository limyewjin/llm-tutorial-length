# LLM Tutorial - Checking different prompts for controlling output length

# Text Length Control

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
  stats were the same across runs, so I added temperature=0.05 to add some randomness.
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


# Bullet Points Control

### Consistency in Meeting Requested List Length

- For small to medium lists (3-20 points):
  - All models are extremely consistent, perfectly hitting the requested number of points
  - Anthropic, Gemini, and OpenAI all show 0.0 standard deviation for list counts
- For large lists (50 points):
  - OpenAI tends to overshoot (avg 55.8 points)
  - Gemini slightly overshoots (avg 52.6 points)
  - Anthropic tends to undershoot (avg 14.0 points for ordered, 48.2 for unordered)

### Ordered vs Unordered Lists
  - For 50-point lists, ordered lists maintain exact counts while unordered lists tend to overshoot
  - OpenAI: Ordered (exactly 50) vs Unordered (avg 55.8)
  - Gemini: Ordered (exactly 50) vs Unordered (avg 52.6)
  - Anthropic: Ordered (avg 14.0) vs Unordered (avg 48.2)
  - Recommendation: Use ordered lists when precise control over list length is critical