import logging
import sys



class StreamLogger(object):

    def __init__(self, stream, log, prefix=''):
        self.stream = stream
        self.prefix = prefix
        self.data = ''
        self.log=log

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

        self.data += data
        tmp = str(self.data)
        if '\x0a' in tmp or '\x0d' in tmp:
            tmp = tmp.rstrip('\x0a\x0d')
            self.log.info('%s%s' % (self.prefix, tmp))
            self.data = ''

    def flush(self):
        """This is sometimes needed"""
        pass


if __name__ =="__main__":
    log = logging.getLogger('stdxxx')
    logging.basicConfig(level=logging.INFO,
                        filename='text.log',
                        filemode='a')
    
    sys.stdout = StreamLogger(sys.stdout, '[stdout] ')    
    print 'test for stdout'