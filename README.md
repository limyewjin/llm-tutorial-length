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
  are the same across runs, but looks like it's not enabled by default. To investigate more.
- "At most X words" is the most reliable across all models for enforcing upper bounds
- Exact word counts ("100 words long") are relatively consistent but tend to overshoot slightly
- Numerical specifications work better than qualitative ones ("short and concise")
- Does "at most" work? Yes, "at most" is quite effective:
  - OpenAI stays under 100 (mean: 96.8 words)
  - Gemini stays close to 100 (mean: 101-103 words)
  - Claude slightly exceeds at 102 words
  - All models show low variance with "at most" constraints
- Does "at least" work? Yes, but with interesting variations:
  - All models exceed the minimum 100 words significantly
  - Gemini produces much longer outputs (229-280 words)
  - Claude produces 183-214 words
  - OpenAI produces 157-170 words
- Reading Time Interpretations:
  - Models interpret "1 minute" differently:
      - Claude: 207 words
      - Gemini: 172 words (mean)
      - OpenAI: 188 words (mean)
  - "30 seconds" produces shorter but inconsistent lengths
- Qualitative Descriptors:
  - Surprisingly, "extremely short and concise" often produces longer outputs than "short and concise" for some models
  - OpenAI's interpretation of "short and concise" is much longer (280 words) than Gemini's (127 words)
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