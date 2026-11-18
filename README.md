# Xiangyu Zou · Academic homepage

A Jekyll academic homepage for [zouxy.cn](https://zouxy.cn), with research interests, publications, appointments, education, and a technical notebook. The page renders the complete publication list into HTML and adds topic filters, year filters, search, and citation copying in the browser.

The site remains compatible with GitHub Pages. Existing article URLs, bibliography files, downloadable papers, and the custom domain are retained. The notebook lives at `/blog/`; the historical posts still use their original date-based URLs. The old `/about/` address redirects to the academic profile on the homepage.

## Preview locally

With Ruby and Bundler available:

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open `http://127.0.0.1:4000/`. To generate the static site without serving it:

```sh
bundle exec jekyll build
```

The generated output is `_site/`. Jekyll 3.10 and `jekyll-paginate` are declared in `Gemfile`; `kramdown-parser-gfm` is included explicitly for the existing Markdown articles. `Gemfile.lock` records the tested dependency versions. For a project-local dependency installation, run `bundle install --path vendor/bundle` instead; this directory is excluded from the site and Git.

## Maintain the content

- `_data/profile.yml` contains the name, position, affiliation, portrait, contact links, appointments, and education.
- `_data/publications.json`: the publication list. Add an object using the fields below; the page groups entries by year automatically.
- `_data/publication_topics.yml` defines the labels and display order of the publication topics.
- `_data/ccf.yml` maps venue abbreviations to grades in the [2026 CCF catalogue](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml).
- `_posts/`: technical notes in Markdown. Keep existing filenames and `date` values to preserve published URLs.
- `bibtex/` and `pubs/`: bibliography files and downloadable papers. Use root-relative links such as `/bibtex/example.bib` in publication data.
- `css/academic.css` and `js/academic.js`: the academic layout and its browser interactions.
- `_layouts/academic.html`: shared document head, navigation, and footer.

A publication entry uses this structure:

```json
{
  "id": "pub-2026-unique-stable-id",
  "year": 2026,
  "title": "Paper title",
  "authors": "First Author, Xiangyu Zou, Other Author",
  "venue": "VENUE",
  "citation": "Full venue and publication details.",
  "url": "",
  "links": [],
  "bibtex": "",
  "topics": ["storage-systems", "deduplication"]
}
```

Keep `id` unique and stable because it is also a link target. Use one or more topic IDs from `_data/publication_topics.yml`. Author names use plain text, and the page emphasizes Xiangyu Zou automatically. Set `format` to `poster` for poster entries so they display the venue abbreviation alone. Use an empty string for an unavailable paper URL or BibTeX entry. Resource links have the shape `{"label": "PDF", "url": "/pubs/example.pdf"}`. A `BibTeX` link should point to a `.bib` file and include the citation text in `bibtex` for the expandable panel. Optional `source_url` and `evidence_note` fields record provenance. Keep an existing paper’s ID if its final publication year or metadata changes.

The [publication audit](docs/publication-audit.md) records the 2026-11-18 refresh, sources, identity checks, and unresolved coverage limits; `_data/publication_audit.json` stores its structured change log. Google Scholar returned HTTP 429, so this refresh does **not** claim a complete synchronization with the Scholar profile. The added works were checked against official proceedings, publisher metadata, and institutional sources. The `docs/` audit and legacy source are excluded from the published site.

`scripts/import-publications.py` only recreates the original 47-paper About-page bibliography and defaults to `docs/legacy-about.html`. Routine maintenance should edit the current JSON directly. The script requires an explicit `--output`; always use a separate destination when comparing historical data, because its legacy export does not include the later researched additions:

```sh
python3 scripts/import-publications.py --source /path/to/legacy-about.html --output /tmp/imported-publications.json
```

## Routing and publishing

`_config.yml` sets `url: https://zouxy.cn`, an empty `baseurl`, `permalink: pretty`, and `timezone: UTC`. Keep UTC so the original post dates produce the same URLs on different computers. The notebook uses `blog/index.html` and `paginate_path: /blog/page:num/`; do not give its index page a front-matter permalink, which would interfere with pagination.

Build and review the changes locally before merging into the branch configured for GitHub Pages. Preserve `CNAME` when publishing to the existing domain. A local preview or local Git branch does not update the public site.

## Credits

The original blog and retained article layouts derive from the [Hux Blog boilerplate](https://github.com/Huxpro/huxpro.github.io). See `LICENSE` for the Apache 2.0 license.
