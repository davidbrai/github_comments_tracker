import unittest
import settings
import dao

class TestDao(unittest.TestCase):

    def setUp(self):
        settings.MONGO_DB = 'test_github_comments'
        self.mongodb = dao.get_db()
        if 'test' not in self.mongodb.name:
            raise AssertionError("test database doesn't contain 'test'. it is: %s" % self.mongodb.name)

    def tearDown(self):
        if 'test' in self.mongodb.name:
            for collection in self.mongodb.collection_names():
                if not 'system' in collection:
                    self.mongodb.drop_collection(collection)
        else:
            raise AssertionError("do you really want to drop database: %s?" % self.mongodb.name)

    def test_puts_comments_in_same_commit_path_line_in_same_thread(self):
        comment1 = {'id': 123, 'commit': 'somecommitid', 'path': 'somepath', 'line': 'someline'}
        comment2 = {'id': 124, 'commit': 'somecommitid', 'path': 'somepath', 'line': 'someline'}
        
        dao.save_to_thread(comment1)
        dao.save_to_thread(comment2)
        
        threads = dao.get_threads()
        assert len(threads) == 1
        self.assertIn(comment1, threads[0]['comments'])
        self.assertIn(comment2, threads[0]['comments'])
    
    def test_comments_on_different_lines_are_on_different_threads(self):
        comment1 = {'id': 123, 'commit': 'somecommitid', 'path': 'somepath', 'line': 'someline'}
        comment2 = {'id': 124, 'commit': 'somecommitid', 'path': 'somepath', 'line': 'differentline'}
        
        dao.save_to_thread(comment1)
        dao.save_to_thread(comment2)
        
        threads = dao.get_threads()
        assert len(threads) == 2
    
    def test_doesnt_save_the_same_comment_twice_by_id(self):
        comment = {'id': 123, 'commit': 'somecommitid', 'path': 'somepath', 'line': 'someline'}
        
        dao.save_to_thread(comment)
        dao.save_to_thread(comment)
        
        threads = dao.get_threads()
        self.assertEqual(len(threads[0]['comments']), 1)
