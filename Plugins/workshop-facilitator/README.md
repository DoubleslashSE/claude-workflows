# Workshop Facilitator Plugin

A Claude Code plugin for facilitating design thinking and brainstorming workshops through a single operator. Features exploration tracking with mind mapping, automatic backtracking after deep dives, and documentation of both explored findings and uncharted territory.

## Key Concept: Single Operator Model

This plugin works through a **single operator** who may represent themselves or a group of any size (0 or more people behind them).

- **Operator decides** → That IS the group's decision
- **Operator says "dive deeper"** → We dive deeper, then backtrack
- **Operator says "move on"** → We move on
- **Operator says "stop"** → We stop and document immediately
- **The operator** handles ensuring all voices in their group are heard

Your job as facilitator: Guide exploration systematically, track territory, backtrack after deep dives, document everything.

## Core Features

### Exploration Tracking (Mind Map)

Every session maintains a visual map of the exploration territory:

```
[TOPIC]
├─ [Branch A] ──────────── ✓ EXPLORED
│  └─ 7 ideas captured
├─ [Branch B] ──────────── ✓ EXPLORED
│  ├─ [B.1] ─────────────── ✓ EXPLORED (deep dive)
│  └─ [B.2] ─────────────── ⊘ SKIPPED
├─ [Branch C] ──────────── ◐ PARTIAL
└─ [Branch D] ──────────── ○ UNCHARTED
```

**Status Key:**
- ✓ EXPLORED - Fully covered, findings documented
- ◐ PARTIAL - Started but not complete
- ○ UNCHARTED - Not explored this session
- ⊘ SKIPPED - Operator chose to skip
- → CURRENT - Currently exploring

### Automatic Backtracking

After every deep dive, the facilitator automatically:
1. Announces return to the parent level
2. Shows remaining unexplored siblings
3. Shows remaining main branches
4. Asks operator for direction

### Documentation of Uncharted Territory

Every session document MUST include:
- **Explored findings** - What we learned
- **Uncharted territory** - What we didn't explore and why
- **Future recommendations** - Where to start next time

**No silent omissions** - if a branch was identified but not explored, it's documented.

## Quick Start

```bash
# Run a general workshop
/workshop-facilitator:workshop "Product strategy planning"

# Design thinking workshop
/workshop-facilitator:design-thinking "Improve customer onboarding"

# Brainstorming session
/workshop-facilitator:brainstorm "Marketing campaign ideas"
```

## Workshop Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              EXPLORATION-BASED WORKSHOP FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. TERRITORY MAPPING                                           │
│     ├─ Clarify objectives and scope                             │
│     ├─ Identify major branches to explore                       │
│     └─ Validate map with operator                               │
│                                                                 │
│  2. SYSTEMATIC EXPLORATION                                      │
│     FOR EACH BRANCH:                                            │
│     ├─ Generate ideas/insights                                  │
│     ├─ Identify sub-branches                                    │
│     └─ Checkpoint: dive deeper or move on?                      │
│                                                                 │
│     IF DIVE DEEPER:                                             │
│     ├─ Note position for backtrack                              │
│     ├─ Explore sub-branch                                       │
│     └─ BACKTRACK: Return and show remaining                     │
│                                                                 │
│  3. CONVERGENCE (when operator ready)                           │
│     ├─ Synthesize findings                                      │
│     └─ Define actions                                           │
│                                                                 │
│  4. DOCUMENTATION                                               │
│     ├─ Document EXPLORED territory                              │
│     ├─ Document UNCHARTED territory                             │
│     └─ Recommend future starting points                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Checkpoint Protocol

At every checkpoint, the facilitator shows:

```markdown
**Checkpoint: [Current Branch]**

**Just completed**: [What we explored]
**Captured**: [N] ideas/insights

**Current Map**:
[Visual tree with statuses]

**Options**:
1. Dive deeper into [sub-area]
2. Move to [next branch]
3. Stop and document current state
```

## Commands

| Command | Description |
|---------|-------------|
| `/workshop-facilitator:workshop` | Complete workshop with exploration tracking |
| `/workshop-facilitator:design-thinking` | Design thinking (Empathize→Define→Ideate→Prototype→Test) |
| `/workshop-facilitator:brainstorm` | Focused brainstorming session |
| `/workshop-facilitator:synthesize` | Synthesize and prioritize existing ideas |

## Agents

