#!/bin/bash
cd "$(dirname "$0")" || exit
# shellcheck disable=SC2103
cd ..
python -m PyJudge $1
pause