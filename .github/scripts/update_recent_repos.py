import os
import requests
from datetime import datetime

USERNAME = os.environ["GH_USERNAME"]
TOKEN = os.environ["GH_TOKEN"]
API_URL = f"https://api.github.com/users/{USERNAME}/events/public"

def get_recent_repos(username, token, max_repos=5):
    headers = {"Authorization": f"token {token}"}
    r = requests.get(API_URL, headers=headers)
    r.raise_for_status()
    events = r.json()
    repos = []
    seen = set()

    for event in events:
        repo_name = event["repo"]["name"]
        if repo_name not in seen:
            seen.add(repo_name)
            repos.append(repo_name)
        if len(repos) == max_repos:
            break
    return repos

def update_readme(repos):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- RECENT_REPOS_START -->"
    end_marker = "<!-- RECENT_REPOS_END -->"
    start = content.find(start_marker)
    end = content.find(end_marker)
    if start == -1 or end == -1:
        print("Markers not found in README.md")
        return

    repo_lines = []
    for repo in repos:
        repo_url = f"https://github.com/{repo}"
        repo_lines.append(f"- [{repo}]({repo_url})")

    new_section = f"{start_marker}\n" + "\n".join(repo_lines) + f"\n{end_marker}"
    new_content = content[:start] + new_section + content[end+len(end_marker):]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    repos = get_recent_repos(USERNAME, TOKEN)
    update_readme(repos)

if __name__ == "__main__":
    main()
