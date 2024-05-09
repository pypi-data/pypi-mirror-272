import re
import arxiv

from typing import Optional


def get_arxiv_id(title: str) -> Optional[str]:
    # split title into multiple components
    query = " AND ".join(
        map(
            lambda x: f"ti:{x}",
            map(
                lambda x: re.sub(r"\W", "", x),
                title.split(" "),
            ),
        ),
    )

    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    results = client.results(search)
    all_results = list(results)

    for result in all_results:
        if result.title.lower() == title.lower():
            match_result = result
            break
    else:
        match_result = None

    if match_result is None:
        return None
    else:
        entry_id = match_result.entry_id
        arxiv_id = re.search(r"http://arxiv.org/abs/(\d*\.\d*)", entry_id).group(1)
        return arxiv_id
