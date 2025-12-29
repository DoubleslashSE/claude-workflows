#!/usr/bin/env python3
"""
Workflow State Management

Provides utilities for managing workflow state across sessions:
- Load/save workflow state
- Update story status
- Track checkpoints
- Validate state consistency

State file: .claude/workflow-state.json
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any


STATE_FILE = Path('.claude/workflow-state.json')


def generate_workflow_id() -> str:
    """Generate a unique workflow ID."""
    return str(uuid.uuid4())[:8]


def now_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def create_initial_state(goal: str, session_id: str = None) -> Dict[str, Any]:
    """Create a new workflow state."""
    return {
        'workflowId': generate_workflow_id(),
        'sessionId': session_id or 'unknown',
        'startedAt': now_iso(),
        'lastUpdated': now_iso(),
        'goal': goal,
        'status': 'in_progress',
        'currentPhase': 'analysis',
        'currentAgent': 'orchestrator',
        'stories': [],
        'decisions': [],
        'checkpoints': {
            'lastHumanReview': now_iso(),
            'storiesSinceReview': 0,
            'failedAttempts': 0
        },
        'blockers': []
    }


def load_state() -> Optional[Dict[str, Any]]:
    """Load workflow state from file."""
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, IOError):
        return None


def save_state(state: Dict[str, Any]) -> bool:
    """Save workflow state to file."""
    state['lastUpdated'] = now_iso()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding='utf-8')
        return True
    except IOError:
        return False


def initialize_workflow(goal: str, session_id: str = None) -> Dict[str, Any]:
    """Initialize a new workflow or return existing if active."""
    existing = load_state()
    if existing and existing.get('status') == 'in_progress':
        # Resume existing workflow
        existing['sessionId'] = session_id or existing.get('sessionId')
        save_state(existing)
        return existing

    # Create new workflow
    state = create_initial_state(goal, session_id)
    save_state(state)
    return state


def add_story(
    title: str,
    size: str = 'M',
    acceptance_criteria: List[str] = None
) -> str:
    """Add a new story to the workflow. Returns story ID."""
    state = load_state()
    if not state:
        raise ValueError('No active workflow. Call initialize_workflow first.')

    story_num = len(state['stories']) + 1
    story_id = f'S{story_num}'

    story = {
        'id': story_id,
        'title': title,
        'size': size,
        'status': 'pending',
        'acceptanceCriteria': acceptance_criteria or [],
        'assignedAgent': None,
        'attempts': 0,
        'createdAt': now_iso(),
        'lastUpdated': now_iso()
    }

    state['stories'].append(story)
    save_state(state)
    return story_id


def update_story_status(
    story_id: str,
    status: str,
    agent: str = None
) -> bool:
    """Update a story's status."""
    state = load_state()
    if not state:
        return False

    for story in state['stories']:
        if story['id'] == story_id:
            story['status'] = status
            story['lastUpdated'] = now_iso()
            if agent:
                story['assignedAgent'] = agent
            if status == 'in_progress':
                story['attempts'] = story.get('attempts', 0) + 1

            # Update checkpoint counter
            if status == 'completed':
                state['checkpoints']['storiesSinceReview'] += 1

            save_state(state)
            return True

    return False


def update_phase(phase: str, agent: str = None) -> bool:
    """Update the current workflow phase."""
    state = load_state()
    if not state:
        return False

    state['currentPhase'] = phase
    if agent:
        state['currentAgent'] = agent
    save_state(state)
    return True


def add_decision(title: str, choice: str, rationale: str) -> str:
    """Record an architecture decision."""
    state = load_state()
    if not state:
        raise ValueError('No active workflow.')

    decision_num = len(state['decisions']) + 1
    decision_id = f'ADR-{decision_num:03d}'

    decision = {
        'id': decision_id,
        'title': title,
        'choice': choice,
        'rationale': rationale,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'accepted'
    }

    state['decisions'].append(decision)
    save_state(state)
    return decision_id


def add_blocker(description: str, severity: str = 'medium') -> None:
    """Add a blocker to the workflow."""
    state = load_state()
    if not state:
        return

    blocker = {
        'description': description,
        'severity': severity,
        'createdAt': now_iso(),
        'resolved': False
    }

    state['blockers'].append(blocker)
    state['status'] = 'blocked'
    save_state(state)


def resolve_blocker(index: int) -> bool:
    """Resolve a blocker by index."""
    state = load_state()
    if not state or index >= len(state['blockers']):
        return False

    state['blockers'][index]['resolved'] = True
    state['blockers'][index]['resolvedAt'] = now_iso()

    # Check if any unresolved blockers remain
    if not any(b for b in state['blockers'] if not b['resolved']):
        state['status'] = 'in_progress'

    save_state(state)
    return True


def should_checkpoint() -> bool:
    """Check if human review checkpoint is needed."""
    state = load_state()
    if not state:
        return False

    checkpoints = state.get('checkpoints', {})
    return checkpoints.get('storiesSinceReview', 0) >= 5


def record_human_review() -> None:
    """Record that a human review checkpoint occurred."""
    state = load_state()
    if not state:
        return

    state['checkpoints']['lastHumanReview'] = now_iso()
    state['checkpoints']['storiesSinceReview'] = 0
    save_state(state)


def complete_workflow() -> bool:
    """Mark the workflow as completed."""
    state = load_state()
    if not state:
        return False

    state['status'] = 'completed'
    state['completedAt'] = now_iso()
    save_state(state)
    return True


def get_workflow_summary() -> Dict[str, Any]:
    """Get a summary of the current workflow state."""
    state = load_state()
    if not state:
        return {'error': 'No active workflow'}

    stories = state.get('stories', [])
    completed = sum(1 for s in stories if s['status'] == 'completed')
    in_progress = sum(1 for s in stories if s['status'] == 'in_progress')
    pending = sum(1 for s in stories if s['status'] == 'pending')

    return {
        'workflowId': state.get('workflowId'),
        'goal': state.get('goal'),
        'status': state.get('status'),
        'currentPhase': state.get('currentPhase'),
        'currentAgent': state.get('currentAgent'),
        'progress': {
            'total': len(stories),
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'percentage': round(completed / len(stories) * 100) if stories else 0
        },
        'checkpointDue': should_checkpoint(),
        'blockers': [b for b in state.get('blockers', []) if not b['resolved']]
    }


# CLI interface for testing
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: python state.py <command> [args]')
        print('Commands: init, status, add-story, update-story, complete')
        sys.exit(1)

    command = sys.argv[1]

    if command == 'init':
        goal = sys.argv[2] if len(sys.argv) > 2 else 'Test workflow'
        state = initialize_workflow(goal)
        print(f'Initialized workflow: {state["workflowId"]}')

    elif command == 'status':
        summary = get_workflow_summary()
        print(json.dumps(summary, indent=2))

    elif command == 'add-story':
        title = sys.argv[2] if len(sys.argv) > 2 else 'New Story'
        story_id = add_story(title)
        print(f'Added story: {story_id}')

    elif command == 'update-story':
        story_id = sys.argv[2] if len(sys.argv) > 2 else 'S1'
        status = sys.argv[3] if len(sys.argv) > 3 else 'completed'
        update_story_status(story_id, status)
        print(f'Updated {story_id} to {status}')

    elif command == 'complete':
        complete_workflow()
        print('Workflow completed')

    else:
        print(f'Unknown command: {command}')
        sys.exit(1)
