__author__ = 'evan'
import logger


LOG = logger.get_loger()

class LogIp(object):

    def process_request(self, request):
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        path = request.get_full_path()
        message = 'request ip: ' + ip + ', path: ' + path
        LOG.warn(message)
