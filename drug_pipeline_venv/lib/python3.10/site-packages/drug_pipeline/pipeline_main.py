from traitlets import default
from pipeline import Pipeline
import pathlib
import typing
from config import DATA_DIR, OUTPUT_DIR
import argparse

path_type = typing.Union[str, pathlib.Path]


def main(
    drugs_file_path: path_type = DATA_DIR.joinpath("./drugs.csv"),
    pubmed_file_path: path_type = DATA_DIR.joinpath("./pubmed.csv"),
    clinical_trial_file_path: path_type = DATA_DIR.joinpath("./clinical_trials.csv"),
    output_path: path_type = OUTPUT_DIR.joinpath("./results.json"),
):
    """pipeline main function

    Args:
        drugs_file_path (path_type, optional): drugs csv file path. Defaults to DATA_DIR.joinpath("./drugs.csv").
        pubmed_file_path (path_type, optional): pubmed csv file path. Defaults to DATA_DIR.joinpath("./pubmed.csv").
        clinical_trial_file_path (path_type, optional): clinical trials csv file path. Defaults to DATA_DIR.joinpath( "./clinical_trials.csv" ).
        output_path (path_type, optional): output path to store the graph json file. Defaults to OUTPUT_DIR.joinpath("./results.json").
    """
    pipeline = Pipeline(
        drugs_file_path, pubmed_file_path, clinical_trial_file_path, output_path
    )
    pipeline.read_drugs()
    pipeline.add_pubmed_publication_mention()
    pipeline.add_clinical_trial_mention()
    pipeline.add_journal_mention()
    pipeline.save_json_graph()


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add arguments
    parser.add_argument(
        "--drugs_file_path",
        type=str,
        nargs="?",
        const=DATA_DIR.joinpath("./drugs.csv"),
        default=DATA_DIR.joinpath("./drugs.csv"),
        help="drugs csv file path",
    )
    parser.add_argument(
        "--pubmed_file_path",
        type=str,
        nargs="?",
        const=DATA_DIR.joinpath("./pubmed.csv"),
        default=DATA_DIR.joinpath("./pubmed.csv"),
        help="pubmed csv file path",
    )
    parser.add_argument(
        "--clinical_trial_file_path",
        type=str,
        nargs="?",
        const=DATA_DIR.joinpath("./clinical_trials.csv"),
        default=DATA_DIR.joinpath("./clinical_trials.csv"),
        help="clinical trials csv file path",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        nargs="?",
        const=OUTPUT_DIR.joinpath("./results.json"),
        default=OUTPUT_DIR.joinpath("./results.json"),
        help="output path to store the graph json file",
    )
    # Parse the argument
    args = parser.parse_args()
    main(
        args.drugs_file_path,
        args.pubmed_file_path,
        args.clinical_trial_file_path,
        args.output_path,
    )
