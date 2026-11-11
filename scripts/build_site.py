"""Build the GitHub Pages paper explorer from the Markdown topic collections."""

import argparse
import hashlib
import html
import json
import re
import shutil
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/LuckyGirl-XU/Awesome-DynamicGraphLearning"
SITE_URL = "https://luckygirl-xu.github.io/Awesome-DynamicGraphLearning/"
TOPICS = {
    "continuous-time": "Continuous-time dynamic graphs",
    "discrete-time": "Discrete-time dynamic graphs",
    "text-attributed": "Dynamic text-attributed graphs",
    "anomaly-detection": "Anomaly detection",
    "temporal-hypergraphs": "Temporal hypergraphs",
    "streaming": "Streaming graph learning",
    "continual-learning": "Continual & open-world temporal graph learning",
    "unlearning": "Dynamic & temporal graph unlearning",
}
CTDG_TASKS = {
    "link-prediction": "Link Prediction",
    "node-affinity": "Node Affinity Prediction",
    "multi-task": "Multi-task Learning",
}
HIGHLIGHTS_START = "<!-- RECENT_PAPERS:START -->"
HIGHLIGHTS_END = "<!-- RECENT_PAPERS:END -->"


def normalize(title):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFKC", title)).casefold()


def read_catalog(root=ROOT):
    records = {}
    for topic in TOPICS:
        path = root / "papers" / (topic + ".md")
        section = None
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("## "):
                section = line[3:].strip()
            if not line.startswith("| ") or line.startswith(("| Paper |", "| ---")):
                continue
            cells = [html.unescape(cell.strip()) for cell in line.strip("|").split("|")]
            if len(cells) != 3 or not section:
                raise ValueError(f"Invalid paper row: {path}:{line_number}")
            title, venue, resources = cells
            year_match = re.search(r"\b(?:19|20)\d{2}\b", venue)
            year = int(section) if section.isdigit() else int(year_match[0]) if year_match else None
            venue = re.sub(r"\s*\b(?:19|20)\d{2}\b", "", venue).strip()
            links = []
            for label, url in re.findall(r"\[([^\]]+)\]\(([^\s]+)\)", resources):
                if urlsplit(url).scheme not in ("https", "http"):
                    raise ValueError(f"Unsupported resource URL: {path}:{line_number}")
                links.append({"label": label, "url": url})
            # A shared title/year can be cross-listed in different topics.
            # Different years stay distinct, preserving preprint/publication records.
            key = (normalize(title), year)
            if key not in records:
                digest = hashlib.sha256((key[0] + str(year)).encode()).hexdigest()[:12]
                records[key] = {"id": digest, "title": title, "year": year,
                                "venue": venue, "topics": [], "kinds": [],
                                "links": [], "sources": []}
            record = records[key]
            if record["venue"].lower().startswith("arxiv") and not venue.lower().startswith("arxiv"):
                record["venue"] = venue
            for field, value in (("topics", topic), ("kinds", section if not section.isdigit() else "Paper")):
                if value not in record[field]:
                    record[field].append(value)
            for link in links:
                if link not in record["links"]:
                    record["links"].append(link)
            record["sources"].append({"path": str(path.relative_to(root)), "line": line_number})
    papers = list(records.values())
    for paper in papers:
        paper["has_code"] = any(link["label"].lower().startswith("code") for link in paper["links"])
        paper["acronym"] = "TCSD" if any(link["url"] == "https://github.com/LuckyGirl-XU/TCSD" for link in paper["links"]) else ""
        paper["tasks"] = []
        if "continuous-time" in paper["topics"]:
            for task, pattern in (("link-prediction", r"link[ -]+prediction"),
                                  ("node-affinity", r"node[ -]+affinity"),
                                  ("multi-task", r"multi[ -]+task")):
                if re.search(pattern, paper["title"], re.IGNORECASE):
                    paper["tasks"].append(task)
    return sorted(papers, key=lambda p: (-(p["year"] or 0), p["title"].casefold()))


def escape(value):
    return html.escape(str(value), quote=True)


def resource_link(link, css="resource-link"):
    return f'<a class="{css}" href="{escape(link["url"])}" target="_blank" rel="noopener noreferrer">{escape(link["label"])}</a>'


