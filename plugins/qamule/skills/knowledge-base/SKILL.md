---
name: knowledge-base
description: Maintain reusable and validated test knowledge to ensure the correct business context.
---

# Knowledge Base

## Structure

```txt
knowledge-base/
  app/
    overview.md
    setup.md
    domains/{domain}.md
    tasks/{task}.md
    screens/{screen}.md
    quirks/{quirk}.md
  deps/{package}/
```

- `app/` owns the primary-app knowledge; `deps/` holds system and third-party surfaces.
- `overview` and `setup` cover app identity and environment setup; `quirk` records reusable recovery paths.
- `domain` contains business rules, valid state transitions, and their constraints.
- `task` contains the preconditions, ordered steps, expected outcome, and recovery path for completing one business operation.
- `screen` contains stable selectors, visible UI states, and navigation relationships.

**One topic per file. Link related facts; do not duplicate them.**

## Frontmatter

```markdown
---
name: refund-order
description: "Refund a completed order from its detail screen."
tags: [domain:orders, task:refund, screen:order-detail]
---
```

## Content Hints

- link across documents instead of repeating the same fact.
- Write short, confirmed facts needed for the next decision.
- Exclude raw UI dumps, guesses, credentials, personal data, one-off failures, and unproven selectors.
- Update changed facts and remove invalid ones; version control retains history.
