import unittest
from argument_sampling.topic_similarity import *
from collections import Counter

class testSampleFiles(unittest.TestCase):
    def test_sample_files_mostl_similar_different_topics_perspectrum(self):
        df_similar_examples_different_topics = load_similar_examples("perspectrum", "test", "notebooks/data-preparation/sampling_strategies/similarities-perspectrum-most-similar-different-topics.tsv")
        #k = [2, 4, 8, 16, 32, 64]
            #self.assertEqual(df_similar_examples_different_topics["k"].unique().tolist(), k)
        stance_counts = df_similar_examples_different_topics.groupby("test-id").agg({"stance":Counter})
        expected_stance_counts = {1: 8 , 0:8}
        for stance in stance_counts.stance:
            self.assertEqual(stance, expected_stance_counts)
        topic_counts = df_similar_examples_different_topics.groupby("test-id").agg({"topic":lambda l: len(set(l))})

        for topic_count in topic_counts.topic:
            self.assertGreater(topic_count, 7)


        retrieved_counts = df_similar_examples_different_topics.groupby("test-id").agg({"id":lambda l: len(set(l))})
        for retrieved_count in retrieved_counts.id:

            self.assertEqual(retrieved_count, 16)
        self.assertEqual(len(df_similar_examples_different_topics["test-id"].unique()), 2773)

    def test_sample_files_most_similar_different_topics_vast(self):
        df_similar_examples_different_topics = load_similar_examples("vast", "test", "notebooks/data-preparation/sampling_strategies/similarities-vast-most-similar-different-topics.tsv")
        #k = [2, 4, 8, 16, 32, 64]
        #self.assertEqual(df_similar_examples_different_topics["k"].unique().tolist(), k)
        stance_counts = df_similar_examples_different_topics.groupby("test-id").agg({"stance":Counter})
        expected_stance_counts = {1: 5 , 0:5, 2:5}
        for stance in stance_counts.stance:
            for key, value in expected_stance_counts:
                self.assertGreater(value, expected_stance_counts[key])
        topic_counts = df_similar_examples_different_topics.groupby("test-id").agg({"topic":lambda l: len(set(l))})

        for topic_count in topic_counts.topic:
            self.assertGreater(topic_count, 7)



        retrieved_counts = df_similar_examples_different_topics.groupby("test-id").agg({"id":lambda l: len(set(l))})
        for retrieved_count in retrieved_counts.id:

            self.assertEqual(retrieved_count, 16)

        self.assertEqual(len(df_similar_examples_different_topics["test-id"].unique()), 1460)

    def test_sample_files_most_similar_different_topics(self):
        df_similar_examples_different_topics = load_similar_examples("ibmsc", "test", "notebooks/data-preparation/sampling_strategies/similarities-ibmsc-most-similar-different-topics.tsv")
    #k = [2, 4, 8, 16, 32, 64]
    #self.assertEqual(df_similar_examples_different_topics["k"].unique().tolist(), k)
        stance_counts = df_similar_examples_different_topics.groupby("test-id").agg({"stance":Counter})
        expected_stance_counts = {1: 8 , 0:8}
        for stance in stance_counts.stance:
            self.assertEqual(stance, expected_stance_counts)
        topic_counts = df_similar_examples_different_topics.groupby("test-id").agg({"topic":lambda l: len(set(l))})

        for topic_count in topic_counts.topic:
            self.assertGreater(topic_count, 7)



        retrieved_counts = df_similar_examples_different_topics.groupby("test-id").agg({"id":lambda l: len(set(l))})
        for retrieved_count in retrieved_counts.id:

            self.assertEqual(retrieved_count, 16)

        self.assertEqual(len(df_similar_examples_different_topics["test-id"].unique()), 1355)