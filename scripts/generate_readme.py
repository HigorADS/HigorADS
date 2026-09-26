#!/usr/bin/env python3
"""Generate the editable selected-projects section in the profile README."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PROJECTS = ROOT / "projects.json"
START = "<!-- SELECTED_PROJECTS:START -->"
END = "<!-- SELECTED_PROJECTS:END -->"


def render_project(project: dict) -> str:
    name = project["name"]
    emoji = project.get("emoji", "📁")
    url = project["url"]
    description = project["description"]
    tags = " ".join(f"<code>{tag}</code>" for tag in project.get("tags", []))
    return f'''    <td width="50%" valign="top">
      <h3><a href="{url}">{emoji} {name}</a></h3>
      <p>{description}</p>
      <p>{tags}</p>
    </td>'''


def render_section(projects: list[dict]) -> str:
    if not projects:
        return f"{START}\n## 📌 Projetos selecionados\n\n*Ainda não há projetos selecionados.*\n{END}"

    rows = []
    for index in range(0, len(projects), 2):
        cells = [render_project(project) for project in projects[index:index + 2]]
        if len(cells) == 1:
            cells.append('    <td width="50%" valign="top"></td>')
        rows.append("  <tr>\n" + "\n".join(cells) + "\n  </tr>")

    table = "<table>\n" + "\n".join(rows) + "\n</table>"
    return f"{START}\n## 📌 Projetos selecionados\n{table}\n{END}"


def main() -> None:
    projects = json.loads(PROJECTS.read_text(encoding="utf-8"))
    readme = README.read_text(encoding="utf-8")
    generated = render_section(projects)

    if START in readme and END in readme:
        before = readme.split(START, 1)[0]
        after = readme.split(END, 1)[1]
        readme = before + generated + after
    else:
        marker = "## 🌱 Próximos passos"
        readme = readme.replace(marker, generated + "\n" + marker, 1)

    README.write_text(readme, encoding="utf-8")


if __name__ == "__main__":
    main()
