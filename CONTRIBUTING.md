# Contributing

Contributions are welcome through [pull requests](https://github.com/LuckyGirl-XU/Awesome-DynamicGraphLearning/pulls) and [issues](https://github.com/LuckyGirl-XU/Awesome-DynamicGraphLearning/issues/new/choose).

## Add a Paper

1. Choose a relevant page in [papers](papers) and the appropriate year, survey, or benchmark section.
2. Use the full paper title and a verified venue. Mark unpublished manuscripts as `arXiv` or `Preprint`.
3. Link to a stable publication page, DOI, arXiv record, or OpenReview page. Avoid signed download URLs.
4. Include a code link when available. Label third-party implementations `Code (unofficial)` and anonymous repositories `Code (anonymous)`.
5. Check for an existing entry. Cross-listing across relevant topics is welcome; merge duplicates within the same topic and retain alternative paper or code links.

Use the existing three-column table format:

```markdown
| Full Paper Title | Venue | [Paper](https://example.org/paper) · [Code](https://github.com/owner/repository) |
```

Use `—` for a missing venue or resource link. Do not add empty links or empty year headings. Keep any short descriptions factual and specific.

## Add a Dataset or Library

Add benchmark entry points to [Datasets & Benchmarks](resources/datasets-and-benchmarks.md), or software to [Libraries & Implementations](resources/libraries.md). Include the project name, scope, and original resource link.

## Update the Homepage

Keep the README concise. Place complete paper lists in topic pages and select a small number of recent papers for the homepage. Describe the selection year without implying that it is a complete list or a ranking.

## Preview the Paper Explorer

The website is generated from the Markdown tables in `papers/`. Update those tables to keep both views in sync. Entries with the same title and year are combined across topics in the explorer; all source locations and links are retained. Homepage selections are defined in `site/highlights.json`; each selection must match a catalog entry. Run `python3 scripts/build_site.py --update-readme` after changing selections to update the README and website together.

CTDG task tags use explicit task names in paper titles; unassigned papers remain in the parent collection. Temporal continual learning and open-world temporal graph learning share one direction. Graph unlearning has a separate collection.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_site.py
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000`. Website layout and filtering live in `site/`. GitHub Actions rebuilds and publishes the explorer when these sources change on `main`.

## Report a Correction

Include the affected entry, its page, and a source supporting the correction. For a broken link, provide a stable replacement when possible.
