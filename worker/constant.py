PROCESSED = 0
FAILED = 1
EXCEPTION = 2

retcode_table = {
    'processed': PROCESSED,
    'failed': FAILED,
    'exception': EXCEPTION,
}


def get_retcode(output):
    i = output[0] - ord('0')
    if i < 0 or i >= len(retcode_table):
        return -1
    return i


def verbose_retcode(c):
    return list(retcode_table.keys())[c]
