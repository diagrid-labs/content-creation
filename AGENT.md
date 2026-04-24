# Content Creation Agent

This repository contains Claude Code skills for creating and reviewing content at Diagrid.

## Prerequisites

These skills require the Claude Code CLI. Install it from the [Claude Code docs](https://docs.claude.com/en/docs/claude-code/overview) before using the commands below. Once `claude` is available on your PATH, launch it from the repo root and the `/write-post` and `/review-post` slash commands will be loaded automatically.

## Available Skills

### `/write-post`

Create a post template using an interview-driven approach based on the Diataxis framework. Run `/write-post` (optionally with a topic) to start an interactive interview that produces a structured markdown template tailored to the chosen content type (blog, case-study, event, podcast, press, video, webinar) and document type (Tutorial, How-to, Explanation, Reference, Product announcement, Event announcement, Case study, Company news, Opinion / Thought leadership).

Skill definition: [.claude/skills/write-post/SKILL.md](.claude/skills/write-post/SKILL.md)

### `/review-post`

Review a drafted post for front-matter correctness, document-type structure, style-rule compliance, and length. Returns a findings report grouped by Blockers, Warnings, and Suggestions, plus a publish-readiness verdict. Invoked automatically at the end of `/write-post` and can also be run standalone on any post in `blog-posts/`.

Skill definition: [.claude/skills/review-post/SKILL.md](.claude/skills/review-post/SKILL.md)

## Shared references

Both skills pull their definitions and rules from [.claude/post-common/](.claude/post-common/):

- [content-types.md](.claude/post-common/content-types.md) — valid `contentType` values
- [document-types.md](.claude/post-common/document-types.md) — Diataxis and marketing document types
- [document-structures.md](.claude/post-common/document-structures.md) — section template per document type
- [post-length.md](.claude/post-common/post-length.md) — target word counts per document type
- [front-matter.md](.claude/post-common/front-matter.md) — prompt metadata and YAML front-matter spec
- [style-rules.md](.claude/post-common/style-rules.md) — writing, title, and length rules
