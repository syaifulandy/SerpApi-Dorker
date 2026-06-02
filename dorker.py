#!/usr/bin/env python3

import argparse
import json
import os
import sys
import time

try:
    import serpapi
except ImportError:
    print("[!] Missing module: serpapi")
    print("[!] Install:")
    print("    pip3 install serpapi")
    sys.exit(1)

MAX_WORDS = 30


def banner():
    print("=" * 60)
    print(" SerpAPI Dork Generator")
    print("=" * 60)


def load_lines(filename, name):
    if not os.path.isfile(filename):
        print(f"[!] {name} file not found: {filename}")
        return None

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [x.strip() for x in f if x.strip()]

        if not lines:
            print(f"[!] {name} file is empty: {filename}")
            return None

        # remove duplicates while preserving order
        seen = set()
        unique = []

        for line in lines:
            if line not in seen:
                seen.add(line)
                unique.append(line)

        return unique

    except Exception as e:
        print(f"[!] Failed reading {filename}: {e}")
        return None


def load_api_key(filename):
    if not os.path.isfile(filename):
        print(f"[!] API key file not found: {filename}")
        return None

    try:
        with open(filename, "r", encoding="utf-8") as f:
            key = f.read().strip()

        if not key:
            print("[!] API key file is empty")
            return None

        return key

    except Exception as e:
        print(f"[!] Failed reading API key: {e}")
        return None



def build_query(domains, keywords):
    domain_part = "(" + " OR ".join(
        f"site:{d}" for d in domains
    ) + ")"

    keyword_part = "(" + " or ".join(
        f'"{k}"' for k in keywords
    ) + ")"

    return f"{domain_part} and {keyword_part}"
def actual_query_words(query):
    return len(
        query
        .replace("(", " ")
        .replace(")", " ")
        .replace('"', " ")
        .split()
    )


def generate_queries(domains, keywords):

    queries = []

    #
    # Split domain dulu
    #
    domain_chunks = []
    current_domains = []

    for domain in domains:

        test_domains = current_domains + [domain]

        test_query = build_query(
            test_domains,
            keywords
        )

        if actual_query_words(test_query) <= MAX_WORDS:
            current_domains.append(domain)

        else:

            if current_domains:
                domain_chunks.append(
                    current_domains
                )

            current_domains = [domain]

    if current_domains:
        domain_chunks.append(
            current_domains
        )

    #
    # Split keyword jika masih kepanjangan
    #
    for d_chunk in domain_chunks:

        current_keywords = []

        for kw in keywords:

            test_keywords = (
                current_keywords + [kw]
            )

            test_query = build_query(
                d_chunk,
                test_keywords
            )

            if (
                actual_query_words(
                    test_query
                )
                <= MAX_WORDS
            ):
                current_keywords.append(
                    kw
                )

            else:

                if current_keywords:

                    queries.append(
                        build_query(
                            d_chunk,
                            current_keywords
                        )
                    )

                current_keywords = [kw]

        if current_keywords:

            queries.append(
                build_query(
                    d_chunk,
                    current_keywords
                )
            )

    return queries

def save_queries(queries, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for q in queries:
                f.write(q + "\n")

        return True

    except Exception as e:
        print(f"[!] Failed saving query file: {e}")
        return False


def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )

        return True

    except Exception as e:
        print(f"[!] Failed saving {filename}: {e}")
        return False


def append_hits(results, filename):
    try:
        organic = results.get("organic_results", [])

        with open(filename, "a", encoding="utf-8") as f:
            for item in organic:
                url = item.get("link")
                if url:
                    f.write(url + "\n")

    except Exception:
        pass


def search(api_key, query):
    client = serpapi.Client(api_key=api_key)

    return client.search({
        "engine": "google",
        "google_domain": "google.com",
        "q": query,
        "gl": "id",
        "filter": "0"
    })


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--apikey",
        default="apikey.txt"
    )

    parser.add_argument(
        "-d",
        "--domain",
        default="domain.txt"
    )

    parser.add_argument(
        "-q",
        "--query",
        default="query.txt"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="generated_queries.txt"
    )

    parser.add_argument(
        "--no-search",
        action="store_true"
    )

    args = parser.parse_args()

    banner()

    domains = load_lines(args.domain, "Domain")
    if domains is None:
        sys.exit(1)

    keywords = load_lines(args.query, "Keyword")
    if keywords is None:
        sys.exit(1)

    print(f"[+] Domains  : {len(domains)}")
    print(f"[+] Keywords : {len(keywords)}")

    queries = generate_queries(
        domains,
        keywords
    )

    if not save_queries(
        queries,
        args.output
    ):
        sys.exit(1)

    print(f"[+] Queries generated : {len(queries)}")
    for idx, q in enumerate(
        queries,
        start=1
    ):

        words = actual_query_words(q)

        print(
            f"    Query {idx}: {words} words"
        )
    print(f"[+] Saved            : {args.output}")

    if args.no_search:
        print("[+] Done (generate only)")
        return

    api_key = load_api_key(args.apikey)

    if not api_key:
        sys.exit(1)

    os.makedirs("results", exist_ok=True)

    hits_file = "hits.txt"

    try:
        if os.path.exists(hits_file):
            os.remove(hits_file)
    except Exception:
        pass

    print()

    for idx, query in enumerate(queries, start=1):

        print(
            f"[{idx}/{len(queries)}] Searching..."
        )

        try:
            results = search(
                api_key,
                query
            )

            json_file = (
                f"results/query_{idx}.json"
            )

            save_json(
                json_file,
                results
            )

            append_hits(
                results,
                hits_file
            )

            total = (
                results
                .get(
                    "search_information",
                    {}
                )
                .get(
                    "total_results",
                    "Unknown"
                )
            )

            print(
                f"    Results : {total}"
            )
            print(
                f"    Saved   : {json_file}"
            )

        except KeyboardInterrupt:
            print(
                "\n[!] Interrupted by user"
            )
            sys.exit(0)

        except Exception as e:
            print(
                f"    Error: {e}"
            )

        time.sleep(1)

    print()
    print("[+] Finished")
    print(
        f"[+] Queries : {args.output}"
    )
    print(
        f"[+] Hits    : {hits_file}"
    )
    print(
        f"[+] JSON    : results/"
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit(0)