def read_highlights(papers, root=ROOT):
    selections = json.loads((root / "site" / "highlights.json").read_text(encoding="utf-8"))
    highlights = []
    for selection in selections:
        matches = [paper for paper in papers if paper["title"] == selection["title"]
                   and paper["year"] == selection["year"] and selection["topic"] in paper["topics"]]
        if len(matches) != 1:
            raise ValueError(f"Highlight must match exactly one catalog record: {selection['title']}")
        highlights.append({**matches[0], **selection})
    if {item["topic"] for item in highlights} != set(TOPICS):
        raise ValueError("Highlights must represent every research topic")
    return highlights


def display_title(paper):
    return (paper.get("acronym", "") + ": " if paper.get("acronym") else "") + paper["title"]


def paper_url(paper):
    return next(link["url"] for link in paper["links"] if link["label"].lower().startswith("paper"))


def highlights_markdown(highlights):
    lines = ["| Paper | Venue | Topic / Task |", "| --- | --- | --- |"]
    for paper in highlights:
        title = f'[{display_title(paper)}]({paper_url(paper)})'
        code = next((link for link in paper["links"] if link["label"].lower().startswith("code")), None)
        if code:
            title += f' · [Code]({code["url"]})'
        focus = paper["focus"]
        if paper["topic"] == "continuous-time":
            focus = "CTDG · " + focus
        anchor = paper.get("anchor") or (CTDG_TASKS[paper["task"]].lower().replace(" ", "-") if paper.get("task") else str(paper["year"]))
        lines.append(f'| {title} | {paper["venue"]} {paper["year"]} | [{focus}](papers/{paper["topic"]}.md#{anchor}) |')
    return "\n".join(lines)


def update_readme(highlights, root=ROOT):
    path = root / "README.md"
    text = path.read_text(encoding="utf-8")
    start = text.index(HIGHLIGHTS_START) + len(HIGHLIGHTS_START)
    end = text.index(HIGHLIGHTS_END)
    path.write_text(text[:start] + "\n\n" + highlights_markdown(highlights) + "\n\n" + text[end:], encoding="utf-8")


def highlight_card(paper):
    topic = paper["topic"]
    code = next((link for link in paper["links"] if link["label"].lower().startswith("code")), None)
    code_link = resource_link(code) if code else ""
    task = paper.get("task")
    query = f"{topic}:{task}" if task else topic
    return f'''<article class="selected-card" data-highlight-topic="{topic}" data-highlight-year="{paper['year']}">
      <p class="selected-meta">{escape(paper['venue'])} {paper['year']}<span>{escape(paper['focus'])}</span></p>
      <h3><a href="{escape(paper_url(paper))}" target="_blank" rel="noopener noreferrer">{escape(display_title(paper))}</a></h3>
      <div class="highlight-actions">{code_link}<a class="text-link small" href="?topic={query}#paper-explorer">{escape(CTDG_TASKS[task] if task else TOPICS[topic])} — {'Task papers' if task else 'Full paper list'} →</a></div>
    </article>'''


def spotlight_card(paper):
    code = next((link for link in paper["links"] if link["label"].lower().startswith("code")), None)
    code_link = resource_link({"label": "View code ↗", "url": code["url"]}, "button button-light") if code else ""
    return f'''<article class="spotlight" aria-labelledby="spotlight-title" data-highlight-topic="{paper['topic']}" data-highlight-year="{paper['year']}">
      <div class="spotlight-top"><span class="eyebrow">{escape(paper['focus'])}</span><span class="venue-badge">{escape(paper['venue'])} {paper['year']}</span></div>
      <p class="method-name">{escape(paper['acronym'])}</p>
      <h2 id="spotlight-title">{escape(paper['title'])}</h2>
      <p class="spotlight-description">{escape(TOPICS[paper['topic']])} · {escape(paper['focus'])}</p>
      <div class="spotlight-actions">{resource_link({'label': 'Read paper ↗', 'url': paper_url(paper)}, 'button button-dark')}{code_link}</div>
    </article>'''


