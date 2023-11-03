#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def get_project_package(project_dir):
    if (project_dir / "project_name").exists():
        return "project_name"

    return "life_manager_app"


PROJECT_DIR = Path(__file__).absolute().parent
PROJECT_PACKAGE = get_project_package(PROJECT_DIR)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(PROJECT_PACKAGE))
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
