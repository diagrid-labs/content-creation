## Prompt Metadata

Every generated blog post must begin with an HTML comment block that captures the skill invocation and the interview responses. This block is the first thing in the file, above the website front-matter.

Example:

```markdown
<!--
Prompt metadata
===============
Skill: blog-post
Initial prompt: Create a blogpost about workflow durability and state persistance
Topic argument: workflow durability and state persistence

Interview responses
-------------------
- Topic: workflow durability and state persistence
- Content type: blog
- Document type: Explanation
- Target audience: Backend developers who want to build reliable distributed applications
- Intent: Understand how Dapr Workflow provides reliability
- CTAs:
  1. Sign up for a free Catalyst account at https://catalyst.diagrid.io/
  2. Watch the YouTube video: https://youtu.be/T4EHE-q_F34?si=ulDi7KpUkDmBVXFa
- Key points to cover: workflow replay, comparisons with other approaches
- Internal links:
  1. https://www.diagrid.io/catalyst — managed Dapr runtime referenced in the body and summary
  2. https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/ — Dapr Workflow overview
-->
```

Include one line per interview step (Steps 1-8). The `Content type` line must record the exact lowercase value the user picked in Step 2 (one of: `blog`, `case-study`, `event`, `podcast`, `press`, `video`, `webinar`), and this same value must appear as the `contentType` field in the front-matter. If the user skipped a step or answered "none", record that explicitly (for example `- Key points to cover: none`). Preserve the user's exact wording (including any typos) in the `Initial prompt` line.

---

## Website Front-Matter

Every generated blog post must include a YAML front-matter block placed **immediately after the prompt metadata section**. This front-matter is required by the website for rendering, SEO, and categorization.

Example:

```yaml
---
title: "The Latest State of Dapr Report 2026"
slug: "state-of-dapr-2026"
excerpt: "The 2026 State of Dapr report is now available. See how the Dapr community is using workflows, AI agents, and MCP servers, and what it takes to move from prototype to production."
publishedAt: 2026-04-16
publishDateTime: "2026-04-16T08:00:00-08:00"
author: "mark-fussell"
category: "Dapr"
categories:
  - "Dapr"
  - "Agentic AI"
  - "Workflows"
tags:
  - "dapr"
  - "ai-agents"
  - "workflows"
  - "mcp"
  - "state-of-dapr"
featuredImage: "/images/blog/state-of-dapr-2026/featured.webp"
ogImage: "/images/blog/state-of-dapr-2026/featured.webp"
featured: true
contentType: blog
seoTitle: "State of Dapr 2026: AI Agents, Workflows & MCP Trends"
seoDescription: "The 2026 State of Dapr report reveals how developers are using Dapr for AI agents, durable workflows, and MCP servers, and what it takes to run them reliably in production."
canonicalUrl: "https://www.diagrid.io/blog/state-of-dapr-2026"
---
```

---

## Diataxis Structure by Document Type

### Tutorial Structure

Tutorials are **learning-oriented**. The reader is a beginner. You, the author, are the tutor.

Principles:
- Show the destination upfront ("In this tutorial, we will build...")
- Deliver visible results early and often
- Minimize explanation — link to explanation posts instead
- Keep it concrete and specific, no abstractions
- Ignore alternatives and options — one golden path
- Use "we" language ("We are in this together")

Template sections:
1. **Introduction** — What will we build? What will the reader learn? Prerequisites.
2. **Setting Up** — Environment setup, installations, accounts needed.
3. **[Core Steps: 3-5 sections]** — Each step produces a visible result. Name sections after what the reader does: "Create the [X]", "Connect [Y] to [Z]", "Deploy [X]".
4. **Verify It Works** — The reader confirms everything is running.
5. **Summary & Next Steps** — What was built, what was learned, where to go next.

### How-To Structure

How-to guides are **goal-oriented**. The reader knows what they want — help them get there.

Principles:
- Assume competence — don't over-explain basics
- Focus on the problem, not the tool
- Provide executable instructions
- Address real-world complexity; allow for variations
- Name the guide after its goal: "How to [do X]"
- Use conditional imperatives: "If you want X, do Y"

Template sections:
1. **Introduction** — The problem this solves and who it's for. Prerequisites.
2. **[Solution Steps: 3-6 sections]** — Logical, ordered steps. Name sections after outcomes: "Configure [X]", "Set up [Y]", "Handle [edge case]".
3. **Verify / Test** — How to confirm it works.
4. **Troubleshooting** (optional) — Common issues and fixes.
5. **Summary** — Recap and CTAs.

