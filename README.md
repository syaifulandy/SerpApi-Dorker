````markdown
# SerpAPI Dorker

Generate Google dork queries from large domain and keyword lists, automatically split oversized queries to stay within Google's search query limits, then search them through SerpAPI and collect the results.

## Features

- Load domains from `domain.txt`
- Load keywords from `query.txt`
- Load SerpAPI key from `apikey.txt`
- Remove duplicate domains and keywords automatically
- Generate Google dorks in the format:

```text
(site:example.com OR site:test.com) and ("keyword1" or "keyword2")
```

- Automatically split large domain and keyword lists into multiple valid queries
- Prevent oversized Google queries by enforcing a configurable word limit (default: 30 words)
- Save generated dorks to `generated_queries.txt`
- Search generated dorks using SerpAPI
- Save raw JSON responses for every query
- Extract discovered URLs into `hits.txt`
- Graceful error handling for:
  - Missing files
  - Empty files
  - Invalid API keys
  - API failures
  - User interruptions

---

## Example

### domain.txt

```text
go.id
ac.id
```

### query.txt

```text
slot
gacor
```

### Generated Query

```text
(site:go.id OR site:ac.id) and ("slot" or "gacor")
```

---

## Installation

Install the SerpAPI Python package:

```bash
pip3 install serpapi
```

---

## File Structure

```text
.
├── dorker.py
├── apikey.txt
├── domain.txt
├── query.txt
├── generated_queries.txt
├── hits.txt
└── results/
```

---

## Usage

### Default Files

Uses:

- `apikey.txt`
- `domain.txt`
- `query.txt`

```bash
python3 dorker.py
```

### Custom Files

```bash
python3 dorker.py \
  -a myapikey.txt \
  -d domains.txt \
  -q keywords.txt
```

### Generate Queries Only

Skip SerpAPI searches and only generate dorks:

```bash
python3 dorker.py --no-search
```

---

## Output

### generated_queries.txt

Generated Google dorks.

Example:

```text
(site:example1.com OR site:example2.com) and ("keyword1" or "keyword2")
(site:example3.com OR site:example4.com) and ("keyword1" or "keyword2")
```

### hits.txt

Extracted URLs from organic search results.

Example:

```text
https://example.com/page1
https://example.com/page2
https://example.com/page3
```

### results/

Raw SerpAPI JSON responses.

```text
results/
├── query_1.json
├── query_2.json
├── query_3.json
└── ...
```

---

## Query Splitting Logic

Google queries have practical limits on the number of words/operators that can be processed reliably.

This tool automatically:

1. Deduplicates domains and keywords.
2. Calculates query size.
3. Splits domain groups when necessary.
4. Splits keyword groups if they still exceed the limit.
5. Generates multiple valid dorks instead of creating oversized queries.

Example:

```text
49 domains
2 keywords
```

Instead of generating:

```text
(site:49-domains...) and ("slot" or "gacor")
```

The tool generates multiple smaller queries:

```text
(site:d1 OR ... d14) and ("slot" or "gacor")
(site:d15 OR ... d28) and ("slot" or "gacor")
(site:d29 OR ... d42) and ("slot" or "gacor")
(site:d43 OR ... d49) and ("slot" or "gacor")
```

---

## Use Cases

- Website compromise hunting
- Defacement discovery
- SEO spam detection
- Keyword exposure monitoring
- OSINT investigations
- Large-scale Google dorking
- Security research
- Domain portfolio monitoring

---

## Disclaimer

This tool is intended for authorized security testing, OSINT, monitoring, and research purposes only.

The user is solely responsible for ensuring compliance with:

- Applicable laws and regulations
- Google's Terms of Service
- SerpAPI Terms of Service
- Target organization authorization requirements

Use responsibly.
````
