---
description: Start the multi-agent autonomous workflow for feature implementation
argument-hint: [goal description]
allowed-tools: Read, Glob, Grep, Task
---

# Multi-Agent Workflow

You are starting the multi-agent autonomous workflow for this goal:

**Goal:** $ARGUMENTS

## Your Role as Orchestrator

1. Read the workflow skill from `.claude/skills/multi-agent-autonomous-workflow/SKILL.md`
2. Initialize workflow state
3. Follow the three-phase workflow:
   - **Phase 1:** Analysis (analyst → architect)
   - **Phase 2:** Story execution loop (developer → tester → reviewer)
   - **Phase 3:** Completion (devops if needed)

## Starting the Workflow

1. First, invoke the `analyst` subagent with the goal to get user stories
2. Review the stories and invoke `architect` for technical design
3. For each story, follow the execution loop with quality gates

## Important Guidelines

- Use the Task tool to invoke subagents
- Each subagent returns structured output - use it to inform next steps
- Escalate to human at checkpoints or on blockers
- Mark stories as `[SECURITY-SENSITIVE]` if they involve auth, payments, or user data

Begin by reading the workflow skill and invoking the analyst subagent.
