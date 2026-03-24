#!/usr/bin/env python3
"""Fetch failed test cases from a CircleCI job URL."""

import os
import re
import sys

import requests


def parse_circleci_url(url: str) -> tuple[str, int]:
    """Parse a CircleCI job URL and return (project_slug, job_number).

    Expected URL format:
    https://app.circleci.com/pipelines/github/ORG/REPO/PIPELINE/workflows/WF_ID/jobs/JOB_NUM
    """
    pattern = (
        r"https?://app\.circleci\.com/pipelines/"
        r"(github|bitbucket|gitlab)/([^/]+)/([^/]+)"
        r"/\d+/workflows/[^/]+/jobs/(\d+)"
    )
    m = re.match(pattern, url)
    if not m:
        raise ValueError(f"Invalid CircleCI job URL: {url}")

    vcs_map = {"github": "gh", "bitbucket": "bb", "gitlab": "gl"}
    vcs_slug = vcs_map[m.group(1)]
    org = m.group(2)
    repo = m.group(3)
    job_number = int(m.group(4))

    project_slug = f"{vcs_slug}/{org}/{repo}"
    return project_slug, job_number


def fetch_failed_tests(project_slug: str, job_number: int, token: str = "") -> list[dict]:
    """Fetch all test results from a CircleCI job and return only failures."""
    url = f"https://circleci.com/api/v2/project/{project_slug}/{job_number}/tests"
    headers = {"Circle-Token": token} if token else {}
    failed = []
    page_token = None

    while True:
        params = {}
        if page_token:
            params["page-token"] = page_token

        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

        items = data.get("items", [])
        if not items and page_token is None:
            print("Warning: no test results returned (job may have no test metadata).",
                  file=sys.stderr)

        for t in items:
            if t.get("result") not in ("success", "skipped"):
                failed.append(t)

        page_token = data.get("next_page_token")
        if not page_token:
            break

    return failed


def extract_tc_path(t: dict) -> str:
    """Extract the test case path from classname, stripping the GitHub URL prefix."""
    classname = t.get("classname", "")
    prefix = "https://github.com/CUBRID/"
    if classname.startswith(prefix):
        return classname[len(prefix):]
    return t.get("file", classname)


def format_test(t: dict) -> str:
    """Format a single failed test for display."""
    parts = []
    if t.get("classname"):
        parts.append(f"  class:   {t['classname']}")
    if t.get("name"):
        parts.append(f"  name:    {t['name']}")
    if t.get("file"):
        parts.append(f"  file:    {t['file']}")
    if t.get("result"):
        parts.append(f"  result:  {t['result']}")
    if t.get("run_time") is not None:
        parts.append(f"  time:    {t['run_time']:.3f}s")
    if t.get("message"):
        msg = t["message"]
        if len(msg) > 500:
            msg = msg[:500] + "..."
        parts.append(f"  message: {msg}")
    return "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <circleci-job-url> [<url2> ...]", file=sys.stderr)
        sys.exit(1)

    token = os.environ.get("CIRCLECI_TOKEN", "")

    for url in sys.argv[1:]:
        print(f"=== {url} ===")
        try:
            project_slug, job_number = parse_circleci_url(url)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            continue

        print(f"Project: {project_slug}, Job: {job_number}")

        try:
            failed = fetch_failed_tests(project_slug, job_number, token)
        except requests.HTTPError as e:
            print(f"API error: {e}", file=sys.stderr)
            continue

        if not failed:
            print("No failed tests found.")
        else:
            print(f"\n{len(failed)} failed test(s):\n")
            for i, t in enumerate(failed, 1):
                print(f"[{i}]")
                print(format_test(t))
                print()

            # Save test case paths to failed_tc.txt
            outfile = "failed_tc.txt"
            with open(outfile, "w") as f:
                for t in failed:
                    f.write(extract_tc_path(t) + "\n")
            print(f"Saved to {outfile}")


if __name__ == "__main__":
    main()
