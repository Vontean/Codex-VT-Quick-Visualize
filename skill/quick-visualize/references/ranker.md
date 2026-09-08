# Ranker specification

Use Ranker when the user must put every item into a single priority order.

```json
{
  "question": "Put these tasks in priority order.",
  "items": [
    {"label": "Fix the blocker", "value": "blocker"},
    {"label": "Ship the feature", "value": "feature"},
    "Polish the documentation"
  ],
  "follow_up_prompt": "My priority order is: {ordered}. Continue using this order.",
  "follow_up_title": "Confirm priority order"
}
```

- `question`, 2-20 unique `items`, and `follow_up_prompt` are required.
- A string item uses the same label and value; an object may define both.
- Keep every label to one line.
- The template supports pointer dragging and keyboard reordering with the handle's arrow keys.
- `follow_up_prompt` must contain `{ordered}`; the renderer replaces it with a numbered ordered list.
- `follow_up_title` is an optional 1-250 character string shown as the confirmation-dialog heading after the user selects 继续. Prefer a short imperative title such as "Confirm priority order".
