import json
import os
import logging
import unittest
import unittest.mock
from src.twitter_agent.twitter_agent import TwitterAgent

class TestRespondToKeyUsers(unittest.TestCase):
    # Construct relevant paths (OS agnostic)
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_CONVSERSATIONS = os.path.join(THIS_DIR, "test_data", "test_conversations.json")

    # Load test conversations
    with open(TEST_CONVSERSATIONS, 'r') as f:
        test_conversations = json.load(f)

    # Set up logging
    logging.getLogger().setLevel(logging.INFO)

    # Create a new twitter agent
    twitter_agent = TwitterAgent()

    # Mock twitter class
    twitter_agent.twitter = unittest.mock.Mock()
    twitter_agent.twitter.post_tweet.return_value = (True, 0)


    def get_conversation(self, key):
        return {key: self.test_conversations[key]}


    def test_respond_to_key_users_no_relevant_conversations(self):
        self.twitter_agent.twitter.get_relevant_conversations.return_value = {}
        self.twitter_agent.respond_to_key_users()

        # Assert that tweet is not posted
        self.twitter_agent.twitter.post_tweet.assert_not_called()
         

    def test_respond_to_key_users_single_tweet(self):
        self.twitter_agent.twitter.get_relevant_conversations.return_value = self.get_conversation("1882080194049220872")
        self.twitter_agent.respond_to_key_users()

        # Assert that tweet is posted
        self.twitter_agent.twitter.post_tweet.assert_called()


    def test_respond_to_key_users_retweet(self):
        self.twitter_agent.twitter.get_relevant_conversations.return_value = self.get_conversation("1882080527735501115")
        self.twitter_agent.respond_to_key_users()

        # Assert that tweet is posted
        self.twitter_agent.twitter.post_tweet.assert_called()


    def test_respond_to_key_users_quote(self):
        self.twitter_agent.twitter.get_relevant_conversations.return_value = self.get_conversation("1882080576582390231")
        self.twitter_agent.respond_to_key_users()

        # Assert that tweet is posted
        self.twitter_agent.twitter.post_tweet.assert_called()


    def test_respond_to_key_users_thread_started_by_key_user(self):
        self.twitter_agent.twitter.get_relevant_conversations.return_value = self.get_conversation("1882080378296664242")
        self.twitter_agent.respond_to_key_users()

        # Assert that tweet is posted
        self.twitter_agent.twitter.post_tweet.assert_called()


    # def test_respond_to_key_users_thread_started_by_agent(self):
    #     self.twitter_agent.twitter.get_relevant_conversations = unittest.mock.MagicMock(self.test_conversations[""])

    #     # Assert that tweet is posted
    #     self.twitter_agent.twitter.post_tweet.assert_called()


    # def test_respond_to_key_users_thread_started_by_irrelevant_user(self):
    #     self.twitter_agent.twitter.get_relevant_conversations = unittest.mock.MagicMock(self.test_conversations[""])

    #     # Assert that tweet is not posted
    #     self.twitter_agent.twitter.post_tweet.assert_not_called()

if __name__ == '__main__':
    unittest.main()