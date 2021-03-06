import unittest
import config
import dao
import datetime

class TestDao(unittest.TestCase):

    def setUp(self):
        config.MONGO_DB = 'test_github_comments'
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

    def _comment(self, id=123, commit='somecommitid', path='somepath', line='someline', body='body', user_id=17, created_at=None):
        if not created_at:
            created_at = datetime.datetime.today()
        created_at = created_at.replace(microsecond=0)
        return {'id': id, 'commit': commit, 'path': path, 'line': line, 'created_at': created_at, 'body': body, 'user_id': user_id}

    def test_puts_comments_in_same_commit_path_line_in_same_thread(self):
        comment1 = self._comment(id=123)
        comment2 = self._comment(id=124)
        
        dao.save_to_thread(comment1)
        dao.save_to_thread(comment2)
        
        threads = dao.get_all_threads()
        assert len(threads) == 1
        self.assertIn(comment1, threads[0]['comments'])
        self.assertIn(comment2, threads[0]['comments'])
    
    def test_comments_on_different_lines_are_on_different_threads(self):
        comment1 = self._comment(id=123, line='someline')
        comment2 = self._comment(id=124, line='differentline')
        
        dao.save_to_thread(comment1)
        dao.save_to_thread(comment2)
        
        threads = dao.get_all_threads()
        assert len(threads) == 2
    
    def test_doesnt_save_the_same_comment_twice_by_id(self):
        comment = self._comment()
        
        dao.save_to_thread(comment)
        dao.save_to_thread(comment)
        
        threads = dao.get_all_threads()
        self.assertEqual(len(threads[0]['comments']), 1)

    def test_updates_created_date_on_thread(self):
        comment = self._comment(created_at=datetime.datetime.now())
        
        dao.save_to_thread(comment)
        
        thread = dao.get_all_threads()[0]
        self.assertEqual(thread['created_at'], comment['created_at'])
    
    def test_sets_updated_at_with_comment_date(self):
        comment = self._comment(created_at=datetime.datetime.now())
        
        dao.save_to_thread(comment)
        
        thread = dao.get_all_threads()[0]
        self.assertEqual(thread['updated_at'], comment['created_at'])
    
    def test_changes_created_date_if_comment_with_earlier_date(self):
        now = datetime.datetime.now()
        comment = self._comment(created_at=now)
        dao.save_to_thread(comment)
        
        comment2 = self._comment(created_at=(now-datetime.timedelta(days=5)))
        dao.save_to_thread(comment2)

        thread = dao.get_all_threads()[0]
        self.assertEqual(thread['created_at'], comment2['created_at'])
    
    def test_doesnt_change_updated_date_if_comment_with_later_date(self):
        now = datetime.datetime.now()
        comment = self._comment(created_at=now)
        dao.save_to_thread(comment)
        
        comment2 = self._comment(created_at=(now-datetime.timedelta(days=5)))
        dao.save_to_thread(comment2)

        thread = dao.get_all_threads()[0]
        self.assertEqual(thread['updated_at'], comment['created_at'])
    
    def test_doesnt_change_created_date_if_comment_with_later_date(self):
        now = datetime.datetime.now()
        comment = self._comment(created_at=now)
        dao.save_to_thread(comment)
        
        comment2 = self._comment(created_at=(now+datetime.timedelta(days=5)))
        dao.save_to_thread(comment2)
        
        thread = dao.get_all_threads()[0]
        self.assertEqual(thread['created_at'], comment['created_at'])
    
    def test_changes_updated_date_if_comment_with_later_date(self):
        now = datetime.datetime.now()
        comment = self._comment(id=123, created_at=now)
        dao.save_to_thread(comment)
        
        comment2 = self._comment(id=124, created_at=(now+datetime.timedelta(days=5)))
        dao.save_to_thread(comment2)
        
        thread = dao.get_all_threads()[0]
        self.assertEqual(thread['updated_at'], comment2['created_at'])
    
    def test_only_updates_date_of_relevant_thread(self):
        now = datetime.datetime.now()
        before = now - datetime.timedelta(days=5)
        comment1 = self._comment(created_at=now, line='line1')
        dao.save_to_thread(comment1)
        
        comment2 = self._comment(created_at=before, line='line2')
        dao.save_to_thread(comment2)
        
        thread = [t for t in dao.get_all_threads() if t['line'] == 'line1'][0]
        self.assertEqual(thread['created_at'], comment1['created_at'])
    
    def test_returns_thread_ordered_by_updated_descending(self):
        now = datetime.datetime.now()
        later = now + datetime.timedelta(days=5)
        comment1 = self._comment(id=123, line='someline', created_at=now)
        dao.save_to_thread(comment1)
        comment2 = self._comment(id=124, line='differentline', created_at=later)
        dao.save_to_thread(comment2)
        
        threads = dao.get_all_threads()
        self.assertEqual(threads[0]['line'], 'differentline')
    
    def test_new_comment_pushes_thread_up(self):
        now = datetime.datetime.now()
        later = now + datetime.timedelta(days=5)
        much_later = later + datetime.timedelta(days=5)
        comment1 = self._comment(id=123, line='someline', created_at=now)
        dao.save_to_thread(comment1)
        comment2 = self._comment(id=124, line='differentline', created_at=later)
        dao.save_to_thread(comment2)
        comment3 = self._comment(id=125, line='someline', created_at=much_later)
        dao.save_to_thread(comment3)
        
        threads = dao.get_all_threads()
        self.assertEqual(threads[0]['line'], 'someline')

    def test_returns_thread_comments_ordered_by_created_ascending(self):
        now = datetime.datetime.now()
        later = now + datetime.timedelta(days=5)
        comment1 = self._comment(id=123, body='second', created_at=later)
        dao.save_to_thread(comment1)
        comment2 = self._comment(id=124, body='first!1', created_at=now)
        dao.save_to_thread(comment2)

        threads = dao.get_all_threads()
        self.assertEqual(len(threads), 1)
        self.assertEqual([c['body'] for c in threads[0]['comments']], ['first!1', 'second'])

    def test_get_user_threads_returns_only_threads_initiated_by_given_user(self):
        now = datetime.datetime.now()
        later = now + datetime.timedelta(days=5)
        comment1 = self._comment(id=1, user_id=1, created_at=now)
        comment2 = self._comment(id=2, user_id=2, created_at=later)
        dao.save_to_thread(comment1)
        dao.save_to_thread(comment2)

        self.assertEqual(len(dao.get_user_threads(1)), 1)
        self.assertEqual(len(dao.get_user_threads(2)), 0)

    def test_updates_thread_created_by_when_new_comment_comes_before_previous(self):
        now = datetime.datetime.now()
        later = now + datetime.timedelta(days=5)
        comment1 = self._comment(id=1, user_id=1, created_at=later)
        comment2 = self._comment(id=2, user_id=2, created_at=now)
        dao.save_to_thread(comment1)
        dao.save_to_thread(comment2)

        self.assertEqual(len(dao.get_user_threads(1)), 0)
        self.assertEqual(len(dao.get_user_threads(2)), 1)

    def test_get_user_threads_returns_read_when_thread_was_read_by_user(self):
        comment1 = self._comment(user_id=1)
        object_id = dao.save_to_thread(comment1)['upserted']
        dao.mark_thread_as_read(1, str(object_id))

        thread = dao.get_user_threads(1)[0]
        self.assertTrue(thread['read'])

    def test_get_user_threads_returns_not_read_when_thread_was_not_read_by_user(self):
        dao.save_to_thread(self._comment(user_id=1))

        thread = dao.get_user_threads(1)[0]
        self.assertFalse(thread['read'])

    def test_get_user_threads_returns_not_read_when_thread_was_read_by_other_user(self):
        comment1 = self._comment(user_id=1)
        object_id = dao.save_to_thread(comment1)['upserted']
        dao.mark_thread_as_read(2, str(object_id))

        thread = dao.get_user_threads(1)[0]
        self.assertFalse(thread['read'])

    def test_comment_exists(self):
        comment = self._comment()
        self.assertFalse(dao.comment_exists(comment['id']))

        dao.save_to_thread(comment)
        self.assertTrue(dao.comment_exists(comment['id']))
