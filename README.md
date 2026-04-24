# Content Creation skills for Diagrid

This repo contains Claude skills to help with content creation.

## Prerequisites

These skills run inside the Claude Code CLI. Install it first: [Claude Code download & setup](https://docs.claude.com/en/docs/claude-code/overview). Once installed, run `claude` from the root of this repository and the skills will be available as slash commands.

## Skills

- `/write-post` — interview-driven generator that produces a structured post template (Diataxis + marketing document types).
- `/review-post` — checks a drafted post against front-matter, document-structure, style, and length rules, and returns a findings report.

## Usage

Example prompt:

"Create a blog post about how Dapr workflow persists state and how it enables durable execution"

You will be asked several questions about the content type, target audience, intent, and calls to action. The result is a markdown file with a structure that includes suggestions for titles and content for each section. You can either complete the sections yourself or Claude can do this for you. After generation, the post is automatically checked with `/review-post`, and you can rerun the review at any time.

Example results:

- [dapr-workflow-state-persistence-durable-execution-sections-only](/blog-posts/examples/dapr-workflow-state-persistence-durable-execution-sections-only.md) - a generated template where the sections are not completed but do have suggestions.
- [dapr-workflow-state-persistence-durable-execution-full](/blog-posts/examples/dapr-workflow-state-persistence-durable-execution-full.md) - a completed blog post.
