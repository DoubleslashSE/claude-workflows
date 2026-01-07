---
description: Execute business analysis for an existing codebase. Reverse-engineers requirements from code, identifies gaps, and gathers change requirements from stakeholders.
---

# Brownfield Project Analysis

Execute existing codebase analysis for: **$ARGUMENTS**

## Brownfield Overview

This command is optimized for projects involving existing systems. The workflow combines codebase analysis to understand current capabilities with stakeholder interviews to identify desired changes and improvements.

## Brownfield Workflow

### Phase 1: Codebase Discovery (20 min)

**Project Structure Analysis**
1. Identify technology stack
2. Map project organization
3. Identify architectural patterns
4. Locate key components

**Initial Questions**
- What path should I analyze?
- Are there multiple services/components?
- Is there existing documentation to review?

### Phase 2: Domain Model Extraction (30 min)

**Entity Discovery**
1. Identify domain entities
2. Map relationships
3. Document attributes and constraints
4. Identify aggregate boundaries

**Documentation Format**
```markdown
## Entity: {Name}
- Attributes: {list}
- Relationships: {list}
- Business meaning: {description}
- Location: {file path}
```

### Phase 3: Business Rules Discovery (30 min)

**Rule Identification**
1. Find validation logic
2. Identify calculations/formulas
3. Map workflows and state machines
4. Document business constraints

**Rule Categories**
- Validation rules
- Calculation rules
- State transition rules
- Authorization rules

### Phase 4: Integration Mapping (20 min)

**External Systems**
1. Identify API endpoints (exposed)
2. Find external service calls
3. Map message queue usage
4. Document data flows

**Documentation Format**
```markdown
## Integration: {Name}
- Type: API / Message Queue / File / Database
- Direction: Inbound / Outbound / Bidirectional
- Data: {what flows}
- Location: {file path}
```

### Phase 5: Capability Documentation (15 min)

**Current State Summary**
1. What can users do today?
2. What data does the system manage?
3. What integrations exist?
4. What business processes are supported?

### Phase 6: Stakeholder Interview (30 min)

**Current State Questions**
1. What works well in the current system?
2. What are the biggest pain points?
3. What workarounds do people use?
4. What's missing?

**Change Requirements**
1. What needs to change?
2. What new features are needed?
3. What should be removed/deprecated?
4. What performance improvements are needed?

**Migration Considerations**
1. What data needs to be preserved?
2. Can we run parallel systems?
3. What is the cutover strategy?
4. What training is needed?

### Phase 7: Gap Analysis (15 min)

**As-Is vs To-Be**
1. Document current capabilities
2. Document desired capabilities
3. Identify gaps
4. Categorize: New / Changed / Removed

**Technical Debt Assessment**
1. Code quality issues
2. Outdated dependencies
3. Security vulnerabilities
4. Performance bottlenecks

### Phase 8: Prioritization (15 min)

**Change Prioritization**
Using MoSCoW:
- **Must Have**: Critical changes/fixes
- **Should Have**: Important improvements
- **Could Have**: Nice to have enhancements
- **Won't Have**: Deferred to future

### Phase 9: Validation and Documentation (20 min)

**Validation Checkpoint**
1. Verify codebase findings with stakeholder
2. Confirm change requirements
3. Validate priorities
4. Identify risks

**Documentation**
1. Generate as-is requirements
2. Document change requirements
3. Create gap analysis report
4. Produce SRS document

## User Checkpoints

I will pause for your confirmation at:

1. **After Structure Discovery**: "Does this architecture overview match your understanding?"
2. **After Domain Extraction**: "Are these the main business entities?"
3. **After Business Rules**: "Did I capture the business rules correctly?"
4. **After Integration Mapping**: "Are these all the integrations?"
5. **After Stakeholder Interview**: "Have I captured all the desired changes?"
6. **After Gap Analysis**: "Is this gap assessment accurate?"
7. **Before Documentation**: "Ready to generate the SRS?"

## Expected Outputs

1. **Codebase Analysis Report**
   - Technology stack overview
   - Architecture pattern identification
   - Domain model documentation
   - Business rules inventory
   - Integration map

2. **As-Is Requirements Document**
   - Current capabilities
   - Current business rules
   - Current integrations

3. **Change Requirements**
   - New requirements
   - Modified requirements
   - Deprecated features

4. **Gap Analysis Report**
   - Current vs desired state
   - Prioritized gaps
   - Technical debt assessment

5. **SRS Document**
   - IEEE 830 compliant
   - Includes both as-is and to-be

6. **Migration Considerations**
   - Data migration needs
   - Cutover strategy
   - Risk assessment

7. **Validation Report**
   - Quality and completeness assessment

## Analysis Scope Options

**Full Analysis** (Recommended)
Analyze entire codebase and all aspects.

**Focused Analysis**
Target specific areas:
```
/business-analyst:brownfield ./src/auth
/business-analyst:brownfield ./api/orders
```

**Specific Aspects**
Focus on particular concerns:
```
/business-analyst:brownfield security audit
/business-analyst:brownfield integration mapping
/business-analyst:brownfield business rules
```

## Getting Started

Let's begin the brownfield analysis!

First, I need to know:
1. What is the path to the codebase to analyze?
2. What technology stack is used (if you know)?
3. What is the main reason for this analysis (enhancement, migration, audit)?
4. Are there specific areas of concern?
