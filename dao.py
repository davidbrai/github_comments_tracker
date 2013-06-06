import pymongo
import settings

def get_db():
    return pymongo.Connection()[settings.MONGO_DB]

def save_to_thread(comment):
    get_db().threads.update(
            {'commit': comment['commit'], 'line': comment['line'], 'path': comment['path']},
            {'$push': {'comments': comment}},
            upsert=True)


def get_threads():
    threads = get_db().threads.find()
    res = []
    for thread in threads:
        res.append({
            'path': thread['path'],
            'line': thread['line'],
            'commit': thread['commit'],
            'comments': thread['comments']
        })
    return res