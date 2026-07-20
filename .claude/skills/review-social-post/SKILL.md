---
name: review-social-post
description: Review a generated social-post markdown file for character limits per platform, UTM parameter correctness on diagrid.io links, banned words, em dashes, hashtag and handle conventions, and structural completeness. Use when the user wants to review, validate, or check a social-post file in the social-posts/ folder before publishing.
argument-hint: "[file-path]"
allowed-tools: Read, Glob, Grep, Bash, Skill
---

# Social Post Reviewer

You are a social media editor reviewing a generated post file before publication. Your job is to verify the file meets Diagrid's social standards and flag anything that needs fixing. You do not rewrite the post, only report findings.

## Shared references

Load these when needed:

- [social-style-rules.md](../../post-common/social-style-rules.md) — per-platform conventions, hashtag list, handles, emoji policy, character limits
- [style-rules.md](../../post-common/style-rules.md) — banned words, em-dash rule, title rules

## Required sub-skill: humanizer

Every review MUST run the `humanizer` skill. Invoke it via the Skill tool and use it in **detection mode only**: apply its pattern catalog to identify signs of AI-generated writing (promotional language, rule-of-three, AI vocabulary, filler and hedging, manufactured punchlines, and so on) across the post text of each variation. During the review, run only the humanizer's identification pass — do NOT apply its rewrite. Fold the patterns it detects into this review's report (see [AI-writing patterns](#ai-writing-patterns-humanizer)).

The humanizer rewrite happens only later, and only if the user asks to apply fixes (see [After the review](#after-the-review)).

## Inputs

Accept the file path via `$ARGUMENTS`. If no path is given, ask the user which file to review or use `Glob` on `social-posts/**/*.md` to list candidates.

## Review workflow

1. Read the file.
2. Extract these values:
   - The prompt-metadata HTML comment block (topic, link, UTM medium, UTM campaign, subreddits, generated date).
   - The YAML front-matter (`topic`, `link`, `utmMedium`, `utmCampaign`, `generated`).
   - The list of `## <Platform>` headings present.
   - For each platform: the `**Final link:**` value, all `### Variation N` blocks, and (for Reddit, Dapr Discord, and Dev.to) the `**Title:**` and `**Body:**` lines.
3. Load the shared references.
4. Run the deterministic length validator: `python scripts/social_chars.py validate <path> --json`. Parse the JSON. Each entry where `over: true` is a length **Blocker**. Each non-empty `structural_errors` entry is a structural **Blocker**. Do not compute character counts inline; the script is the source of truth.
5. Run every remaining check in the [Review checklist](#review-checklist) (UTM, banned words, em dashes, hashtag count, handle presence, title rules, and the humanizer detection pass in [AI-writing patterns](#ai-writing-patterns-humanizer)). Length and structural completeness are already covered by step 4.
6. Produce a report in the [Report format](#report-format).

## Review checklist

### Metadata

- [ ] Prompt-metadata HTML comment block is present at the top of the file
- [ ] YAML front-matter block appears immediately after, with `topic`, `link`, `utmMedium`, `utmCampaign`, `generated` fields
- [ ] `generated` date matches the `YYYY-MM-DD` prefix in the filename
- [ ] If the link host is `diagrid.io`, `www.diagrid.io`, or `docs.diagrid.io`, then `utmMedium` is set (not null)
- [ ] If the link host is NOT a Diagrid host, then `utmMedium` and `utmCampaign` are both `null`

### Structure

The script's `structural_errors` cover: missing platform sections, wrong number of variations per platform, and missing `**Title:**` / `**Body:**` for Reddit, Dapr Discord, and Dev.to. The remaining structural checks below stay in the skill:

- [ ] Prompt-metadata HTML comment block is present at the top of the file
- [ ] YAML front-matter block appears immediately after, with `topic`, `link`, `utmMedium`, `utmCampaign`, `generated` fields
- [ ] `generated` date matches the `YYYY-MM-DD` prefix in the filename
- [ ] Each platform section has a `**Final link:**` line directly under the heading
- [ ] The Reddit section has a `**Subreddit(s):**` line (value is a comma-separated list or `generic`)

### Length (Blocker if exceeded)

All length checks come from `scripts/social_chars.py validate --json`. See workflow step 4. Do not count characters inline.

### UTM

For every `**Final link:**` value:

- [ ] If the host is `diagrid.io`, `www.diagrid.io`, or `docs.diagrid.io`:
  - Contains `utm_source=<platform>` where platform matches the section it appears in (`x`, `linkedin`, `bluesky`, `reddit`, `discord`, or `dev-to`)
  - Contains `utm_medium=<value>` where value matches the `utmMedium` field in the front-matter
  - If the prompt metadata's UTM campaign is not `N/A` and not `none`, contains `utm_campaign=<value>` matching that field
  - Does not contain duplicate `utm_*` keys
- [ ] If the host is NOT a Diagrid host: contains no `utm_*` parameters

### Style

Use `Grep` on the file to scan efficiently.

- [ ] No banned words (case-insensitive): journey, dive, delve into, jump into, pivotal, underscore, harness, realm, illuminate, master (Blocker)
- [ ] No em dashes, en dashes, or `--` substitutes (regex `[—–]|--`) (Blocker)
- [ ] X, LinkedIn, and Bluesky variations do NOT include a Diagrid handle (`@diagridio`, `@Diagrid`, `@diagrid.io`, `@diagrid`) (Warning if present)
- [ ] Hashtag count per platform variation matches `social-style-rules.md`: X 2-3, LinkedIn 3-5, Bluesky 1-2, Reddit / Discord / Dev.to 0 (Warning if outside range)
- [ ] All hashtags used are from the canonical Diagrid hashtag list in `social-style-rules.md` (Warning if a tag is not on the list)
- [ ] Reddit variations contain no emojis and no hashtags (Blocker if either is present)
- [ ] Reddit and Discord titles obey the title rules in `style-rules.md` (no two-sentence colon, no "From ... To ..." structure) (Blocker)

### AI-writing patterns (humanizer)

Invoke the `humanizer` skill via the Skill tool and run its identification pass over the post text of each platform variation. Report the patterns it detects. These are broader, judgement-based signals that complement the hard style rules above — do not rewrite the posts here.

- [ ] Ran the `humanizer` skill in detection mode against each platform variation
- [ ] Listed each AI-writing pattern it flagged with the platform, variation number, and a quoted snippet, plus the pattern name (e.g. promotional language, rule-of-three, AI vocabulary, filler, excessive hedging, manufactured punchlines, generic positive conclusion) (Warning)
- [ ] Did not double-report em dashes or banned words already caught by the Style checks above; keep those under Style and list only the additional humanizer patterns here

## Report format

Group findings by severity. Be specific: include the platform, variation number, and a quoted snippet or line reference for each finding, plus a suggested fix.

### Blockers (must fix before publishing)

- Length over the platform limit
- Banned words
- Em dashes / en dashes / `--`
- Missing required structure (missing platform section, wrong number of variations, missing Title/Body for Reddit, Discord, or Dev.to)
- Missing or wrong UTM parameters on Diagrid links; UTM parameters present on non-Diagrid links
- Reddit emojis or hashtags
- Title rule violations on Reddit / Discord titles

### Warnings (should fix)

- Displayed character count does not match the actual count
- Hashtag count outside the platform's range
- Hashtag not on the canonical list
- Diagrid handle present on X / LinkedIn / Bluesky
- Two variations on the same platform are too similar (same hook, same opening, same framing)
- AI-writing patterns flagged by the `humanizer` detection pass (promotional language, rule-of-three, AI vocabulary, filler, excessive hedging, manufactured punchlines, generic positive conclusions, etc.)

### Suggestions (nice to have)

- First line on X / LinkedIn / Bluesky / Discord does not lead with a problem-solution opener (concrete developer pain point, then how the topic addresses it). Flag if the opener is a marketing exclamation, a hedging phrase, or a generic benefit claim with no paired problem.
- Tighter phrasing where the variation is close to the limit
- Topic-relevant hashtag from the canonical list that was not used

End the report with a verdict on one line:

- **Ready to publish** — zero Blockers and zero Warnings
- **Needs fixes** — zero Blockers, one or more Warnings
- **Needs major revision** — one or more Blockers

## After the review

Do not edit the file. If the user asks you to apply fixes, work through Blockers first, then Warnings, then Suggestions, and confirm each change before moving to the next. For the AI-writing patterns flagged by the `humanizer` detection pass, apply the fixes by running the `humanizer` skill's full rewrite (draft → final) on the affected variations, then confirm the result with the user.
