import cPickle as pickle
from uuid import uuid4
import time

class RedisSessionStore:

    def __init__(self, redis_connection, **options):
        self.options = {
            'key_prefix': 'session',
            'expire': 7200,
        }
        self.options.update(options)
        self.redis = redis_connection

    def prefixed(self, sid):
        return '%s:%s' % (self.options['key_prefix'], sid)

    def generate_sid(self, ):
        return uuid4().get_hex()

    def get_session(self, sid, name):
        data = self.redis.hget(self.prefixed(sid), name)
        session = pickle.loads(data) if data else dict()
        return session

    def set_session(self, sid, session_data, name):
        expiry = self.options['expire']
        self.redis.hset(self.prefixed(sid), name, pickle.dumps(session_data))
        if expiry:
            self.redis.expire(self.prefixed(sid), expiry)

    def delete_session(self, sid):
        self.redis.delete(self.prefixed(sid))


class Session:

    def __init__(self, session_store, sessionid=None):
        self._store = session_store
        self._sessionid = sessionid if sessionid else self._store.generate_sid()
        self._sessiondata = self._store.get_session(self._sessionid, 'data')
        self.dirty = False

    def clear(self):
        self._store.delete_session(self._sessionid)

    def access(self, remote_ip):
        access_info = {'remote_ip':remote_ip, 'time':'%.6f' % time.time()}
        self._store.set_session(
                self._sessionid,
                'last_access',
                pickle.dumps(access_info)
                )

    def last_access(self):
        access_info = self._store.get_session(self._sessionid, 'last_access')
        return pickle.loads(access_info)

    @property
    def sessionid(self):
        return self._sessionid

    def __getitem__(self, key):
        return self._sessiondata[key]

    def __setitem__(self, key, value):
        self._sessiondata[key] = value
        self._dirty()

    def __delitem__(self, key):
        del self._sessiondata[key]
        self._dirty()

    def __len__(self):
        return len(self._sessiondata)

    def __contains__(self, key):
        return key in self._sessiondata

    def __iter__(self):
        for key in self._sessiondata:
            yield key

    def __repr__(self):
        return self._sessiondata.__repr__()

    def __del__(self):
        if self.dirty:
            self._save()

    def _dirty(self):
        self.dirty = True

    def _save(self):
        self._store.set_session(self._sessionid, self._sessiondata, 'data')
        self.dirty = False
        
'''
usage in tornado:

class Application(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db_session = db_session
        self.redis = redis.StrictRedis()
        self.session_store = RedisSessionStore(self.redis)

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.session['user'] if self.session and 'user' in self.session else None

    @property
    def session(self):
        sessionid = self.get_secure_cookie('sid')
        session = Session(self.application.session_store, sessionid)
        if not sessionid:
            self.set_secure_cookie('sid', session.sessionid)
        return session

'''
