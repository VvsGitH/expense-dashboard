# Issue tracker: Local Markdown

Issues and specs (you may know a spec as a PRD) for this repo live as markdown files under `docs/issues/`.

## Conventions

- One feature per directory: `docs/issues/<feature-slug>/`
- The spec is `docs/issues/<feature-slug>/spec.md`
- Implementation tickets are one file per ticket at `docs/issues/<feature-slug>/<NN>-<slug>.md`, numbered from `01` — never a single combined tickets file
- Ticket status is recorded as a `Status:` line near the top of each file (e.g. `ready-for-agent`, `in-progress`, `done`)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `docs/issues/<feature-slug>/` (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.
