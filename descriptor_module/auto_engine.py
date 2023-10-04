import os
import csv

if not os.getenv("AUTH_KEY") or not os.getenv("COHERE_API_KEY"):
    raise RuntimeError("You need to set both AUTH_KEY and COHERE_API_KEY environment variables to proceed")

try:
    import cohere
except ImportError:
    raise RuntimeError("Cohere library is not installed")

cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))

import requests

def get_ai_snippets_for_query(query):
    headers = {"X-API-Key": os.environ["AUTH_KEY"]}
    results = requests.get(
        f"https://api.ydc-index.io/search?query={query}",
        headers=headers,
    ).json()

    # We return many text snippets for each search hit so
    # we need to explode both levels
    return "\n".join(["\n".join(hit["snippets"]) for hit in results["hits"]])

def get_cohere_prompt(query, context):
    return f"""Tell me about {query['art_name']} done by {query['author_name']} in {query['date']}.
context: {context}
answer: """

def ask_cohere(query, context):
    try:
        return cohere_client.generate(prompt=get_cohere_prompt(query, context))[
            0
        ].text
    except Exception as e:
        print(
            "Cohere call failed for query {} and context {}".format(query, context)
        )
        print(e)
        return "Sorry hooman, got nothing for you on this homie"

def ask_cohere_with_ai_snippets(query):
    ai_snippets = get_ai_snippets_for_query(query)
    return ask_cohere(query, ai_snippets)
