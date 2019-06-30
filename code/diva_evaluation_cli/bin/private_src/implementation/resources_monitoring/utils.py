"""Monitor module: utils module for resource monitoring

"""
import psutil


def psutil_snapshot():
    """ Take a snapshot of cpu and memory usage
    """
    snapshot_dict = {}

    snapshot_dict = {
        'total_cpus_usage': psutil.cpu_percent(interval=1, percpu=True),
        'total_memory_used': psutil_parse_readable_bytes(
                                    psutil.virtual_memory().used
                            ),
        'total_memory': psutil_parse_readable_bytes(
                                    psutil.virtual_memory().total
                            ),
        'total_disk_io_read': psutil_parse_readable_bytes(
                                    psutil.disk_io_counters(perdisk=False, nowrap=True).read_bytes
                            ),
        'total_disk_io_write': psutil_parse_readable_bytes(
                                    psutil.disk_io_counters(perdisk=False, nowrap=True).write_bytes
                            )
        }

    return snapshot_dict


def psutil_snapshot_process(pid, snap_children=True):
    """

    Return the psutil.Process attribute in a dictionnary
    Monitor the children too if desc_children

    Args:
        pid (int): Pid to monitor
        snap_children (boolean): Whether to recurse the function on the process' children

    Returns:
        dict: resources usage for a given pid and its children::

            if snap_children
                {'command':'some_command', ...}
            else:
                {'command':'some_command', ... {'children': [
                    {'command':'some_command', ... {'children': {} }}},
                    ... ]
                }}

    """
    proc = psutil.Process(pid)
    pic = {}

    with proc.oneshot():

        if proc.is_running() and proc.status()!=psutil.STATUS_ZOMBIE:

            all_info = proc.as_dict()

            pic['command'] = ' '.join(all_info.get('cmdline'))
            pic['num_threads'] = all_info.get('num_threads')

            mem_info = all_info.get('memory_info')
            pic['memory_used'] = psutil_parse_readable_bytes(mem_info.rss) if mem_info else None


            if snap_children:
                # Collect descendant prcesses' info
                children = proc.children()
                if len(children) > 0:
                    pic["children"] = []
                    for c in children:
                        cPic = shot(c.pid, snap_children)
                        pic["children"].append(cPic)
    return pic


def psutil_parse_readable_bytes(n_bytes):
    """Parse a number of byte in a human readable format

    Args:
        n_bytes (:obj:) Number of bytes, castable to an int

    Returns:
        Human readable abount of bytes in the best memory unit possible

    Examples:
        >>> psutil_parse_readable_bytes(10000)
        '9.8K'
        >>> psutil_parse_readable_bytes(100001221)
        '95.4M'

    """
    n = int(n_bytes)
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n