| Agent | Role |
|-------|------|
| `session-planner` | Designs workshop structure and initial territory map |
| `facilitator` | Runs sessions with exploration tracking and backtracking |
| `synthesizer` | Groups ideas, identifies patterns across branches |
| `documenter` | Creates artifacts with explored + uncharted documentation |

## Skills

| Skill | Content |
|-------|---------|
| `design-thinking` | 5-phase methodology, empathy mapping, HMW |
| `brainstorming` | SCAMPER, brainwriting, diverge/converge |
| `facilitation-techniques` | Questioning, energy management |
| `session-documentation` | Artifact templates, capture techniques |
| `exploration-tracking` | Mind mapping, backtracking, territory status |

## Example Session Flow

```
Operator: Let's explore "improving developer productivity"

Facilitator: Here's the territory map I see:

[Developer Productivity]
├─ [Tooling] ──────────── ○ UNCHARTED
├─ [Processes] ─────────── ○ UNCHARTED
├─ [Environment] ────────── ○ UNCHARTED
└─ [Skills/Training] ────── ○ UNCHARTED

Does this capture the territory? Where should we start?

Operator: Start with Tooling

Facilitator: Exploring Tooling...
[generates ideas]

Checkpoint: We have 8 ideas. I see sub-branches:
- IDE/Editor optimization
- Build systems
- Testing tools

Dive deeper, move on, or stop?

Operator: Dive into IDE/Editor

Facilitator: [Notes position for backtrack]
Diving into IDE/Editor...
[explores deeper]

BACKTRACK: We've explored IDE/Editor. Remaining:
- Build systems (sibling)
- Testing tools (sibling)
- Processes, Environment, Skills (main branches)

Continue exploring Tooling siblings, or move on?

Operator: Move to Processes

Facilitator: Marking Tooling as PARTIAL (explored IDE, skipped Build/Testing)
Moving to Processes...

[Session continues]

Operator: Stop here

Facilitator:
## Final Map
[Developer Productivity]
├─ [Tooling] ──────────── ◐ PARTIAL
│  ├─ [IDE/Editor] ─────── ✓ EXPLORED (deep dive)
│  ├─ [Build systems] ──── ○ UNCHARTED
│  └─ [Testing tools] ──── ○ UNCHARTED
├─ [Processes] ─────────── ✓ EXPLORED
├─ [Environment] ────────── ○ UNCHARTED
└─ [Skills/Training] ────── ○ UNCHARTED

## Explored: [findings]
## Uncharted: [Build systems, Testing tools, Environment, Skills]
## Recommended next session: Complete Tooling, then Environment
```

## Documentation Output

Every session produces documentation that includes:

1. **Exploration Map** - Visual tree with all branches and status
2. **Explored Territory** - Detailed findings per branch
3. **Uncharted Territory** - Explicit list of what wasn't explored
4. **Decisions & Actions** - What was decided, who owns what
5. **Future Recommendations** - Where to start next time

## Plugin Structure

```
workshop-facilitator/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── session-planner.md
│   ├── facilitator.md      # Single operator, exploration tracking
│   ├── synthesizer.md
│   └── documenter.md       # Explored + uncharted documentation
├── commands/
│   ├── workshop.md
│   ├── design-thinking.md
│   ├── brainstorm.md
│   └── synthesize.md
├── skills/
│   ├── design-thinking/
│   ├── brainstorming/
│   ├── facilitation-techniques/
│   ├── session-documentation/
│   └── exploration-tracking/  # Mind mapping, backtracking
├── hooks/
│   └── hooks.json
└── README.md
```

## Sources & Research

Workshop facilitation best practices from:
- [SessionLab Facilitation Library](https://www.sessionlab.com/library)
- [The Ultimate Guide to Workshop Facilitation](https://www.workshopper.com/post/the-ultimate-guide-to-facilitation)
- [2025 Facilitation Rules](https://www.edufellowship.com/blog/facilitation-workshop-design-2025/)
- [Design Thinking Workshop Guide](https://careerfoundry.com/en/blog/ux-design/design-thinking-workshop/)

## Version History

### v1.0.0
- Initial release with single-operator model
- Exploration tracking with mind mapping
- Automatic backtracking after deep dives
- Documentation of explored + uncharted territory
- Design thinking and brainstorming workshops

## Author

DoubleslashSE (info@doubleslash.se)
