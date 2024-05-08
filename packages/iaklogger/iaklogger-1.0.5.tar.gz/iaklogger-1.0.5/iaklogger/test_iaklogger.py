import iaklogger as iak


def test_log():
    # Test case 1: Log message with default tag
    assert iak.log("Hello, World!") == True

    # Test case 2: Log message with custom tag
    assert iak.log("Error occurred", tags=["ERROR"]) == True

    # Test case 3: iak.log message with multiple tags
    assert iak.log("Warning", tags=["WARNING", "APP"]) == True

    # Test case 4: iak.log message with newline after tag
    assert iak.log("Info", new_line=True) == True

    # Test case 5: Mute default tag
    iak.OPTIONS.mute_default = True
    assert iak.log("Default message") == False

    # Test case 6: Mute all iak.logs
    iak.OPTIONS.mute_all = True
    assert iak.log("This should not be logged") == False

    # Test case 7: Log message to file
    iak.OPTIONS.mute_all = False
    iak.OPTIONS.mute_default = False
    iak.OPTIONS.log_file = "log.txt"
    assert iak.log("Log to file") == True

    # Test case 8: Log message exceeding file size limit
    iak.OPTIONS.log_file_max_size_mb = 0.001
    assert iak.log("Large log message") == True

    # Test case 9: Log message with tags and time
    iak.OPTIONS.show_tags = True
    iak.OPTIONS.show_time = True
    assert iak.log("Debug", tags=["DEBUG"]) == True

    # Test case 10: Log message with invalid tags
    iak.OPTIONS.allowed_tags = ["INFO", "WARNING"]
    assert iak.log("Invalid tag", tags=["ERROR", "DEBUG"]) == False


iak.OPTIONS.allowed_tags = [
    "FORECAST",
    "RESULTS",
    "OPTIMIZER",
    "SOLVING",
    "CONTINUOUS",
    "SYSMANAGER",
    "NETWORK",
    "LOADING",
    "UPDATE",
    "DEBUG",
    "TESTS",
    "ERROR",
    "INFO",
    "WARNING",
    "CONVERSATION",
    "APP"
]
iak.OPTIONS.show_tags = True

test_log()