### Explanation Structure

Explanations are **understanding-oriented**. The reader wants to know *why*.

Principles:
- Make connections between concepts
- Provide context, history, and design decisions
- Embrace opinion — weigh alternatives
- Use analogy to clarify
- Structure around topics, not tasks
- Titles should work with an implicit "About" prefix

Template sections:
1. **Introduction** — The question or tension this post addresses.
2. **Background / Context** — History, prior art, or the problem space.
3. **[Core Concepts: 2-4 sections]** — Each section explores one facet. Name sections after concepts: "The Role of [X]", "Why [Y] Matters", "How [X] Compares to [Y]".
4. **Trade-offs / Considerations** — Honest discussion of limitations and alternatives.
5. **Summary** — Key insight restated, CTAs.

### Reference Structure

References are **information-oriented**. The reader needs facts.

Principles:
- Describe, don't explain or instruct
- Mirror the structure of the product/feature being documented
- Use consistent formatting and patterns
- Be precise, accurate, and complete
- Include examples that illustrate usage
- Stay neutral and objective

Template sections:
1. **Overview** — What is documented and scope.
2. **[Component Sections]** — One section per logical component. Name sections after the things being described: "[API Name]", "[Configuration Options]", "[Feature Area]".
3. **Examples** — Usage examples for key scenarios.
4. **Summary** — Quick recap, CTAs, links to related how-to guides and tutorials.

---

## Marketing Document Structures

Marketing posts follow different conventions than the Diataxis types. They tend to lead with the news and drive a clear action.

### Product Announcement Structure

Announcements are **news-oriented**. Lead with what shipped and why the reader should care.

Principles:
- Lead with the news in the first paragraph
- State the user benefit before the feature list
- Include concrete examples of what the reader can now do
- Drive to a clear next step (try it, read docs, sign up)

Template sections:
1. **Headline announcement** — What shipped, for whom, in one or two sentences.
2. **Why it matters** — The problem this solves and who feels that problem.
3. **What's new** — The feature(s), capabilities, or changes, grouped logically.
4. **How to get started** — Concrete steps or links to get hands-on.
5. **Summary** — Recap and CTAs.

### Event Announcement Structure

Event announcements are **invitation-oriented**. The reader should come away knowing the what, when, where, and why.

Principles:
- State the essentials (name, date, time, location or link) early
- Make the audience and benefit obvious
- Keep it short; the landing page has the details
- Drive to registration

Template sections:
1. **The invitation** — Event name, date, time, format (live/on-demand, in-person/virtual).
2. **Who should attend** — Target audience and what they will learn.
3. **What to expect** — Agenda, speakers, demos, or highlights.
4. **How to register** — Direct link and deadline if any.
5. **Summary** — Recap and CTAs.

### Case Study Structure

Case studies are **story-oriented**. The reader wants to see themselves in the customer's shoes.

Principles:
- Lead with the outcome, then tell the story
- Use the customer's voice where possible (quotes)
- Be specific about metrics and results
- Connect the customer's problem to the reader's likely problem

Template sections:
1. **Customer snapshot** — Who they are, industry, and scale.
2. **The challenge** — The problem they faced before adopting the product.
3. **The solution** — How they used the product, including key capabilities.
4. **The results** — Outcomes, metrics, and quotes.
5. **Summary** — What other teams can take away, and CTAs.

### Company News Structure

Company news posts are **milestone-oriented**. The reader wants to know what happened and what it means.

Principles:
- State the news in the first sentence
- Explain why it matters to users, customers, and the community
- Keep it focused; one milestone per post
- Close with what's next

Template sections:
1. **The news** — What happened, in one or two sentences.
2. **Context** — Background on why this matters now.
3. **What this means for you** — Impact on users, customers, or the community.
4. **What's next** — Upcoming milestones or how to stay in touch.
5. **Summary** — Recap and CTAs.

### Opinion / Thought Leadership Structure

Opinion posts are **argument-oriented**. The reader wants a point of view, backed by evidence.

Principles:
- State the claim early and clearly
- Support with evidence, examples, and experience
- Acknowledge counterarguments honestly
- End with a call to think, act, or discuss

Template sections:
1. **The claim** — The position you are taking, stated plainly.
2. **The tension** — The prevailing view or problem that makes this worth arguing.
3. **The argument** — Two to four points that support the claim, each with evidence.
4. **Counterpoints** — Honest treatment of objections and limits.
5. **Summary** — Restate the claim and CTAs.