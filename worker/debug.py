enable_log = False


def log(msg):
    global enable_log

    if enable_log:
        with open('./log.txt', 'a') as f:
            f.write(msg)
            f.write('\n')
