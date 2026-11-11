import json
import re
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from scripts.build_site import (HIGHLIGHTS_END, HIGHLIGHTS_START, ROOT, TOPICS,
                                build, highlights_markdown, read_catalog, read_highlights)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paper_ids = []
        self.catalog_text = ""
        self.in_catalog = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article" and "data-paper-id" in attrs:
            self.paper_ids.append(attrs["data-paper-id"])
        if tag == "script" and attrs.get("id") == "catalog-data":
            self.in_catalog = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_catalog = False

    def handle_data(self, data):
        if self.in_catalog:
            self.catalog_text += data


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.papers = read_catalog()

    def test_every_markdown_entry_is_represented(self):
        source_rows = []
        for topic in TOPICS:
            path = ROOT / "papers" / (topic + ".md")
            for number, line in enumerate(path.read_text().splitlines(), 1):
                if line.startswith("| ") and not line.startswith(("| Paper |", "| ---")):
                    source_rows.append((str(path.relative_to(ROOT)), number))
        indexed_rows = [(source["path"], source["line"]) for paper in self.papers for source in paper["sources"]]
        self.assertCountEqual(indexed_rows, source_rows)
        self.assertEqual(len({p["id"] for p in self.papers}), len(self.papers))

    def test_tcsd_is_searchable_and_has_code(self):
        paper, = [p for p in self.papers if p["acronym"] == "TCSD"]
        self.assertEqual(paper["year"], 2026)
        self.assertIn("continuous-time", paper["topics"])
        self.assertTrue(paper["has_code"])
        self.assertTrue(any(link["url"] == "https://github.com/LuckyGirl-XU/TCSD" for link in paper["links"]))

    def test_anomaly_paper_does_not_invent_code(self):
        paper, = [p for p in self.papers if p["title"].startswith("Mitigating Anomaly Hallucination:")]
        self.assertEqual(paper["year"], 2026)
        self.assertEqual(paper["topics"], ["anomaly-detection"])
        self.assertFalse(paper["has_code"])

    def test_cross_listed_tgat_keeps_both_topics(self):
        paper, = [p for p in self.papers if p["title"] == "Inductive Representation Learning on Temporal Graphs"]
        self.assertEqual(set(paper["topics"]), {"continuous-time", "discrete-time"})
        self.assertEqual(len(paper["sources"]), 2)

    def test_same_title_different_years_remain_separate(self):
        papers = [p for p in self.papers if p["title"] == "Towards Robust Graph Incremental Learning on Evolving Graphs"]
        self.assertEqual({p["year"] for p in papers}, {2022, 2023})

    def test_surveys_and_benchmarks_retain_years(self):
        survey, = [p for p in self.papers if p["title"] == "Representation Learning for Dynamic Graphs: A Survey"]
        self.assertEqual(survey["year"], 2020)
        self.assertIn("Surveys", survey["kinds"])
        dtgb, = [p for p in self.papers if p["title"].startswith("DTGB:")]
        self.assertEqual(dtgb["year"], 2024)

    def test_highlights_cover_every_topic_and_distinct_temporal_tasks(self):
        highlights = read_highlights(self.papers)
        self.assertEqual({paper["topic"] for paper in highlights}, set(TOPICS))
        temporal = [p for p in highlights if p["topic"] == "continuous-time"]
        self.assertEqual({p["focus"] for p in temporal}, {"Link Prediction", "Node Affinity", "Multi-task"})
        self.assertTrue(any(p["venue"] == "ICLR" and p["topic"] == "discrete-time" for p in highlights))
        self.assertTrue(any(p.get("acronym") == "MoMent" and p["venue"] == "AAAI" for p in highlights))

    def test_older_highlights_are_limited_to_task_representatives(self):
        highlights = read_highlights(self.papers)
        older = [p for p in highlights if p["year"] != 2026]
        self.assertEqual({(p["acronym"], p["venue"], p["year"]) for p in older},
                         {("FastHeP", "KDD", 2025), ("LTF", "ICML", 2025), ("OTGNet", "ICLR", 2023)})

    def test_node_affinity_is_a_separate_ctdg_task(self):
        papers = [p for p in self.papers if "node-affinity" in p["tasks"]]
        self.assertTrue(papers)
        self.assertTrue(all("continuous-time" in p["topics"] for p in papers))
        self.assertTrue(any(p["title"].startswith("Revisiting Node Affinity") for p in papers))
        tcsd, = [p for p in self.papers if p["acronym"] == "TCSD"]
        self.assertEqual(tcsd["tasks"], ["link-prediction"])

    def test_temporal_continual_and_open_world_scope(self):
        ltf, = [p for p in self.papers if p["title"].startswith("A Selective Learning Method")]
        otgnet, = [p for p in self.papers if p["title"] == "Towards Open Temporal Graph Neural Networks"]
        nforgot, = [p for p in self.papers if p["title"].startswith("N-ForGOT:")]
        self.assertEqual((ltf["year"], ltf["venue"]), (2025, "ICML"))
        self.assertTrue(all("continual-learning" in p["topics"] for p in (ltf, otgnet, nforgot)))
        selected = [p for p in read_highlights(self.papers) if p["topic"] == "continual-learning"]
        self.assertEqual({p.get("acronym") for p in selected}, {"LTF", "OTGNet"})

    def test_unlearning_has_its_own_direction(self):
        paper, = [p for p in self.papers if p["title"] == "Online Learning with Certified Unlearning over Graphs"]
        self.assertEqual(paper["topics"], ["unlearning"])
        self.assertIn("unlearning", TOPICS)

    def test_readme_and_website_share_the_same_highlights(self):
        text = (ROOT / "README.md").read_text()
        actual = text.split(HIGHLIGHTS_START, 1)[1].split(HIGHLIGHTS_END, 1)[0].strip()
        self.assertEqual(actual, highlights_markdown(read_highlights(self.papers)))

    def test_generated_html_contains_all_records_without_javascript(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            data = build(output)
            parser = PageParser()
            source = (output / "index.html").read_text()
            parser.feed(source)
            self.assertCountEqual(parser.paper_ids, [p["id"] for p in data["papers"]])
            self.assertEqual(json.loads(parser.catalog_text), data)
            self.assertEqual(json.loads((output / "papers.json").read_text()), data)
            self.assertIsNone(re.search(r"{{[A-Z_]+}}", source))
            for name in ("app.js", "styles.css", "favicon.svg", "sitemap.xml", ".nojekyll"):
                self.assertTrue((output / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
