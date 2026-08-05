# Comparison specification

Use this template to choose exactly one of 2-4 plans compared across the same 2-8 dimensions.

```json
{
  "question": "Which plan fits best?",
  "plans": [
    {
      "title": "Starter",
      "value": "starter",
      "summary": "For individual, lightweight use.",
      "dimensions": [
        {"label": "Projects", "value": "3 active"},
        {"label": "Collaboration", "value": "Individual"},
        {"label": "Support", "value": "Community"}
      ]
    },
    {
      "title": "Pro",
      "value": "pro",
      "summary": "For frequent professional work.",
      "dimensions": [
        {"label": "Projects", "value": "Unlimited"},
        {"label": "Collaboration", "value": "Up to 5 people"},
        {"label": "Support", "value": "Priority"}
      ]
    }
  ],
  "selected": "pro",
  "follow_up_prompt": "I choose {selected}. Continue with this plan."
}
```

- `question`, `plans`, and `follow_up_prompt` are required.
- Each plan requires `title`, `dimensions`, and an optional unique `value` and short `summary`.
- Every plan must contain the same dimension labels in the same order. Values may differ.
- `selected` may match a plan title or value. Omit it to require a fresh choice.
- `follow_up_prompt` must contain `{selected}`; the renderer replaces it with the selected plan title.
