#!/bin/bash

# Parameters
type=""
error_msg="Parameter \"type\" is invalid or undefined."

# Color variables
black=`tput setaf 0`
red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
magenta=`tput setaf 5`
cyan=`tput setaf 6`
white=`tput setaf 7`

reset=`tput sgr0`

# Parse named parameters
for arg in "$@"
  do
    index=$(echo $arg | cut -f1 -d=)
    val=$(echo $arg | cut -f2 -d=)
    # echo "${index} -- ${val}"
  case $index in
    type) type=$val;; 
    *)
  esac
done

# Check if variable type is assigned.
if [ -z "$type" ]
  then
    echo -e "${red}${error_msg}${reset}"
fi

if [ "$type" == "build-static-css-and-js-libs" ]; then 
    bash ${PWD}/scripts/install-static-js-and-css-libs.sh
fi