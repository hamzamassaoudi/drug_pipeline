import pandas as pd
import json
import pathlib
import typing

path_type = typing.Union[str, pathlib.Path]


class Pipeline:
    def __init__(
        self,
        drugs_file_path: path_type,
        pubmed_file_path: path_type,
        clinical_trial_file_path: path_type,
        output_path: path_type,
    ) -> None:
        """init function
        Args:
            drugs_file_path (path_type, optional): drugs csv file path. Defaults to DATA_DIR.joinpath("./drugs.csv").
            pubmed_file_path (path_type, optional): pubmed csv file path. Defaults to DATA_DIR.joinpath("./pubmed.csv").
            clinical_trial_file_path (path_type, optional): clinical trials csv file path. Defaults to DATA_DIR.joinpath( "./clinical_trials.csv" ).
            output_path (path_type, optional): output path to store the graph json file. Defaults to OUTPUT_DIR.joinpath("./results.json").
        """
        self.json_graph = {}
        self.drugs_file_path = drugs_file_path
        self.pubmed_file_path = pubmed_file_path
        self.clinical_trial_file_path = clinical_trial_file_path
        self.output_path = output_path

    def read_drugs(self) -> None:
        """initiate a template dictionary with drug names as keys"""
        drugs_dataset = pd.read_csv(self.drugs_file_path)
        for drug_name in drugs_dataset.drug:
            self.json_graph[drug_name] = {
                "pubmed": [],
                "journal": [],
                "clinical_trial": [],
            }

    def _add_publication_mention_to_graph(
        self, publications_dataset: pd.DataFrame, publication_type: str
    ) -> None:
        """add the publication title and date for each drug if it is mentioned in the title

        Args:
            publications_dataset (pd.DataFrame): publication pandas dataframe
            publication_type (str): type of publication. must be one of (pubmed, clinical_trial)

        Raises:
            ValueError: _description_
        """
        if publication_type not in ["pubmed", "clinical_trial"]:
            raise ValueError(
                "publication_type param must be either pubmed or clinical_trial"
            )
        else:
            for drug_name in self.json_graph.keys():
                for _, row in publications_dataset.iterrows():
                    if drug_name.lower() in row["title"].lower():
                        node_to_append = {"date": row["date"], "title": row["title"]}
                        self.json_graph[drug_name][publication_type].append(
                            node_to_append
                        )

    def add_pubmed_publication_mention(self) -> None:
        """for each drug name, add pubmed publication with a mention of it."""
        pubmed_dataset = pd.read_csv(self.pubmed_file_path)
        self._add_publication_mention_to_graph(pubmed_dataset, "pubmed")

    def add_clinical_trial_mention(self) -> None:
        """for each drug name, add clinical trials publication with a mention of it."""
        clinical_trial_dataset = pd.read_csv(self.clinical_trial_file_path).rename(
            columns={"scientific_title": "title"}
        )
        self._add_publication_mention_to_graph(clinical_trial_dataset, "clinical_trial")

    def add_journal_mention(
        self,
    ) -> None:
        """add information of journal mentioning drug name. A journal is considered as mentioning a given drug if it issued either a pubmed or clinical trial publication mentioning the same drug"""
        pubmed_dataset = pd.read_csv(self.pubmed_file_path)
        clinical_trial_dataset = pd.read_csv(self.clinical_trial_file_path).rename(
            columns={"scientific_title": "title"}
        )
        for drug_name in self.json_graph.keys():
            for _, row in pd.concat(
                [pubmed_dataset, clinical_trial_dataset]
            ).iterrows():
                if drug_name.lower() in row["title"].lower():
                    journal_dictionary = {
                        "date": row["date"],
                        "journal_name": row["journal"],
                    }
                    if journal_dictionary not in self.json_graph[drug_name]["journal"]:
                        self.json_graph[drug_name]["journal"].append(journal_dictionary)

    def get_graph_results(self) -> dict:
        """get the dictionary with all the mentions results

        Returns:
            dict: dictionary with all results
        """
        return self.json_graph

    def save_json_graph(self) -> None:
        """save the dictionary with all the mentions results"""
        json.dump(self.json_graph, open(self.output_path, "w"))
