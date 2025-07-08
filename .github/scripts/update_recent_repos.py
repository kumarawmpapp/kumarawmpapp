import os
import requests

USERNAME = os.environ["GH_USERNAME"]
TOKEN = os.environ["GH_TOKEN"]
API_URL = f"https://api.github.com/users/{USERNAME}/repos?type=owner&sort=updated"

def get_recent_repos(username, token, max_repos=10):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    repos_data = response.json()

    repos = []
    for repo in repos_data:
        if repo["fork"] || repo["archived"]:
            continue  # Skip forked repos

        name = repo["name"]
        url = repo["html_url"]
        description = repo["description"] or "(no description yet)"
        repos.append((name, url, description))

        if len(repos) >= max_repos:
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
        print("❌ Markers not found in README.md")
        return

    repo_lines = [""]
    for name, url, description in repos:
        repo_lines.append(f"➤ [{name}]({url}) — {description}")

    new_section = f"{start_marker}\n" + "\n".join(repo_lines) + f"\n{end_marker}"
    new_content = content[:start] + new_section + content[end + len(end_marker):]

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    repos = get_recent_repos(USERNAME, TOKEN)
    update_readme(repos)

if __name__ == "__main__":
    main()
