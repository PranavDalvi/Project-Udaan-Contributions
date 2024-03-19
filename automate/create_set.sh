#!/bin/bash

# Define the Python script
python_script="/home/full_script_standalone.py"
model_mode="indic-generic-v2"
tgt_lang="eng_Latn"

file_paths=(

)

# Iterate through the associative array and run the Python script for each PDF
for file_path in "${file_paths[@]}"; do
    # arguments="${pdf_arguments[$pdf_path]}"
    filename=$(basename -- "$file_path")
    filename_no_extension="${filename%.*}"
    new_filename="${filename_no_extension}_${model_mode}_${tgt_lang}"

    # Run the Python script with the arguments
    command=$(python "${python_script}" "${new_filename}" "/home/" "${file_path}" "None" "None" "None" "eng+devanagari" "False" "hin_Deva" "${tgt_lang}" "${model_mode}" "PranavDalvi" "None" "jetmeteor1@protonmail.com" "False")

    echo "--------------------------------------------------------"
    echo "{$command}"

    # Add any additional processing or error handling as needed
done
