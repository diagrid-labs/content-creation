# Prompt Metadata and Website Front-Matter

Every post file begins with two blocks in this exact order:

1. A prompt metadata HTML comment block.
2. A YAML front-matter block.

Immediately after the closing `---` of the front-matter, include this line on its own:

> **Note: Images (featuredImage, ogImage) are not created by this skill. You need to add them manually before publishing.**

---

## 1. Prompt metadata

Captures the skill invocation and interview responses. Placed at the top of the file, above the website front-matter.

Example:

```markdown
<!--
Prompt metadata
===============
Skill: write-post
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
  2. https://www.diagrid.io/dapr-university/dapr-workflow — Dapr Workflow track for Dapr University
- Post length: Medium (~1200 words)
-->
```

Requirements:

- Include one line per interview step (Steps 1-9 of the write-post interview).
- The `Content type` line must record the exact lowercase value picked during the interview and listed in [content-types.md](content-types.md).
- That same value must appear in the `contentType` field of the YAML front-matter below.
- If a step was skipped or answered "none", record that explicitly (for example `- Key points to cover: none`).
- Preserve the user's exact wording (including typos) on the `Initial prompt` line.

---

## 2. Website front-matter

Required by the website for rendering, SEO, and categorization. Placed immediately after the prompt metadata block.

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

Required fields: `title`, `slug`, `excerpt`, `publishedAt`, `publishDateTime`, `author`, `category`, `categories`, `tags`, `featuredImage`, `ogImage`, `featured`, `contentType`, `seoTitle`, `seoDescription`, `canonicalUrl`.

Consistency rules:

- `slug` must match the filename (minus `.md`).
- `contentType` must match the `Content type` line in the prompt metadata and must be one of the values in [content-types.md](content-types.md).
- `featuredImage` and `ogImage` paths should follow `/images/blog/{slug}/...`.
- `canonicalUrl` should end with the slug.
