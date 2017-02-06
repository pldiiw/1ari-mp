#!/bin/bash

RESET="\e[0m"
BOLD="\e[1m"
RED="\e[91m"
GREEN="\e[92m"
YELLOW="\e[93m"

yapf -rdp src/ test/
echo -en "${YELLOW}Apply these modifications? [Yy/*]${RESET} "
read -n 1 choice
echo
if [ $choice = "y" -o $choice = "Y" ]; then
  echo -n "Applying..."
  yapf -rip src/ test/
  if [ $? -eq 0 ]; then
    echo -e " ${BOLD}${GREEN}Done ✓${RESET}"
  else
    echo -e " ${BOLD}${RED}Failed ✗${RESET}"
  fi
else
  echo -e "${RED}Aborting${RESET}..."
fi
