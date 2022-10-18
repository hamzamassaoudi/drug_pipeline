from collections import Counter
import json
from config import OUTPUT_DIR
import pathlib
import typing
import argparse

path_type = typing.Union[str, pathlib.Path]


def read_json_results(results_path: path_type) -> dict:
    """read a json file and load it as dictionary

    Args:
        results_path (_type_): output path of the results of the pipeline
    """
    return json.load(open(results_path))


def _get_unique_mentions(drug_graph: dict) -> typing.List[str]:
    """for each drug name get the set of journal names mentioning it

    Args:
        drug_graph  : output json graph
    """
    journal_mentions = []
    for drug in drug_graph.keys():
        unique_journal_mention = set(
            [journal["journal_name"] for journal in drug_graph[drug]["journal"]]
        )
        journal_mentions += list(unique_journal_mention)
    return journal_mentions


def most_journal_drug_mentions(drug_graph: dict) -> str:
    """get the journal that mentions maximum of different drug names

    Args:
        drug_graph: output json graph
    """
    journal_mentions = _get_unique_mentions(drug_graph)
    mention_counter = Counter(journal_mentions)
    return max(journal_mentions, key=mention_counter.get)


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_path",
        type=str,
        nargs="?",
        const=OUTPUT_DIR.joinpath("./results.json"),
        default=OUTPUT_DIR.joinpath("./results.json"),
        help="output path of the pipeline results",
    )
    args = parser.parse_args()

    # Opening reuslts JSON file
    drug_graph = read_json_results(args.output_path)
    # get the journal name with the most mentions occurrences of drugs
    journal_with_higher_drug_mentions = most_journal_drug_mentions(drug_graph)
    print(
        "The journal with most drug mentions is : {}".format(
            journal_with_higher_drug_mentions
        )
    )
