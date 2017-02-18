#!/bin/bash

FILES_TO_TYPECHECK=(JeffersonShell.py JeffersonGUI.py)

REPODIR=$(dirname $0)
export PYTHONPATH=$REPODIR/src:$PYTHONPATH

RESET="\e[0m"
BOLD="\e[1m"
RED="\e[91m"
GREEN="\e[92m"

echo -n "* Type checking... "
for TYPED_FILE in $FILES_TO_TYPECHECK; do
  MYPY_REPORT=$(mypy --silent-imports $REPODIR/src/$TYPED_FILE)
  if [[ $? -ne 0 ]]; then
    echo -e "${BOLD}${RED}Failed ✗${RESET}"
    echo "$MYPY_REPORT"
    exit 1
  fi
done
echo -e "${BOLD}${GREEN}OK ✓${RESET}"

echo -n "* Running test suite... "
for FILE_TO_TEST in $REPODIR/test/*.py; do
  TEST_REPORT=$(python3 $FILE_TO_TEST -v 2>&1)
  if [[ $? -ne 0 ]]; then
    echo -e "${BOLD}${RED}Failed ✗${RESET}"
    echo "$TEST_REPORT"
    exit 1
  fi
done
echo -e "${BOLD}${GREEN}OK ✓${RESET}"
