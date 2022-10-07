#!/bin/bash
title=$1
msg=$2

osascript -e "display notification \"$msg\" with title \"$title\"  sound name \"Frog\""
