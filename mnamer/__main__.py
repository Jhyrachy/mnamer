#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

from teletype.exceptions import TeletypeQuitException, TeletypeSkipException
from mapi.exceptions import MapiNotFoundException

from mnamer import VERSION
from mnamer.args import Arguments
from mnamer.cli import (
    enable_style,
    enable_verbose,
    get_choice,
    msg,
    print_listing,
    print_heading,
)
from mnamer.config import Configuration
from mnamer.exceptions import MnamerConfigException
from mnamer.target import Target


def main():
    args = Arguments()
    config = Configuration(**args.configuration)
    try:
        config.load_file()
    except MnamerConfigException:
        pass
    targets = Target.populate_paths(args.targets, **config)
    enable_style(config.get("nostyle") is False)
    enable_verbose(config.get("verbose") is True)

    # Handle directives and configuration
    if config.get("version"):
        msg("mnamer version %s" % VERSION)
        exit(0)
    elif config.get("config"):
        exit(0)

    # Exit early if no media files are found
    total_count = len(targets)
    if total_count == 0:
        msg("No media files found. Run mnamer --help for usage", "yellow")
        exit(0)

    # Print configuration details
    msg("Starting mnamer\n", "bold underline")
    print_listing(config.preference_dict, "Preferences", True)
    print_listing(config.directive_dict, "Directives", True)
    print_listing(targets, "Targets", True)

    # Main program loop
    success_count = 0
    for target in targets:

        # Process current target
        if config.get("verbose"):
            print_listing(target.metadata)
        try:
            print_heading(target)
            get_choice(target)
            msg("moving to %s" % target.destination.full, bullet=True)
            if not config.get("test"):
                target.relocate()
            msg("OK!\n", "green", True)
            success_count += 1
        except TeletypeQuitException:
            msg("EXITING as per user request\n", "red", True)
            break
        except TeletypeSkipException:
            msg("SKIPPING as per user request\n", "yellow", True)
            continue
        except MapiNotFoundException:
            msg("No matches found, SKIPPING\n", "yellow", True)

    # Display results
    summary = "%d out of %d files processed successfully"
    if success_count == 0:
        msg(summary % (success_count, total_count), "red")
    elif success_count == total_count:
        msg(summary % (success_count, total_count), "green")
    else:
        msg(summary % (success_count, total_count), "yellow")


if __name__ == "__main__":
    main()
