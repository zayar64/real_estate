#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

all_commands = {0: 'changepassword', 1: 'createsuperuser', 2: 'remove_stale_contenttypes', 3: 'check', 4: 'compilemessages', 5: 'createcachetable', 6: 'dbshell', 7: 'diffsettings', 8: 'dumpdata', 9: 'flush', 10: 'inspectdb', 11: 'loaddata', 12: 'makemessages', 13: 'makemigrations', 14: 'migrate', 15: 'optimizemigration', 16: 'sendtestemail', 17: 'shell', 18: 'showmigrations', 19: 'sqlflush', 20: 'sqlmigrate', 21: 'sqlsequencereset', 22: 'squashmigrations', 23: 'startapp', 24: 'startproject', 25: 'test', 26: 'testserver', 27: 'clearsessions', 28: 'collectstatic', 29: 'findstatic', 30: 'runserver'}

main_commands = {
    0: None,
    1: "runserver",
    2: "test",
    3: "makemigrations",
    4: "migrate",
    5: "createsuperuser",
    6: "startproject",
    7: "startapp"
}

key = 0

command = main_commands[key]

if key:
    sys.argv.append(command)

if key == 1:
    port = "8000"
    sys.argv.append(port)

if key == 3:
    target = input("Target to make migrations : ")
    if target:
        sys.argv.append(target)

if key == 6:
    name = input("Project name : ")
    sys.argv.append(name)

if key == 7:
    name = input("App name : ")
    sys.argv.append(name)



from real_estate.settings import development, production

states = {
    1: "development",
    2: "production"
}

key = 1

state = states.get(key)

if state == "development":
    configured_settings = development.configured_settings
else:
    configured_settings = production.configured_settings

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate.settings.%s' % (state))
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
