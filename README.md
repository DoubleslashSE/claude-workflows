# Claude Code Plugin Marketplace

A collection of plugins for [Claude Code](https://claude.com/claude-code) that extend its capabilities with specialized workflows, skills, and agents.

## Available Plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [dotnet-tdd](./plugins/dotnet-tdd) | Test-Driven Development for .NET with SOLID, DRY, KISS, YAGNI, and CQS principles | 1.0.0 |

## Installation

Install a plugin by pointing Claude Code to the plugin directory:

```bash
claude --plugin-dir ./plugins/dotnet-tdd
```

## Repository Structure

```
plugins/
├── dotnet-tdd/              # .NET TDD plugin
│   ├── .claude-plugin/
│   │   └── plugin.json      # Plugin manifest
│   ├── agents/              # Specialized agents
│   ├── commands/            # Slash commands
│   ├── hooks/               # Event hooks
│   ├── skills/              # Domain knowledge
│   └── README.md
└── [future-plugins]/
```

## Plugin Anatomy

Each plugin follows a standard structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Required: Plugin manifest
├── agents/              # Optional: Subagent definitions
├── commands/            # Optional: Slash commands
├── hooks/               # Optional: Event hooks
├── skills/              # Optional: Knowledge files
└── README.md            # Plugin documentation
```

### plugin.json

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What the plugin does",
  "keywords": ["relevant", "tags"],
  "commands": ["./commands/command.md"],
  "agents": ["./agents/agent.md"],
  "skills": ["./skills/skill-name"],
  "hooks": "./hooks/hooks.json"
}
```

## Contributing

Want to add a plugin? Submit a PR with your plugin in the `plugins/` directory following the structure above.

## License

MIT
