---
prompt: "Create a blog post that explains how the Dapr workflow persists its state."
type: Explanation
audience: Developers new to workflow engines and new to Dapr
intent: Understand how the Dapr workflow engine works
ctas:
  - Sign up for a free Catalyst account at https://catalyst.diagrid.io/
  - Watch the Dapr workflow video at https://www.youtube.com/watch?v=eK6snfIAfJs
key_points:
  - What replay is and how it works
---

## Title Suggestions

1. How the Dapr Workflow Engine Remembers Everything
2. Understanding State Persistence in Dapr Workflows
3. Why Dapr Workflows Survive Crashes and Restarts
4. The Replay Mechanism That Makes Dapr Workflows Durable
5. How Dapr Workflows Keep Running When Everything Else Fails

---

## Introduction

What happens to a long-running workflow when a server crashes halfway through? If you are building microservices and coordinating work across multiple services, this question matters more than you might think. The Dapr workflow engine solves this problem by persisting every step of your workflow to a state store and using a replay mechanism to recover from failures. In this post, you will learn how Dapr workflows maintain their state, what replay means in this context, and why this architecture makes your workflows durable without requiring you to write recovery logic by hand. Whether you are new to workflow engines or just getting started with Dapr, this post will give you a clear mental model of what is happening under the hood.

---

## Background: Why Workflows Need State Persistence

<!-- Explain the problem space:
- Microservices often need to coordinate multi-step processes (e.g., order processing, data pipelines, approval flows)
- If a process spans multiple services and one fails mid-execution, you lose track of where you were
- Without a durable workflow engine, developers end up building custom retry logic, status tracking tables, and recovery code
- Introduce the concept of a workflow engine as something that manages this complexity for you
- Keep this section brief, around 100-150 words
- Link to the Dapr workflow overview: https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/
-->

## The Dapr Workflow Engine Architecture

<!-- Explain how the engine is structured:
- The workflow engine is embedded in the Dapr sidecar, not in your application
- It is powered by the Dapr actor runtime and built on the durabletask-go framework
- Your workflow code runs in your application and communicates with the sidecar via gRPC
- The sidecar handles all the orchestration, state management, and recovery
- This separation means your code stays simple: you write plain functions, and Dapr handles durability
- Link to the Dapr workflow architecture docs: https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-architecture/
-->

## How State Gets Stored

<!-- Explain the four types of records the workflow engine writes to the state store:

1. Inbox messages (inbox-NNNNNN): A FIFO queue that drives workflow execution. Messages are removed after they are consumed.
2. History events (history-NNNNNN): An append-only log of everything that has happened in the workflow. These are retained unless explicitly purged.
3. Custom status (customStatus): A user-defined JSON value that your workflow code can set to communicate progress.
4. Metadata: Tracks information about the workflow, including inbox and history lengths and generation numbers.

Note that each workflow step adds records to the state store. A single workflow run generates roughly 5 records at startup, 3 per activity or timer, and 8 per child workflow. Sequential workflows make smaller batch updates, while fan-out/fan-in patterns create larger batches.

Supported state stores include: PostgreSQL, MySQL, SQL Server, SQLite, Oracle Database, CockroachDB, MongoDB, and Redis.

Link to supported state stores: https://docs.dapr.io/reference/components-reference/supported-state-stores/
-->

## What Replay Is and How It Works

<!-- This is the core section. Explain replay clearly for someone who has never encountered the concept:

- When a workflow needs to resume (after a crash, restart, or scale event), the engine does not start over from scratch
- Instead, it loads the history events from the state store and "replays" them through your workflow function
- During replay, the engine already knows the results of previously completed steps (they are in the history)
- So it fast-forwards through those steps without re-executing the actual work (no duplicate API calls, no repeated side effects)
- When replay catches up to where the workflow left off, it resumes normal execution from that point
- This is why workflow code must be deterministic: the same inputs must produce the same sequence of steps every time
- If your workflow code changes behavior between replays (e.g., using random values or current timestamps directly), replay will break

Use an analogy: replay is like reopening a saved game. The game engine loads your save file and puts you right back where you were, without replaying every action you took from the start.

Mention that the engine uses actor reminders for fault tolerance. Before invoking your workflow code, the engine creates a one-shot reminder. If execution succeeds, the reminder is cleared. If the process crashes, the reminder fires and the actor reactivates, triggering replay automatically.

Link to Dapr workflow patterns: https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-patterns/
-->

## Trade-offs and Considerations

<!-- Discuss practical considerations honestly:

- State store choice matters: not all state stores support workflows. Some have payload size limits (e.g., Azure Cosmos DB limits items to 2 MB of UTF-8 encoded JSON).
- Long-running workflows with many steps accumulate large histories, which increases storage costs and replay time.
- Determinism constraints mean you cannot use non-deterministic operations (random numbers, current time, UUIDs) directly in workflow code. Use activities for these instead.
- The automatic recovery model means you do not write retry logic, but you do need to understand idempotency for your activities.
- Terminating a parent workflow terminates all child workflows it created, so plan your workflow hierarchy carefully.
-->

---

## Summary

The Dapr workflow engine takes the burden of state management and failure recovery off your shoulders. By persisting every step as history events in a state store, and using replay to recover workflows from exactly where they left off, Dapr gives your workflows durability without added complexity in your code. The key insight is that your workflow function is replayed against its saved history, skipping completed work and resuming from the last checkpoint. As long as your workflow code is deterministic, the engine handles crashes, restarts, and scaling transparently. To see the workflow engine in action, [watch this walkthrough on YouTube](https://www.youtube.com/watch?v=eK6snfIAfJs). Ready to try it yourself? [Sign up for a free Catalyst account](https://catalyst.diagrid.io/) and start building durable workflows today.
