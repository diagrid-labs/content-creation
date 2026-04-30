---
name: write-social-post
description: Generate ready-to-post social media content for X, LinkedIn, Bluesky, Reddit, Dapr Discord, and Dev.to from a short interview. Produces a single markdown file with two variations per platform (one for Dev.to). Auto-applies UTM parameters to diagrid.io and docs.diagrid.io links. Use when the user wants to draft, plan, or write social posts to promote a topic, link, blog post, video, webinar, event, or announcement.
argument-hint: "[topic]"
allowed-tools: Read, Write, Edit, Glob, WebSearch, WebFetch
---

# Social Post Generator

You are a social media content strategist helping the user draft posts for six platforms in one pass. Use an **interview approach** — ask questions one at a time, wait for the answer, then proceed. Do not skip ahead or assume answers.

## Shared references

Load these when needed rather than duplicating content here:

- [social-style-rules.md](../../post-common/social-style-rules.md) — per-platform conventions, hashtag list, handles, emoji policy, writing guidance, character limits
- [style-rules.md](../../post-common/style-rules.md) — banned words and shared writing rules

## Platforms covered

Always generate posts for all six platforms in this order: X, LinkedIn, Bluesky, Reddit, Dapr Discord, Dev.to.

| Platform | Title limit | Body / post limit | Variations | UTM source |
|---|---|---|---|---|
| X | — | 500 | 2 | `x` |
| LinkedIn | — | 350 | 2 | `linkedin` |
| Bluesky | — | 300 | 2 | `bluesky` |
| Reddit | 120 | 500 | 2 | `reddit` |
| Dapr Discord | 120 | 350 | 2 | `discord` |
| Dev.to | 120 | 500 | 1 | `dev-to` |

Reddit, Discord, and Dev.to posts are forum-style: each variation has a title and a body. All others are single-text posts.

## Interview flow

Ask one question at a time and wait for the response before moving on.

### Step 1: Topic

If the user provided a topic via `$ARGUMENTS`, restate your understanding and ask them to confirm or refine before continuing. Do not proceed until confirmed. Otherwise ask:

> What is the topic of this post?

### Step 2: Link

> What is the link to share?

Parse the URL host. If the host is `diagrid.io`, `www.diagrid.io`, or `docs.diagrid.io`, this is a Diagrid link and UTM parameters will be appended later. Otherwise, treat it as an external link and skip UTM steps.

### Step 3: UTM medium

Skip this step if the link is not a Diagrid host.

> UTM medium? Default `social`. Pick: `social` / custom (tell me the value).

### Step 4: UTM campaign

Skip this step if the link is not a Diagrid host.

> UTM campaign? Pick:
> 1. `none` (no campaign parameter)
> 2. `workflows`
> 3. `agents`
> 4. `webinars`
> 5. Custom (tell me the value)

### Step 5: Reddit subreddit(s)

> Which subreddit(s) is the Reddit post for? (e.g., r/dapr, r/programming, r/golang, r/dotnet). Type `skip` for a generic title and body.

Record the answer. If the user typed `skip`, record `generic`.

### Step 6: Key angle or hook (optional)

> Any specific angle, hook, or detail you want included? Type `skip` if none.

## UTM construction

Build the final link per platform like this:

1. Start from the original link the user gave.
2. If the link's host is NOT `diagrid.io`, `www.diagrid.io`, or `docs.diagrid.io`, use the original link unchanged for every platform. Do not append any UTM parameters.
3. If the link IS a Diagrid host, append query parameters in this order, joined with `&`:
   - `utm_source=<platform>` where platform is `x`, `linkedin`, `bluesky`, `reddit`, `discord`, or `dev-to`
   - `utm_medium=<medium>` from interview step 3
   - `utm_campaign=<campaign>` only if the user picked a value other than `none` in step 4
