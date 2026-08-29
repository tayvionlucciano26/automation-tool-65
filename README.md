# automation-tool-65

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

automation-tool-65 is a Python-based automation utility that executes predefined tasks for file handling, data processing, and service integrations. Users can configure custom workflows that run manually or according to time-based schedules.

## Features
- Create workflows in YAML to chain file operations, HTTP requests, and shell commands
- Schedule automations using cron expressions or fixed intervals
- Automatic retries with exponential backoff for failed tasks
- Execution reports exported as JSON with optional Slack webhook notifications

## Installation

```bash
git clone https://github.com/Developer/automation-tool-65.git
cd automation-tool-65
pip install -r requirements.txt
```

## Usage

Create a `workflow.yaml` file:

```yaml
tasks:
  - name: backup
    type: file_copy
    source: ./data
    destination: ./backup
  - name: sync
    type: http_post
    url: https://api.example.com/update
```

Run the workflow:

```bash
automation-tool-65 run workflow.yaml
```