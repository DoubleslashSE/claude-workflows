---
description: Execute a complete workshop session with a single operator. Tracks exploration state, implements backtracking after deep dives, and documents both explored findings and uncharted territory.
---

# Workshop Session

Execute a complete workshop session for: **$ARGUMENTS**

## Single Operator Model

**IMPORTANT**: This workshop runs through a single operator who may represent themselves or a group.

- When the operator decides to dive deeper → that IS the group's decision
- When the operator decides to move on → proceed without second-guessing
- When the operator decides to stop → stop immediately and document
- The operator handles ensuring all voices in their group are heard

Your job: Guide exploration systematically, track territory, backtrack after deep dives, document everything.

## Workshop Flow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│              EXPLORATION-BASED WORKSHOP FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PHASE 1: TERRITORY MAPPING                                     │
│  ├─ Clarify objectives and scope                                │
│  ├─ Identify major branches to explore                          │
│  ├─ Create initial exploration map                              │
│  └─ Validate map with operator                                  │
│                                                                 │
│  PHASE 2: SYSTEMATIC EXPLORATION                                │
│  ├─ Work through branches                                       │
│  ├─ At each branch:                                             │
│  │  ├─ Generate ideas/insights                                  │
│  │  ├─ Identify sub-branches                                    │
│  │  └─ Checkpoint: dive deeper or move on?                      │
│  ├─ If dive deeper:                                             │
│  │  ├─ Note position for backtrack                              │
│  │  ├─ Explore sub-branch                                       │
│  │  └─ BACKTRACK: Return and show remaining                     │
│  └─ Update exploration map continuously                         │
│                                                                 │
│  PHASE 3: CONVERGENCE (when operator ready)                     │
│  ├─ Group and prioritize findings                               │
│  └─ Define actions for priorities                               │
│                                                                 │
│  PHASE 4: DOCUMENTATION                                         │
│  ├─ Document EXPLORED territory with findings                   │
│  ├─ Document UNCHARTED territory explicitly                     │
│  └─ Recommend future session starting points                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 1: Territory Mapping

### Initial Discovery

1. **Topic**: What are we exploring?
2. **Goal**: What does success look like?
   - Chart everything?
   - Focus on specific areas?
   - Generate ideas for action?
3. **Context**: What's relevant background?

### Create Exploration Map

Decompose the topic into major branches:

```markdown
## Exploration Map: [TOPIC]

**Goal**: [What we aim to achieve]

**Territory**:
```
[TOPIC]
├─ [Branch A] ──────────── ○ UNCHARTED
├─ [Branch B] ──────────── ○ UNCHARTED
├─ [Branch C] ──────────── ○ UNCHARTED
└─ [Branch D] ──────────── ○ UNCHARTED
```

**Status Key**:
- ✓ EXPLORED - Fully covered
- ◐ PARTIAL - Started, not complete
- ○ UNCHARTED - Not yet explored
- → CURRENT - Exploring now
- ⊘ SKIPPED - Operator chose to skip
```

### Validate with Operator

"Does this map capture the territory? Any branches to add, remove, or rename?"

"Where would you like to start? Or should we work through systematically?"

## Phase 2: Systematic Exploration

### Entering a Branch

```markdown
## Exploring: [Branch Name]

**Current Position**:
```
[TOPIC]
├─ [A] ──────────── ✓ EXPLORED (7 ideas)
├─ [B] ──────────── → CURRENT
├─ [C] ──────────── ○ UNCHARTED
└─ [D] ──────────── ○ UNCHARTED
```

"Let's explore [B]. What ideas, aspects, or considerations come to mind?"
```

### During Exploration

- Capture all contributions
- Note when sub-branches emerge
- Build on ideas with follow-up questions

### Checkpoint Format

**At EVERY checkpoint, show:**

```markdown
**Checkpoint: [Current Branch]**

**Just completed**: [What we explored]
**Captured**: [N] ideas/insights

**Current Map**:
```
[TOPIC]
├─ [A] ──────────── ✓ EXPLORED
├─ [B] ──────────── → CURRENT
│  ├─ [B.1] ─────── ○ UNCHARTED (just identified)
│  └─ [B.2] ─────── ○ UNCHARTED (just identified)
├─ [C] ──────────── ○ UNCHARTED
└─ [D] ──────────── ○ UNCHARTED
```

**Options**:
1. **Dive deeper** into [B.1] or [B.2]
2. **Mark [B] complete** and move to [C]
3. **Stop here** and document current state
```

