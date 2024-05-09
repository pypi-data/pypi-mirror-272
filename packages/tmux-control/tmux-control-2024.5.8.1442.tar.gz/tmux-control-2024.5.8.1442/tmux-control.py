#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# tmux-control                                                                 #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is a way to configure and control tmux.                         #
#                                                                              #
# copyright (C) 2015 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses>.                                               #
#                                                                              #
################################################################################

# launch modes

analysis mode:
-----------------------
|                     |
|       ranger        |
|                     |
|                     |
|---------------------|
|                     |
|      terminal       |
|                     |
|                     |
-----------------------

badass mode (does not work via SSH):
-----------------------
| ranger   |          |
|----------|          |
| terminal |          |
|----------|          |
| htop     |  ranger  |
|----------|          |
| arXiv    |          |
|----------|          |
| cmus     |          |
-----------------------

detail mode:
-----------------------
|          |          |
| ranger   |          |
|----------|          |
| terminal |          |
|----------|  ranger  |
| htop     |          |
|----------|          |
| arXiv    |          |
|          |          |
-----------------------

edit mode (default):
-----------------------
|          |          |
|          |          |
|          |          |
|          |          |
| terminal |  ranger  |
|          |          |
|          |          |
|          |          |
|          |          |
-----------------------

Nvidia mode:
-----------------------
|                     |
|        htop         |
|                     |
|                     |
|---------------------|
|                     |
|        nvtop        |
|                     |
|                     |
-----------------------

run mode:
-----------------------
|                     |
|                     |
|                     |
|                     |
|      scripts        |
|                     |
|                     |
|                     |
|                     |
-----------------------

work mode:
-----------------------
|                     |
|       ranger        |
|---------------------|
|                     |
|      terminal       |
|---------------------|
|          |          |
|  ranger  |  cmus    |
|          |          |
-----------------------

usage:
    program [options]

options:
    -h, --help  display help message
    --version   display version and exit

    --analysis  analysis configuration
    --badass    badass configuration
    --detail    detail configuration
    --edit      edit configuration
    --nvidia    Nvidia configuration
    --run       run configuration
    --work      work configuration

    --directory=NAME  directory of scripts to run             [default: scripts]
    --extension=EXT   scripts extension (set to none for any) [default: sh]
