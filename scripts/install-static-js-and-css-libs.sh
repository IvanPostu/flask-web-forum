#!/bin/bash

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

# If there is an error code, interrupts the execution process
Error_Checker() {
    exit_code="$1"
    error_msg="$2"
    success_msg="$3"

    if [ $exit_code -eq 0 ];
    then
        echo -e "${green}${success_msg}${reset}"
    else
        echo -e "${red}${error_msg}${reset} Exit code: ${exit_code}"
        exit 1 # terminate and indicate error
    fi
}
step=1

echo -e "${yellow}Run script for install static js and css libraries from npm and move it into flask project static files directory.${reset}"

echo -e "${magenta}Step ${step}: Download static js and css files using npm and nodejs.${reset}"

cd ./static_libs_builder

npm install
Error_Checker $? "Step ${step} error!" "Step ${step} successfully completed!"
step=$(( $step + 1 ))

echo -e "${magenta}Step ${step}: Move downloaded libraries in separate folder.${reset}"

npm run build
Error_Checker $? "Step ${step} error!" "Step ${step} successfully completed!"
step=$(( $step + 1 ))

# back to project dir
cd ..

echo -e "${magenta}Step ${step}: Move necessary libraries from separate folder to flask project static folder.${reset}"

mkdir -p ./web-application/static/npm_libs
mv ./static_libs_builder/collected_static_libs/** ./web-application/static/npm_libs
Error_Checker $? "Step ${step} error!" "Step ${step} successfully completed!"
step=$(( $step + 1 ))

echo -e "${yellow}Script completed successfully.${reset}"