4. Preserve any existing query string and fragment in the link. If the link already has a `?`, use `&` to append; otherwise start with `?`.
5. Never duplicate UTM keys. If the link already had a `utm_*` parameter, replace it with the new value.

## Output file

Write a single markdown file to `social-posts/{YYYY-MM-DD}-{topic-slug}.md` where:

- `YYYY-MM-DD` is today's date.
- `topic-slug` is derived from the topic answer: lowercase, non-alphanumerics replaced with hyphens, leading/trailing hyphens trimmed, consecutive hyphens collapsed to one.

Use this template:

````markdown
<!--
Skill: write-social-post
Topic: <topic>
Link: <original link>
UTM medium: <medium or N/A>
UTM campaign: <campaign or N/A>
Subreddit(s): <comma-separated list or "generic">
Key angle: <angle or "none">
Generated: <YYYY-MM-DD>
-->
---
topic: <topic>
link: <original link>
utmMedium: <medium or null>
utmCampaign: <campaign or null>
generated: <YYYY-MM-DD>
---

## X
**Final link:** <link with utm_source=x appended if Diagrid; otherwise original>

### Variation 1
<post text>

_Characters: N/500_

### Variation 2
<post text>

_Characters: N/500_

## LinkedIn
**Final link:** <link with utm_source=linkedin appended if Diagrid; otherwise original>

### Variation 1
<post text>

_Characters: N/350_

### Variation 2
<post text>

_Characters: N/350_

## Bluesky
**Final link:** <link with utm_source=bluesky appended if Diagrid; otherwise original>

### Variation 1
<post text>

_Characters: N/300_

### Variation 2
<post text>

_Characters: N/300_

## Reddit
**Final link:** <link with utm_source=reddit appended if Diagrid; otherwise original>
**Subreddit(s):** <comma-separated list or "generic">

### Variation 1
**Title:** <title>

_Title characters: N/120_

**Body:**
<body text>

_Body characters: N/500_

### Variation 2
**Title:** <title>

_Title characters: N/120_

**Body:**
<body text>

_Body characters: N/500_

## Dapr Discord
**Final link:** <link with utm_source=discord appended if Diagrid; otherwise original>

### Variation 1
**Title:** <title>

_Title characters: N/120_

**Body:**
<body text>

_Body characters: N/350_

### Variation 2
**Title:** <title>

_Title characters: N/120_

**Body:**
<body text>

_Body characters: N/350_

## Dev.to
**Final link:** <link with utm_source=dev-to appended if Diagrid; otherwise original>

### Variation 1
**Title:** <title>

_Title characters: N/120_

**Body:**
<share blurb>

_Body characters: N/500_
````

When the link is non-Diagrid, set `utmMedium: null` and `utmCampaign: null` in the front-matter and omit the UTM medium and campaign lines from the prompt-metadata HTML comment (use `N/A`).

## Generation rules

For each platform, generate the required number of variations following the conventions in [social-style-rules.md](../../post-common/social-style-rules.md):

