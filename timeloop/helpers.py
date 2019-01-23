from timeloop.exceptions import ServiceExit


def service_shutdown(signum, frame):
    raise ServiceExit
