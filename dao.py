import pymongo
import settings

def get_db():
    return pymongo.MongoClient()[settings.MONGO_DB]

def save_to_thread(comment):
    comment_id = comment['id']
    get_db().comments.update({'id': comment_id}, comment, upsert=True)
    
    query = {'commit': comment['commit'],
             'line': comment['line'],
             'path': comment['path']}
    
    get_db().threads.update(
            query,
            {
             '$push': {'comments': comment_id},
             '$setOnInsert': {'created_at': comment['created_at'],
                              'created_by': comment['user_id'],
                              'updated_at': comment['created_at']}
             },
            upsert=True)
    
    update_thread_created_fields(query, comment['created_at'], comment['user_id'])
    update_thread_updated_date(query, comment['created_at'])

def update_thread_created_fields(query, created_at, created_by):
    update_query = query.copy()
    update_query['created_at'] = {'$gt': created_at}
    get_db().threads.update(update_query, {'$set': {'created_at': created_at, 'created_by': created_by}})

def update_thread_updated_date(query, created_at):
    update_query = query.copy()
    update_query['updated_at'] = {'$lt': created_at}
    get_db().threads.update(update_query, {'$set': {'updated_at': created_at}})

def get_user_threads(user_id):
    return _get_threads({'created_by': user_id})

def get_all_threads():
    return _get_threads({})

def _get_threads(query):
    threads = get_db().threads.find(query).sort([('updated_at', -1)])
    res = []
    for thread in threads:
        res.append({
            'path': thread['path'],
            'line': thread['line'],
            'commit': thread['commit'],
            'created_at': thread['created_at'],
            'updated_at': thread['updated_at'],
            'comments': get_comments(thread['comments'])
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