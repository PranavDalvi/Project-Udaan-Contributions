#!/bin/bash

# path to your Python script
python_script="/home/main.py"

# [""]="-im  -l  -m  -s  -e "
declare -A file_args=(


)

for file in "${!file_args[@]}"; do
    file_arguments="${file_args[$file]}"
    command="python $python_script -i $file $file_arguments"
    echo "Running command: $command"
    $command

    echo "--------------------------------------------------------"
done
