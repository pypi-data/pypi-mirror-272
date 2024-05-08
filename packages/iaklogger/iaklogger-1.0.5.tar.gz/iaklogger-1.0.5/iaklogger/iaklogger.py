import time

DEFAULT = "DEFAULT"  # prints default messages


class OPTIONS:
    allowed_tags = []
    """list (Default: Empty): list of allowed tags. Tag DEFAULT is always allowed unless mute_default is true."""
    log_file = None
    """str (Default: None): File path to save the log. If set, the log will be saved to this file."""
    log_file_max_size_mb = 1024 * 1024 * 10
    """int (Default: 10MB): Maximum size of the log file. If the file exceeds this size, it will be truncated."""
    mute_default = False
    """bool (Default: False): True to mute DEFAULT tag."""
    mute_all = False
    """bool (Default: False): True to mute all logs."""
    newline_after_tag = False
    """bool (Default: False): True to add a newline after tags."""
    show_tags = False
    """bool (Default: False): True to print tags before the message."""
    show_time = False
    """bool (Default: False): True to print time before the message."""


def check_tags(list1, list2):
    return all(tag in list2 for tag in list1)


def log(printable_obj, tags=[DEFAULT], new_line=False):
    """
    Logs the message to the console and/or to a file.
    Args:
        printable_obj (str): Message to log.
        tags (list, optional): List of tags for this message. Default to [DEFAULT].
    Returns:
        bool: True if the message was logged, False otherwise.
    """
    new_line_str = ""
    tags_str = ""
    time_str = ""
    if not check_tags(tags, OPTIONS.allowed_tags) and (not check_tags(tags, [DEFAULT]) or OPTIONS.mute_default):
        return False
    elif not OPTIONS.mute_all:
        if OPTIONS.newline_after_tag or new_line:
            new_line_str = "\n"
        if OPTIONS.show_tags:
            tags_str = f"[{'-'.join(tags)}] "
            # printable_obj = f"[{'-'.join(tags)}]{new_line}{printable_obj}"
        if OPTIONS.show_time:
            time_str = f'{time.strftime("%Y-%m-%d %H:%M:%S")} '
            # printable_obj = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {printable_obj}"
        print(f"{time_str}{tags_str}{new_line_str}{printable_obj}")
        if OPTIONS.log_file:
            log_to_file(printable_obj)
        return True


def log_to_file(printable_obj):
    printable_obj_size = len(printable_obj.encode('utf-8'))
    with open(OPTIONS.log_file, "a+") as f:
        f.seek(0, 2)  # Mueve el puntero al final del archivo
        if f.tell() + printable_obj_size < OPTIONS.log_file_max_size_mb * 1024 * 1024:
            f.write(printable_obj + "\n")
        else:
            f.seek(0)  # Mueve el puntero al principio del archivo
            lines = f.readlines()
            total_size = sum(len(line.encode('utf-8')) for line in lines)
            while lines and total_size + printable_obj_size > OPTIONS.log_file_max_size_mb * 1024 * 1024:
                total_size -= len(lines.pop(0).encode('utf-8'))
            f.seek(0)
            f.truncate()
            f.writelines(lines)
            f.write(printable_obj + "\n")
