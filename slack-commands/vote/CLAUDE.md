# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Slack voting bot deployed as Firebase Cloud Functions. Users create polls via a slash command (`/투표 옵션1, 옵션2, 옵션3`), and Slack users vote by clicking buttons in the resulting message.

## Deployment Commands

```bash
# Authenticate with Firebase
firebase login

# Set required secrets (first time only)
firebase functions:secrets:set SLACK_SIGNING_SECRET
firebase functions:secrets:set SLACK_BOT_TOKEN

# Deploy
firebase deploy --only functions

# View logs
firebase functions:log --only slack_vote
firebase functions:log --only slack_vote_interactive
```

There are no build, test, or lint scripts — this is a pure serverless Python project.

## Architecture

**Two Firebase Cloud Functions** (in `functions/main.py`):
- `slack_vote` — handles the `/투표` slash command, parses comma-separated options, and posts the initial Block Kit message
- `slack_vote_interactive` — handles button click payloads, toggles the user's vote, and updates the message in-place

**Vote state is stored in the Slack message itself** (no database). Each button's `value` field holds a JSON payload: `{"idx": 0, "opt": "option name", "v": ["user_id1", "user_id2"]}`. This means votes are lost if the message is deleted.

**Key module responsibilities:**
- `vote_service.py` — all voting logic and Block Kit UI construction (`parse_options`, `create_vote_blocks`, `update_vote_blocks`, `toggle_vote`)
- `slack_utils.py` — Slack API calls (`update_message`) and HMAC-SHA256 request signature verification with 5-minute replay protection
- `firebase.json` / `.firebaserc` — Firebase project configuration (`.firebaserc` contains the project ID and must be set before deploying)

## Constraints

- 2–10 options per poll
- Max ~150 votes per option (limited by Slack's 2000-char button value field)
- Max 50 characters per option text
