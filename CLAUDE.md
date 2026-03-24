# cubrid-circleci-failcases-fetcher

CLI tool that extracts failed test cases from CircleCI job URLs.

## Setup

```bash
uv sync
export CIRCLECI_TOKEN="your-token"
```

## Usage

```bash
uv run python main.py <circleci-job-url> [<url2> ...]
```

Example:
```bash
uv run python main.py "https://app.circleci.com/pipelines/github/CUBRID/cubrid/26882/workflows/b7dfb704-d6f1-4fef-8507-aefd95439843/jobs/118600"
```

## Architecture

- Single-file CLI tool (`main.py`)
- Parses CircleCI job URLs to extract project slug and job number
- Uses CircleCI API v2 `GET /project/{slug}/{job}/tests` with pagination
- Requires `CIRCLECI_TOKEN` env var for authentication
- Filters tests where `result` is not `success` or `skipped`