def paper_card(paper):
    paper_links = [link for link in paper["links"] if link["label"].lower().startswith("paper")]
    title = escape(paper["title"])
    if paper["acronym"]:
        title = escape(paper["acronym"]) + ": " + title
    if paper_links:
        title = f'<a href="{escape(paper_links[0]["url"])}" target="_blank" rel="noopener noreferrer">{title}</a>'
    topic_buttons = "".join(f'<button class="topic-tag" type="button" data-topic="{topic}">{escape(TOPICS[topic])}</button>' for topic in paper["topics"])
    topic_buttons += "".join(f'<button class="topic-tag task-tag" type="button" data-topic="continuous-time:{task}">{escape(CTDG_TASKS[task])}</button>' for task in paper["tasks"])
    kinds = "".join(f'<span class="kind-label">{escape(kind.rstrip("s"))}</span>' for kind in paper["kinds"] if kind != "Paper")
    # Keep citation-export links in the data and Markdown, but prioritize paper/code actions in the browser.
    visible_links = [link for link in paper["links"] if link["label"].lower() != "bibtex"]
    resources = "".join(resource_link(link) for link in visible_links)
    if not resources:
        resources = '<span class="muted">No resource link listed</span>'
    source = paper["sources"][0]
    source_url = f'{REPOSITORY}/blob/main/{source["path"]}#L{source["line"]}'
    return f'''<article class="paper-card" data-paper-id="{paper['id']}">
      <div class="paper-meta"><span>{paper['year'] or 'Year not listed'}</span><span>{escape(paper['venue'])}</span>{kinds}<span class="code-status {'available' if paper['has_code'] else ''}">{'Code linked' if paper['has_code'] else 'No code link'}</span></div>
      <h3>{title}</h3><div class="paper-topics">{topic_buttons}</div>
      <div class="paper-actions">{resources}<a class="source-link" href="{source_url}" target="_blank" rel="noopener noreferrer">In full paper list ↗</a></div>
    </article>'''


def build(output, root=ROOT):
    output = output.resolve()
    if output == root or root in output.parents and output.parts[len(root.parts)] in ("papers", "site", "resources", "scripts", ".git"):
        raise ValueError("Build output must not overwrite source directories")
    output.mkdir(parents=True, exist_ok=True)
    papers = read_catalog(root)
    highlights = read_highlights(papers, root)
    spotlight, = [paper for paper in highlights if paper.get("spotlight")]
    data = {"topics": TOPICS, "tasks": CTDG_TASKS, "papers": papers,
            "highlights": [{"paper_id": paper["id"], "topic": paper["topic"], "focus": paper["focus"]} for paper in highlights],
            "source_entries": sum(len(paper["sources"]) for paper in papers)}
    template = (root / "site" / "index.html").read_text(encoding="utf-8")
    years = sorted({paper["year"] for paper in papers if paper["year"]}, reverse=True)
    replacements = {
        "PAPER_COUNT": str(len(papers)),
        "CODE_COUNT": str(sum(paper["has_code"] for paper in papers)),
        "TOPIC_COUNT": str(len(TOPICS)),
        "YEAR_OPTIONS": "".join(f'<option value="{year}">{year}</option>' for year in years),
        "TOPIC_OPTIONS": "".join(
            f'<option value="{key}">{escape(label)}</option>' + (
                "".join(f'<option value="continuous-time:{task}">↳ {escape(name)}</option>' for task, name in CTDG_TASKS.items())
                if key == "continuous-time" else "")
            for key, label in TOPICS.items()),
        "PAPER_CARDS": "\n".join(paper_card(paper) for paper in papers),
        "SELECTED_CARDS": "\n".join(highlight_card(paper) for paper in highlights if not paper.get("spotlight")),
        "SPOTLIGHT": spotlight_card(spotlight),
        "CATALOG_JSON": json.dumps(data, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"),
    }
    for key, value in replacements.items():
        template = template.replace("{{" + key + "}}", value)
    for name in ("styles.css", "app.js", "favicon.svg"):
        version = hashlib.sha256((root / "site" / name).read_bytes()).hexdigest()[:12]
        template = template.replace(f'"./{name}"', f'"./{name}?v={version}"')
    if re.search(r"{{[A-Z_]+}}", template):
        raise ValueError("Unresolved template placeholder")
    (output / "index.html").write_text(template, encoding="utf-8")
    (output / "papers.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("styles.css", "app.js", "favicon.svg"):
        shutil.copyfile(root / "site" / name, output / name)
    (output / ".nojekyll").touch()
    (output / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{SITE_URL}</loc></url></urlset>\n')
    print(f"Built {len(papers)} paper records from {data['source_entries']} Markdown entries in {output}")
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    parser.add_argument("--update-readme", action="store_true", help="Refresh the README selection from site/highlights.json")
    args = parser.parse_args()
    if args.update_readme:
        update_readme(read_highlights(read_catalog()))
    build(args.output)
