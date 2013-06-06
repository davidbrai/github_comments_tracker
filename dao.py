import pymongo
import settings

def get_db():
    return pymongo.Connection()[settings.MONGO_DB]

def save_to_thread(comment):
    comment_id = comment['id']
    get_db().comments.update({'id': comment_id}, comment, upsert=True)
    
    query = {'commit': comment['commit'],
             'line': comment['line'],
             'path': comment['path']}
    
    get_db().threads.update(
            query,
            {'$push': {'comments': comment_id}},
            upsert=True)


def get_threads():
    threads = get_db().threads.find()
    res = []
    for thread in threads:
        res.append({
            'path': thread['path'],
            'line': thread['line'],
            'commit': thread['commit'],
            'comments': get_comments(thread['comments'])
        })
    return res

def get_comments(comment_ids):
    print "got comment ids: %s" % comment_ids
    comments = list(get_db().comments.find({'id': {'$in': comment_ids}}))
    return remove_object_ids(comments)

def remove_object_ids(comments):
    res = []
    for comment in comments:
        c = dict(comment)
        del c['_id']
        res.append(c)
    return res