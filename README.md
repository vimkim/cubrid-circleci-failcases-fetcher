# cubrid-circleci-failcases-fetcher

Fetch failed test cases from CircleCI job URLs for CUBRID CI pipelines.

## Setup

```bash
uv sync
```

## Usage

```bash
just run <circleci-job-url>
```

Example:

```bash
just run "https://app.circleci.com/pipelines/github/CUBRID/cubrid/26882/workflows/b7dfb704-d6f1-4fef-8507-aefd95439843/jobs/118600"
```

Multiple URLs:

```bash
just run "https://...jobs/118600" "https://...jobs/118601"
```

## Output

Failed test details are printed to stdout, and test case paths are saved to `failed_tc.txt`:

```
cubrid-testcases-private-ex/blob/develop/shell/_06_issues/_14_1h/bug_bts_12381/cases/bug_bts_12381.sh
cubrid-testcases-private-ex/blob/develop/shell/_06_issues/_15_1h/bug_bts_16011/cases/bug_bts_16011.sh
...
```

## Authentication

No token required for public projects (e.g., CUBRID/cubrid). For private projects, set:

```bash
export CIRCLECI_TOKEN="your-circleci-api-token"
```
