# Content Creation skills for Diagrid

This repo contains Claude skills to help with content creation.

## Prerequisites

These skills run inside the Claude Code CLI. Install it first: [Claude Code download & setup](https://docs.claude.com/en/docs/claude-code/overview). Once installed, run `claude` from the root of this repository and the skills will be available as slash commands.

## Skills

- `/write-post` — interview-driven generator that produces a structured post template (Diataxis + marketing document types).
- `/review-post` — checks a drafted post against front-matter, document-structure, style, and length rules, and returns a findings report.
- `/write-social-post` — interview-driven generator that produces a single markdown file with two variations per platform (one for Dev.to and Medium) covering X, LinkedIn, Bluesky, Reddit, Dapr Discord, Dev.to, and Medium. Auto-applies UTM parameters to `diagrid.io` and `docs.diagrid.io` links.
- `/review-social-post` — checks a generated social-post file for character limits per platform, UTM correctness, banned words, em dashes, hashtag and handle conventions, and structural completeness.

## Usage

### Blog and other long-form posts

Example prompt:

"Create a blog post about how Dapr workflow persists state and how it enables durable execution"

You will be asked several questions about the content type, target audience, intent, and calls to action. The result is a markdown file with a structure that includes suggestions for titles and content for each section. You can either complete the sections yourself or Claude can do this for you. After generation, the post is automatically checked with `/review-post`, and you can rerun the review at any time.

Example results:

- [dapr-workflow-state-persistence-durable-execution-sections-only](/examples/dapr-workflow-state-persistence-durable-execution-sections-only.md) - a generated template where the sections are not completed but do have suggestions.
- [dapr-workflow-state-persistence-durable-execution-full](/examples/dapr-workflow-state-persistence-durable-execution-full.md) - a completed blog post.

### Social posts

Example prompt:

"Create social posts about the new Dapr workflow versioning support in .NET, link https://www.diagrid.io/blog/dapr-workflow-versioning-dotnet"

You will be asked for the topic, the link, the UTM medium and campaign (only when the link points at a Diagrid host), the Reddit subreddit(s), and an optional angle. The result is a single markdown file in `social-posts/` with two variations for X, LinkedIn, Bluesky, Reddit, and Dapr Discord, plus one Dev.to and one Medium blog-style post (Medium reuses the Dev.to content). Each variation shows its character count against the platform limit. After generation, the file is automatically checked with `/review-social-post`.