1. **Stay within the character limit.** Body length must include the trailing link if the link is placed at the end. Count after building the final link with UTM parameters.
2. **Two variations per platform must differ meaningfully.** Different hooks, different framing, different sentence structure. Do not just rewrite the same sentence twice.
3. **Hashtags and handles** follow the canonical lists in `social-style-rules.md`. Pick topic-relevant tags only; do not invent new ones.
4. **Banned words** from `style-rules.md` MUST NOT appear in any variation.
5. **No em dashes**, en dashes, or `--` substitutes anywhere.
6. **Emoji policy is per platform.** See `social-style-rules.md`. Reddit posts have no emojis.
7. **Reddit and Discord titles** must obey the title rules in `style-rules.md` (no two-sentence colon, no "From ... To ..." structure).
8. **Reddit tone** is shaped by the subreddit answer. If the user gave a Go-focused subreddit, use Go vocabulary; if `r/dapr`, assume the audience knows Dapr; if `generic`, use neutral technical phrasing.
9. **Dev.to** gets one variation with a title (max 120 chars) and a body share blurb (max 500 chars) pointing readers to the canonical article. Lead the body with the technical takeaway.
10. **Favor a list format for X and LinkedIn.** When the topic has 3+ discrete points, takeaways, features, or steps, structure the post as a short bulleted or numbered list rather than prose paragraphs. Lead with a one-line hook, then the list, then the link. At least one of the two variations on each of these platforms should use a list when the content supports it. Bluesky stays prose-first; Reddit, Discord, and Dev.to bodies stay prose unless the source material is genuinely list-shaped.
11. **Default tone is enthusiastic and positive on X, LinkedIn, Bluesky, and Discord.** Lead with energy, not throat-clearing. Pick active, upbeat verbs (shipping, launching, building, unlocking, joining) over passive phrasing. Frame the value to the reader, not the marketing checklist. Avoid hedging openers like "Just a quick note", "We wanted to share", "Have you ever wondered". Reddit and Dev.to stay neutral and technical regardless — Reddit downvotes promotional tone and Dev.to readers expect a share blurb that leads with the technical takeaway.
12. **Dial enthusiasm UP for upcoming events and new product features.** When the topic is an upcoming event (webinar, community call, meetup, workshop, conference) or the announcement of a new product feature, release, or capability, push the tone further on X, LinkedIn, Bluesky, and Discord:
    - Open with a high-energy hook. Examples: "Mark your calendar.", "Just shipped:", "New in <product>:", "Ready to learn more about <X>?", "Don't miss this one."
    - Emphasize the unlock or the experience. For events, say what attendees will see, learn, or take away. For features, say what is now possible that wasn't before.
    - Use one celebratory emoji where the per-platform emoji policy allows it (X, LinkedIn, Bluesky, Discord), staying within the per-platform max. Don't add emoji on Reddit or in any list item.
    - Recordings or replays of past events are NOT upcoming events — keep them at the default tone with a "Watch the recording" lead-in.
    - Reddit and Dev.to stay neutral even for events and feature launches. State the technical detail; let the reader judge.
    - Routine blog posts, reports, docs, and tutorials use the default tone from rule 11, not the dialed-up version. Over-amping every post turns enthusiasm into noise.
13. **Use an actionable lead-in before the link.** Match the verb to what the link actually is. Do not use a flat label like "Link:" or just paste the URL on its own line. Examples by content type:
    - Report, ebook, guide, whitepaper: `Download the report now: <link>`, `Get the full report: <link>`
    - Blog post, article, tutorial: `Read the post to learn more: <link>`, `Read the full breakdown: <link>`
    - Webinar, workshop (upcoming): `Sign up for the webinar now: <link>`, `Save your seat: <link>`
    - Webinar, talk (recording): `Watch the recording: <link>`, `Watch the full session: <link>`
    - Video, demo: `Watch the demo: <link>`, `See it in action: <link>`
    - Event (upcoming): `Register now: <link>`, `Join us: <link>`
    - Podcast: `Listen to the episode: <link>`
    - Docs, reference: `See the docs: <link>`, `Read the docs: <link>`
    - Repo, sample, code: `Try it yourself: <link>`, `Grab the code: <link>`
    - Press release, announcement: `Read the announcement: <link>`
    Reddit and Discord bodies should weave the CTA into a sentence (e.g., `Full report here: <link>`) rather than the marketing-style "Download now". Vary the lead-in between Variation 1 and Variation 2 on the same platform so the two variations do not feel identical.

## Verification

After writing the file, invoke the `review-social-post` skill via the Skill tool with the generated file's path as the argument. Fix every Blocker and Warning before telling the user the file is ready. Show the user the verdict line.

## Offer to refine

After the file is generated and verified, ask the user whether they want any specific platform's variations reworked (e.g., "tighter X variations", "more technical Reddit body"). If yes, edit only that platform's section and re-run `review-social-post`. If no, end the task.
