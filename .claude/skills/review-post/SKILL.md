---
name: review-post
description: Review a drafted post file for front-matter correctness, document-type structure adherence, style-rule compliance, length, and completeness. Use when the user wants to review, critique, proofread, or check a post of any content type (blog, case-study, event, podcast, press, video, webinar) before publishing.
argument-hint: "[file-path]"
allowed-tools: Read, Glob, Grep, Skill
---

# Post Reviewer

You are a content editor reviewing a post before publication. Your job is to verify the post meets Diagrid's standards and flag anything that needs fixing. You do not rewrite the post — only report findings.

## Shared references

All definitions and rules this review enforces live in `../../post-common/`. Load the file(s) you need when you need them:

- [content-types.md](../../post-common/content-types.md) — valid `contentType` values
- [document-types.md](../../post-common/document-types.md) — document type names
- [document-structures.md](../../post-common/document-structures.md) — section template per document type
- [post-length.md](../../post-common/post-length.md) — target word counts per document type
- [front-matter.md](../../post-common/front-matter.md) — prompt metadata and YAML front-matter spec
- [style-rules.md](../../post-common/style-rules.md) — writing, title, and length rules

## Required sub-skill: humanizer

Every review MUST run the `humanizer` skill. Invoke it via the Skill tool and use it in **detection mode only**: apply its pattern catalog to identify signs of AI-generated writing (inflated significance, superficial -ing analyses, promotional language, rule-of-three, AI vocabulary, filler and hedging, and so on). During the review, run only the humanizer's identification pass — do NOT apply its rewrite. Fold the patterns it detects into this review's report (see [AI-writing patterns](#ai-writing-patterns-humanizer)).

The humanizer rewrite happens only later, and only if the user asks to apply fixes (see [After the review](#after-the-review)).

## Inputs

Accept the post path via `$ARGUMENTS`. If no path is given, ask the user which file to review or use `Glob` on `blog-posts/**/*.md` to list candidates.

## Review workflow

1. Read the post file.
2. Extract these values from the post:
   - `contentType` from the YAML front-matter
   - `Content type` line from the prompt metadata block
   - `Document type` line from the prompt metadata block
   - `Post length` line from the prompt metadata block (the numeric target)
   - CTAs listed in the prompt metadata
   - Internal links listed in the prompt metadata
3. Load the shared references needed for the review. At minimum, load [style-rules.md](../../post-common/style-rules.md), [front-matter.md](../../post-common/front-matter.md), and the section in [document-structures.md](../../post-common/document-structures.md) matching the post's document type.
4. Run every check in the [Review Checklist](#review-checklist), including the humanizer detection pass in [AI-writing patterns](#ai-writing-patterns-humanizer).
5. Produce a report in the [Report Format](#report-format).

## Review checklist

### Metadata

Run these checks only if a prompt metadata HTML comment block is present at the top of the file. If it is absent, skip this entire section.

- [ ] Prompt metadata HTML comment block is present at the top of the file with one line per interview step (1-9)
- [ ] YAML front-matter block appears immediately after the prompt metadata and includes every required field listed in [front-matter.md](../../post-common/front-matter.md)
- [ ] `contentType` matches the `Content type` line in the prompt metadata
- [ ] `contentType` is one of the values in [content-types.md](../../post-common/content-types.md)
- [ ] `slug` in the front-matter matches the filename (minus `.md`)
- [ ] `canonicalUrl` ends with the slug
- [ ] `featuredImage` and `ogImage` paths follow `/images/blog/{slug}/...`
- [ ] The bold image note ("Images (featuredImage, ogImage) are not created by this skill...") is present immediately after the closing `---` of the front-matter

### Structure

- [ ] 3-5 title suggestions are present before the intro
- [ ] Intro paragraph (~100-150 words) is written, not a placeholder
- [ ] Body sections match the template for the post's document type in [document-structures.md](../../post-common/document-structures.md) (same headings in the same order)
- [ ] Summary paragraph (~100-150 words) is written
- [ ] Every CTA listed in the prompt metadata appears in the summary (or, where natural, in the body)
- [ ] Every internal link listed in the prompt metadata appears somewhere in the intro, body, or summary

### Style

Apply every rule in [style-rules.md](../../post-common/style-rules.md). Use `Grep` on the file to scan efficiently:

- [ ] No em dashes or common substitutes (scan with regex `[—–]|--` to catch em dash U+2014, en dash U+2013, and double hyphen)
- [ ] No emojis inside list items
- [ ] No bold text formatting inside list items (scan for `^\s*[-*\d].*\*\*`)
- [ ] None of the banned words appear: journey, dive, delve into, jump into, pivotal, underscore, harness, realm, illuminate, master (case-insensitive). **Note:** "harness" and "master" are also banned in their domain-specific senses (e.g. "master branch") — flag every hit and let the author decide.
- [ ] No title combines two sentences with a colon
- [ ] No title uses the "From ... To ..." structure
- [ ] Second-person voice spot-check: read the intro and summary and confirm the narrative addresses the reader as "you". First-person plural ("we", "our") is acceptable in Tutorials and marketing voice. This is a judgement call, not a grep.

### AI-writing patterns (humanizer)

Invoke the `humanizer` skill via the Skill tool and run its identification pass over the post body (intro through summary). Report the patterns it detects. These are broader, judgement-based signals that complement the hard style rules above — do not rewrite the post here.

- [ ] Ran the `humanizer` skill in detection mode against the post body
- [ ] Listed each AI-writing pattern it flagged with a line number or quoted snippet and the pattern name (e.g. inflated significance, rule-of-three, superficial -ing analysis, promotional language, filler, excessive hedging, generic positive conclusion)
- [ ] Did not double-report em dashes or banned words already caught by the Style checks above; keep those under Style and list only the additional humanizer patterns here

- [ ] Count words from the opening intro paragraph through the closing summary paragraph (exclude front-matter, HTML comments, titles, and guidance placeholders)
- [ ] Word count is within ±15% of the target on the `Post length` line of the prompt metadata. Verify the target against [post-length.md](../../post-common/post-length.md) for the post's document type.
- [ ] If no prompt metadata is present, use the document-type's closest bucket (Short / Medium / Long) in [post-length.md](../../post-common/post-length.md) based on the measured word count. Report the matched bucket and flag a Warning if the count falls outside ±15% of any of the three buckets.

## Report format

Group findings by severity. Be specific: include the exact location (line number, heading, or quoted snippet) and a suggested fix for each finding.

### Blockers (must fix before publishing)

Things that make the post invalid or break rules:
- Missing required front-matter fields
- `contentType` missing or not in the allowed list
- Missing intro or summary
- Style rule violations: em dashes, banned words, emojis, colon titles, From-To titles
- Structural mismatches with the document type template

### Warnings (should fix)

Things that weaken the post but don't break rules:
- Word count outside ±15% of the target
- Missing CTAs or internal links that the prompt metadata says should be there
- Weak, generic, or duplicate titles
- Sections that are thin, repetitive, or off-topic for the document type
- Inconsistencies between prompt metadata and front-matter (mismatched content type, missing tags, etc.)
- AI-writing patterns flagged by the `humanizer` detection pass (inflated significance, rule-of-three, superficial -ing analyses, promotional language, filler, excessive hedging, generic positive conclusions, etc.)

### Suggestions (nice to have)

Opportunities to strengthen the post:
- Ways to sharpen the intro hook
- Sections that would benefit from a concrete example, diagram, or code snippet
- Opportunities for additional internal links to relevant Diagrid content

End the report with a clear verdict on one line:
- **Ready to publish** — zero Blockers and zero Warnings
- **Needs fixes** — zero Blockers, one or more Warnings
- **Needs major revision** — one or more Blockers

## After the review

Do not edit the post. If the user asks you to apply fixes after reading the report, work through Blockers first, then Warnings, then Suggestions, and confirm each change with the user before moving on. For the AI-writing patterns flagged by the `humanizer` detection pass, apply the fixes by running the `humanizer` skill's full rewrite (draft → final) on the affected passages, then confirm the result with the user.
