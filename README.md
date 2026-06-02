# SerpAPI Dorker

Generate Google dorks from a list of domains and keywords, automatically splitting queries to stay within Google's search query limits.

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

## Features

- Generate Google dorks from domain and keyword lists
- Automatically remove duplicate domains and keywords
- Automatically split oversized queries
- Keep generated queries below Google's practical query length limits
- Save generated dorks to `generated_queries.txt`
- Search generated dorks using SerpAPI
- Save raw JSON responses
- Extract discovered URLs into `hits.txt`
- Support custom input/output files

## Installation

```bash
pip3 install serpapi
```

## Usage

Default files:

```bash
python3 dorker.py
```

Custom files:

```bash
python3 dorker.py \
  -a apikey.txt \
  -d domain.txt \
  -q query.txt
```

Generate queries only:

```bash
python3 dorker.py --no-search
```

## Output

### generated_queries.txt

Generated Google dorks.

### hits.txt

Collected URLs from search results.

### results/

Raw SerpAPI JSON responses.

## Why?

Google does not reliably process very large search queries.

Instead of generating a single oversized query such as:

```text
(site:domain1.com OR site:domain2.com OR ... site:domain50.com) and ("slot" or "gacor")
```

the tool automatically splits it into multiple smaller queries that remain within Google's practical limits.

## Disclaimer

This tool is intended for security research, OSINT, and authorized testing activities only.

Users are responsible for complying with applicable laws, Google's Terms of Service, SerpAPI Terms of Service, and any authorization requirements of the target organizations.