"""

import docopt
import os
import re
import sys

name    = "tmux-control"
version = "2024-05-08T1442Z"

def main(options):

    engage_configuration_analysis = options["--analysis"]
    engage_configuration_badass   = options["--badass"]
    engage_configuration_detail   = options["--detail"]
    engage_configuration_edit     = options["--edit"]
    engage_configuration_Nvidia   = options["--nvidia"]
    engage_configuration_run      = options["--run"]
    engage_configuration_work     = options["--work"]

    directoryname                 = options["--directory"]
    extension_required            = options["--extension"]
    if extension_required.lower() == "none":
        extension_required = None

    host_name = os.uname()[1]
    if "cern.ch" in host_name:
        executable = "/usr/bin/tmux"
    elif "physics.gla.ac.uk" in host_name:
        executable = "/usr/bin/tmux"
    else:
        executable = "tmux"

    configuration_analysis = \
    """
    set -g set-remain-on-exit on
    new -s "ANALYSIS"
    set-option -g prefix C-a
    unbind C-b
    bind - split-window -v
    bind | split-window -h
    bind k kill-session
    bind K kill-server
    ## colours
    set-option -g window-status-current-bg yellow
    set-option -g pane-active-border-fg yellow
    set -g status-fg black
    set -g status-bg '#FEFE0A'
    set -g message-fg black
    set -g message-bg '#FEFE0A'
    set -g message-command-fg black
    set -g message-command-bg '#FEFE0A'
    set-option -g mode-keys vi
    set -g history-limit 20000
    ## mouse mode
    set -g mouse on
    ## status
    set-option -g status-interval 1
    set-option -g status-left-length 20
    set-option -g status-left ''
    set-option -g status-right '%Y-%m-%dT%H%M%S '
    ## run programs in panes
    # split up-down
    split-window -v
    # split left up
    select-pane -t 0
    send-keys 'ranger' Enter
    select-pane -t 1
    send-keys 'clear' Enter
    set -g set-remain-on-exit off
    """

    configuration_badass = \
    """
    set -g set-remain-on-exit on
    new -s "BADASS"
    set-option -g prefix C-a
    unbind C-b
    bind - split-window -v
    bind | split-window -h
    bind k kill-session
    bind K kill-server
    ## colours
    set-option -g window-status-current-bg yellow
    set-option -g pane-active-border-fg yellow
    set -g status-fg black
    set -g status-bg '#FEFE0A'
    set -g message-fg black
    set -g message-bg '#FEFE0A'
    set -g message-command-fg black
    set -g message-command-bg '#FEFE0A'
    set-option -g mode-keys vi
    set -g history-limit 20000
    ## mouse mode
    set -g mouse on
    ## status
    set-option -g status-interval 1
    set-option -g status-left-length 20
    set-option -g status-left ''
    set-option -g status-right '%Y-%m-%dT%H%M%S '
    ## run programs in panes
    # split left-right
    split-window -h
    # split left up
    select-pane -t 0
    split-window -v
    select-pane -t 0
    split-window -v
    select-pane -t 0
    split-window -v
    select-pane -t 3
    split-window -v
    select-pane -t 0
    send-keys 'ranger' Enter
    select-pane -t 1
    send-keys 'clear' Enter
    select-pane -t 2
    send-keys 'htop' Enter
    select-pane -t 3
    send-keys 'elinks http://arxiv.org/list/hep-ph/new' Enter
    select-pane -t 4
    send-keys 'cmus' Enter
    select-pane -t 5
    send-keys 'ranger' Enter
    select-pane -t 4
    set -g set-remain-on-exit off
    """

    configuration_detail = \
    """
    set -g set-remain-on-exit on
    new -s "DETAIL"
    set-option -g prefix C-a
    unbind C-b
    bind - split-window -v
    bind | split-window -h
    bind k kill-session
    bind K kill-server
    ## colours
    set-option -g window-status-current-bg yellow
    set-option -g pane-active-border-fg yellow
    set -g status-fg black
    set -g status-bg '#FEFE0A'
    set -g message-fg black
    set -g message-bg '#FEFE0A'
    set -g message-command-fg black
    set -g message-command-bg '#FEFE0A'
    set-option -g mode-keys vi
    set -g history-limit 20000
    ## mouse mode
    set -g mouse on
    ## status
    set-option -g status-interval 1
    set-option -g status-left-length 20
    set-option -g status-left ''
    set-option -g status-right '%Y-%m-%dT%H%M%S '
    ## run programs in panes
    # split left-right
    split-window -h
    # split left up
    select-pane -t 0
    split-window -v
    select-pane -t 0
    split-window -v
    select-pane -t 0
    split-window -v
    select-pane -t 0
    send-keys 'ranger' Enter
    select-pane -t 1
    send-keys 'clear' Enter
    select-pane -t 2
    send-keys 'htop' Enter
    select-pane -t 3
    send-keys 'elinks http://arxiv.org/list/hep-ph/new' Enter
    select-pane -t 4
    send-keys 'ranger' Enter
    set -g set-remain-on-exit off
    """

    configuration_edit = \
    """
    set -g set-remain-on-exit on
    new -s "EDIT"
    set-option -g prefix C-a
    unbind C-b
    bind - split-window -v
    bind | split-window -h
    bind k kill-session
    bind K kill-server
    ## colours
    set-option -g window-status-current-bg yellow
    set-option -g pane-active-border-fg yellow
    set -g status-fg black
    set -g status-bg '#FEFE0A'
    set -g message-fg black
    set -g message-bg '#FEFE0A'
    set -g message-command-fg black
    set -g message-command-bg '#FEFE0A'
    set-option -g mode-keys vi
    set -g history-limit 20000
    ## mouse mode
    set -g mouse on
    ## status
    set-option -g status-interval 1
    set-option -g status-left-length 20
    set-option -g status-left ''
    set-option -g status-right '%Y-%m-%dT%H%M%S '
    ## run programs in panes
    # split left-right
    split-window -h
    select-pane -t 0
    send-keys 'clear' Enter
    select-pane -t 1
    send-keys 'ranger' Enter
    set -g set-remain-on-exit off
    """

    configuration_Nvidia = \
    """
    set -g set-remain-on-exit on
    new -s "NVIDIA"
    set-option -g prefix C-a
    unbind C-b
    bind - split-window -v
    bind | split-window -h
    bind k kill-session
    bind K kill-server
    ## colours
    set-option -g window-status-current-bg yellow
    set-option -g pane-active-border-fg yellow
    set -g status-fg black
    set -g status-bg '#FEFE0A'
    set -g message-fg black
    set -g message-bg '#FEFE0A'
    set -g message-command-fg black
    set -g message-command-bg '#FEFE0A'
    set-option -g mode-keys vi
    set -g history-limit 20000
    ## mouse mode
    set -g mouse on
    ## status
    set-option -g status-interval 1
    set-option -g status-left-length 20
    set-option -g status-left ''
    set-option -g status-right '%Y-%m-%dT%H%M%S '
    ## run programs in panes
    # split up-down
    split-window -v
    # split left up
    select-pane -t 0
    send-keys 'htop' Enter
    select-pane -t 1
    send-keys 'watch -n 0.5 nvidia-smi' Enter
    set -g set-remain-on-exit off
    """

    configuration_run = \
    """
    set -g set-remain-on-exit on
    new -s "RUN"
    set-option -g prefix C-a
    unbind C-b
    bind - split-window -v
    bind | split-window -h
    bind k kill-session
    bind K kill-server
    ## colours
    set-option -g window-status-current-bg yellow
    set-option -g pane-active-border-fg yellow
    set -g status-fg black
    set -g status-bg '#FEFE0A'
    set -g message-fg black
    set -g message-bg '#FEFE0A'
    set -g message-command-fg black
    set -g message-command-bg '#FEFE0A'
    set-option -g mode-keys vi
    set -g history-limit 20000
    ## mouse mode
    set -g mouse on
    ## status
    set-option -g status-interval 1
    set-option -g status-left-length 20
    set-option -g status-left ''
    set-option -g status-right '%Y-%m-%dT%H%M%S '
    set -g set-remain-on-exit off
    ## run scripts in windows
    """

    configuration_work = \
    """
    set -g set-remain-on-exit on
    new -s "WORK"
    set-option -g prefix C-a
    unbind C-b
    bind - split-window -v
    bind | split-window -h
    bind k kill-session
    bind K kill-server
    ## colours
    set-option -g window-status-current-bg yellow
    set-option -g pane-active-border-fg yellow
    set -g status-fg black
    set -g status-bg '#FEFE0A'
    set -g message-fg black
    set -g message-bg '#FEFE0A'
    set -g message-command-fg black
    set -g message-command-bg '#FEFE0A'
    set-option -g mode-keys vi
    set -g history-limit 20000
    ## mouse mode
    set -g mouse on
    ## status
    set-option -g status-interval 1
    set-option -g status-left-length 20
    set-option -g status-left ''
    set-option -g status-right '%Y-%m-%dT%H%M%S '
    ## run programs in panes
    split-window -v
    select-pane -t 1
    split-window -v
    select-pane -t 3
    split-window -h
    select-pane -t 0
    send-keys 'ranger' Enter
    select-pane -t 1
    send-keys 'clear' Enter
    select-pane -t 2
    send-keys 'ranger' Enter
    select-pane -t 3
    send-keys 'cmus' Enter
    set -g set-remain-on-exit off
    """

    if engage_configuration_run:
        filepaths = natural_sort(filepaths_at_directory(
            directory          = directoryname,
            extension_required = extension_required
        ))
        for index, filepath in enumerate(filepaths):
            configuration_run += "    new-window\n"
            configuration_run += "    rename-window -t {index} '{name}'\n".format(
                index = index + 1,
                name  = os.path.split(filepath)[1]
            )
            configuration_run += "    select-window -t {index}\n".format(
                index = index + 1
            )
            configuration_run += "    send-keys '{filepath}' Enter\n".format(
                filepath = filepath
            )
        #configuration_run += "    choose-window\n"
        configuration_run += "    select-window -t 0\n"

    if engage_configuration_analysis:
        configuration_tmux = configuration_analysis
    elif engage_configuration_badass:
        configuration_tmux = configuration_badass
    elif engage_configuration_detail:
        configuration_tmux = configuration_detail
    elif engage_configuration_edit:
        configuration_tmux = configuration_edit
    elif engage_configuration_Nvidia:
        configuration_tmux = configuration_Nvidia
    elif engage_configuration_run:
        configuration_tmux = configuration_run
    elif engage_configuration_work:
        configuration_tmux = configuration_work
    else:
        configuration_tmux = configuration_edit

    command                                             = \
        "configuration_tmux=\"$(mktemp)\" && { echo \"" + \
        configuration_tmux                              + \
        "\" > \"${configuration_tmux}\"; "              + \
        executable                                      + \
        " -f \"${configuration_tmux}\" attach; "        + \
        "unlink \"${configuration_tmux}\"; }"

    os.system(command)
    sys.exit()

def natural_sort(list_object):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanumeric_key = lambda key: [convert(text) for text in re.split("([0-9]+)", key)]
    return sorted(list_object, key = alphanumeric_key)

def filepaths_at_directory(directory=None, extension_required=None):
    if not os.path.isdir(directory):
        print(f"error -- directory {directory} not found")
        raise(IOError)
    filepaths = [os.path.abspath(os.path.join(directory, filename))\
                 for filename in os.listdir(directory)\
                 if os.path.isfile(os.path.join(directory, filename))]
    if extension_required:
        filepaths = [filepath for filepath in filepaths if extension_required in\
                     os.path.splitext(filepath)[1]]
    return filepaths

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)
