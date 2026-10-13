"""先响应停发请求，再持久化；等待数据库时也阻止下一次平台提交。"""
from threading import Event, Lock

_pause_requested = Event()
_revision = 0
_control_lock = Lock()
persistence_lock = Lock()

def request_pause(paused):
    global _revision
    with _control_lock:
        _revision += 1
        if paused:
            _pause_requested.set()
        else:
            _pause_requested.clear()
        return _revision

def pause_requested():
    return _pause_requested.is_set()

def pause_revision():
    with _control_lock:
        return _revision
