# Fetch failed test cases from CircleCI job URLs

# Run with a CircleCI job URL
run *urls:
    uv run python main.py {{urls}}

# Install globally via uv tool (provides `circleci-failcases` command)
install:
    uv tool install . --force

# Uninstall global command
uninstall:
    uv tool uninstall cubrid-circleci-failcases-fetcher

# Install dependencies
sync:
    uv sync

# Example with a real URL
example:
    uv run python main.py "https://app.circleci.com/pipelines/github/CUBRID/cubrid/26882/workflows/b7dfb704-d6f1-4fef-8507-aefd95439843/jobs/118600"
