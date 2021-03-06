import pymongo
import config
from time import time

_mongo_client = None

def get_db():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = pymongo.MongoClient()[config.MONGO_DB]
        ensure_indexes(_mongo_client)
    return _mongo_client

def ensure_indexes(mongo_client):
    mongo_client.threads.ensure_index([('created_by', 1)])

def save_to_thread(comment):
    comment_id = comment['id']
    get_db().comments.update({'id': comment_id}, comment, upsert=True)
    
    query = {'commit': comment['commit'],
             'line': comment['line'],
             'path': comment['path']}
    
    res = get_db().threads.update(
            query,
            {
             '$addToSet': {'comments': comment_id},
             '$setOnInsert': {'created_at': comment['created_at'],
                              'created_by': comment['user_id'],
                              'updated_at': comment['created_at']}
             },
            upsert=True)
    
    update_thread_created_fields(query, comment['created_at'], comment['user_id'])
    update_thread_updated_date(query, comment['created_at'])
    return res

def update_thread_created_fields(query, created_at, created_by):
    update_query = query.copy()
    update_query['created_at'] = {'$gt': created_at}
    get_db().threads.update(update_query, {'$set': {'created_at': created_at, 'created_by': created_by}})

def update_thread_updated_date(query, created_at):
    update_query = query.copy()
    update_query['updated_at'] = {'$lt': created_at}
    get_db().threads.update(update_query, {'$set': {'updated_at': created_at}})

def get_user_threads(user_id):
    return _get_threads({'created_by': user_id}, user_id)

def get_all_threads():
    return _get_threads({})

def _get_threads(query, user_id=None):
    threads = list(get_db().threads.find(query).sort([('updated_at', -1)]))
    res = []

    comment_ids = sum((thread['comments'] for thread in threads), [])
    comment_by_id = dict((c['id'], c) for c in get_comments(comment_ids))

    for thread in threads:
        read = user_id is not None and user_id in thread.get('read',[])
        res.append({
            'id': str(thread['_id']),
            'read': read,
            'path': thread['path'],
            'line': thread['line'],
            'commit': thread['commit'],
            'created_at': thread['created_at'],
            'updated_at': thread['updated_at'],
            'comments': sorted((comment_by_id[cid] for cid in thread['comments']),
                               key=lambda c: c['created_at'])
        })
    return res

def get_comments(comment_ids):
    comments = list(get_db().comments.find({'id': {'$in': comment_ids}}).sort('created_at', 1))
    return remove_object_ids(comments)

def remove_object_ids(comments):
    res = []
    for comment in comments:
        c = dict(comment)
        del c['_id']
        res.append(c)
    return res

def mark_thread_as_read(user_id, thread_id):
    get_db().threads.update(
            {'_id': pymongo.helpers.bson.ObjectId(thread_id)},
            {'$addToSet': {'read': user_id}})

def comment_exists(comment_id):
    return get_db().comments.find_one({'id': comment_id}) is not None


