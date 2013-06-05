import pymongo
import settings

mongodb = pymongo.Connection()[settings.MONGO_DB]

def save_to_thread(comment):
    mongodb.threads.update(
            {'commit': comment['commit'], 'line': comment['line'], 'path': comment['path']},
            {'$push': {'comments': comment}},
            upsert=True)
