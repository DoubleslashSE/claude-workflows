---
description: Synthesize and analyze ideas from a workshop or brainstorming session. Groups ideas into themes, identifies patterns, and creates prioritized summaries.
---

# Synthesize Ideas

Synthesize and analyze: **$ARGUMENTS**

## Synthesis Overview

Transform raw workshop outputs into organized, actionable insights:

```
┌─────────────────────────────────────────────────────────────────┐
│                   SYNTHESIS PROCESS                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  INPUT                    PROCESS                 OUTPUT        │
│  ┌──────────┐            ┌──────────┐            ┌──────────┐  │
│  │ Raw ideas│───────────▶│ Cluster  │───────────▶│ Themes   │  │
│  │ Notes    │            │ & Group  │            │ Insights │  │
│  │ Outputs  │            │          │            │ Priorities│  │
│  └──────────┘            └──────────┘            └──────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Input Collection

### What to Synthesize

Provide the raw materials:
- List of ideas generated
- Discussion notes
- Voting results
- Any categorizations already made

"Please share the ideas or workshop outputs you'd like me to synthesize."

## Step 1: Affinity Mapping

### Clustering Process

"I'll organize these [N] items into related clusters..."

```markdown
## Affinity Clusters

### Cluster 1: [Theme Name]
**Common Thread**: [What unifies these items]
- [Item A]
- [Item B]
- [Item C]

### Cluster 2: [Theme Name]
**Common Thread**: [What unifies these items]
- [Item D]
- [Item E]

### Cluster 3: [Theme Name]
...

### Unclustered Items
Items that don't fit patterns but may be significant:
- [Item X]: [Why it's notable]
```

### Checkpoint
"I've grouped the items into [N] clusters:
1. **[Cluster 1]**: [N] items - [Brief description]
2. **[Cluster 2]**: [N] items - [Brief description]
3. **[Cluster 3]**: [N] items - [Brief description]

Do these groupings make sense? Would you like to:
- **Reorganize** any items?
- **Merge or split** clusters?
- **Proceed** to pattern analysis?"

## Step 2: Pattern Analysis

### Identifying Patterns

"Looking across clusters, I see these patterns..."

```markdown
## Pattern Analysis

### Strong Patterns (Appear across multiple clusters)
1. **[Pattern Name]**
   - Evidence: [Where this appears]
   - Significance: [What this tells us]

2. **[Pattern Name]**
   - Evidence: [Where this appears]
   - Significance: [What this tells us]

### Emerging Patterns (Appear in a single cluster but notable)
1. **[Pattern Name]**
   - Evidence: [Where this appears]
   - Potential: [Why it might be significant]

### Tensions/Contradictions
- [Pattern A] vs [Pattern B]: [The tension]
- Resolution options: [How to reconcile]
```

### Checkpoint
"Key patterns I've identified:
- **[Pattern 1]**: [Brief description]
- **[Pattern 2]**: [Brief description]

Any patterns you see that I missed? Should we:
- **Explore** any pattern deeper?
- **Proceed** to insight extraction?"

## Step 3: Insight Extraction

### Generating Insights

"Based on clusters and patterns, here are the key insights..."

```markdown
## Key Insights

### Insight 1: [Title]
**Observation**: [What we noticed]
**So What**: [Why it matters]
**Now What**: [Recommended action]

### Insight 2: [Title]
**Observation**: [What we noticed]
**So What**: [Why it matters]
**Now What**: [Recommended action]

### Insight 3: [Title]
...
```

### Surprise Analysis
"What's surprising about these results?"

```markdown
## Surprises & Anomalies

### Expected but Absent
- [What we thought would appear but didn't]
- Possible reason: [Hypothesis]

### Unexpected Presence
- [What appeared that we didn't expect]
- Significance: [What this might mean]

### Intensity Surprises
- [Topic that got more/less attention than expected]
```

## Step 4: Priority Matrix

### Organizing by Impact/Effort

```markdown
## Priority Matrix

### Quick Wins (High Impact, Low Effort)
Do these first:
1. [Item] - [Why it's a quick win]
2. [Item] - [Why it's a quick win]

### Major Projects (High Impact, High Effort)
Plan these carefully:
1. [Item] - [Why it's worth the effort]
2. [Item] - [Why it's worth the effort]

### Fill-Ins (Low Impact, Low Effort)
Do if time permits:
1. [Item]
2. [Item]

### Deprioritize (Low Impact, High Effort)
Avoid unless circumstances change:
1. [Item] - [Why not now]
```

### Checkpoint
"Here's the priority assessment:
- **Quick Wins**: [N] items ready for immediate action
- **Major Projects**: [N] items needing planning
- **Fill-Ins**: [N] items for later
- **Deprioritize**: [N] items to avoid

Does this prioritization feel right? Should we adjust any items?"

## Step 5: Gap Analysis

### Identifying Missing Elements

```markdown
## Gap Analysis

### What's Missing?

**Unexplored Angles**:
- [Angle not covered]
- [Perspective not represented]

**Questions Unanswered**:
- [Question raised but not resolved]
- [Question that should have been asked]

**Follow-up Needed**:
- [Topic requiring more exploration]
- [Decision requiring more information]

### Recommendations
For a complete picture, consider:
1. [Recommendation for addressing gap]
2. [Recommendation for addressing gap]
```

## Final Synthesis Output

### Executive Summary

```markdown
# Synthesis Summary: [Topic]

## At a Glance
- **Total Items Analyzed**: [N]
- **Themes Identified**: [N]
- **Priority Items**: [N]
- **Key Insights**: [N]

## Main Themes
| Theme | Items | Strength | Top Idea |
|-------|-------|----------|----------|
| [Theme 1] | [N] | Strong | [Best item] |
| [Theme 2] | [N] | Medium | [Best item] |
| [Theme 3] | [N] | Emerging | [Best item] |

## Key Insights
1. **[Insight 1]**: [One-line summary with action]
2. **[Insight 2]**: [One-line summary with action]
3. **[Insight 3]**: [One-line summary with action]

## Top Priorities
| Priority | Item | Action | Owner |
|----------|------|--------|-------|
| 1 | [Item] | [Next step] | [Who] |
| 2 | [Item] | [Next step] | [Who] |
| 3 | [Item] | [Next step] | [Who] |

## Gaps to Address
- [Gap 1]: [Suggested follow-up]
- [Gap 2]: [Suggested follow-up]

## Next Steps
1. [Immediate action]
2. [Near-term action]
3. [Follow-up session if needed]
```

### Detailed Documentation

Full synthesis document with:
- Complete cluster contents
- All patterns identified
- Full insight write-ups
- Detailed priority rationale
- Comprehensive gap analysis

## Usage Examples

```bash
# Basic synthesis
/workshop-facilitator:synthesize "Our brainstorming notes"

# From file
/workshop-facilitator:synthesize --input workshop-notes.md

# Focus on prioritization
/workshop-facilitator:synthesize "Feature ideas" --focus priorities

# Include gap analysis
/workshop-facilitator:synthesize "Customer feedback" --include-gaps
```

## Getting Started

To begin synthesis, please share:
1. The ideas or outputs to synthesize
2. Any context about the original session
3. What kind of synthesis is most useful (themes, priorities, insights)
