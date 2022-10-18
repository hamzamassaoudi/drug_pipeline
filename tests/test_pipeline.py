import unittest
from drug_pipeline import pipeline


class TestPipeline(unittest.TestCase):
    def test_drug_initialization(self):
        """
        Test that it can sum a list of integers
        """
        pipeline_object = pipeline.Pipeline(
            "../data/drugs.csv",
            "../data/pubmed.csv",
            "../data/clinical_trials.csv",
            "../output/results.json",
        )
        pipeline_object.read_drugs()
        graph_result = pipeline_object.get_graph_results()
        self.assertIn("DIPHENHYDRAMINE", graph_result.keys())


if __name__ == "__main__":
    unittest.main()