### Deep Dive Protocol

When operator chooses to dive deeper:

```markdown
## Deep Dive: [Sub-branch]

**Position saved for backtrack**:
- Parent: [B]
- Unexplored siblings: [B.2]
- Next main branch: [C]

"Diving into [B.1]..."

[Explore deeper]

---

**BACKTRACK**

"We've explored [B.1]. Returning to [B] level."

**Remaining unexplored**:
- [B.2] - sibling sub-branch
- [C], [D] - main branches

"Would you like to explore [B.2], move to [C], or stop here?"
```

### Moving On

When operator chooses to move on:

1. Mark current branch as EXPLORED or PARTIAL
2. Note any sub-branches identified but not explored
3. Show next branch and remaining territory
4. Proceed

## Phase 3: Convergence

When operator is ready to converge (or all branches explored):

### Synthesis

"Let me organize our findings across all explored branches..."

```markdown
## Findings Summary

**By Branch**:
- [A]: [N] ideas - Key themes: [themes]
- [B]: [N] ideas - Key themes: [themes]
  - [B.1]: [N] ideas (deep dive)

**Cross-cutting Themes**:
1. [Theme spanning branches]
2. [Theme spanning branches]
```

### Prioritization

"Which findings are most important to act on?"

Options:
- Top 3 selection
- Dot voting
- Impact/effort assessment

### Action Definition

For each priority:
- What's the first concrete action?
- Who owns it?
- By when?

## Phase 4: Documentation

### Final Exploration Map

```markdown
## Final Exploration Map

```
[TOPIC]
├─ [A] ──────────── ✓ EXPLORED
│  └─ 7 ideas captured
├─ [B] ──────────── ✓ EXPLORED
│  ├─ [B.1] ─────── ✓ EXPLORED (deep dive)
│  │  └─ 12 ideas captured
│  └─ [B.2] ─────── ⊘ SKIPPED
├─ [C] ──────────── ◐ PARTIAL
│  └─ 3 ideas, needs more work
└─ [D] ──────────── ○ UNCHARTED
```
```

### Explored Territory

Document findings for each explored branch with:
- Ideas captured
- Key insights
- Decisions made
- Connections to other branches

### Uncharted Territory

**REQUIRED** - Document what was NOT explored:

```markdown
## Uncharted Territory

### [D]: [Name]
**Status**: ○ UNCHARTED
**Reason**: Session ended before reaching
**What's likely there**: [Brief description]
**Recommended for**: Future session
**Priority**: [High/Medium/Low]

### [B.2]: [Name]
**Status**: ⊘ SKIPPED
**Reason**: Operator chose to prioritize [B.1]
**What's there**: [If known]
**Recommended for**: Follow-up if [B.1] findings warrant
```

### Future Work Recommendations

```markdown
## Recommended Next Steps

**Priority 1**: [Immediate actions from this session]

**Future Sessions**:
1. Complete [C] (partial)
2. Explore [D] (uncharted)
3. Revisit [B.2] if [B.1] findings pan out

**Starting Point**: Resume at [C] to complete partial work
```

## Operator Decision Handling

| Operator Says | Your Response |
|---------------|---------------|
| "Dive deeper" | Note position, explore sub-branch, backtrack after |
| "Move on" | Mark status, show next branch and remaining |
| "Skip this" | Mark as SKIPPED, note reason, move to next |
| "Stop" | Stop immediately, document explored + uncharted |
| "Go back" | Return to previous branch, show status |

## Usage Examples

```bash
# Basic workshop
/workshop-facilitator:workshop "Product roadmap planning"

# With explicit goal
/workshop-facilitator:workshop "Customer pain points" --goal "chart everything"

# Focused exploration
/workshop-facilitator:workshop "API design options" --focus "authentication approaches"
```

## Getting Started

Let's begin!

1. What topic or challenge would you like to explore?
2. What does success look like - chart everything, or focus on specific areas?
3. Any relevant context I should know?
