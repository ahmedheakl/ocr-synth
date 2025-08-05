#!/bin/bash

# pipeline for the creation of the dataset

# MinIO configuration alias
MINIO_ALIAS="myS3"  # Change this to your MinIO alias
DESTINATION_DIR="/data/dataset_syn_rik"  # Local path where you want to copy the files

# Array of directories to look into on MinIO
BUCKET_NAME="foc-deepsearch-arxiv-data" 
SOURCE_DIR='src'
echo "Listing folders inside MinIO directory: $MINIO_ALIAS/$BUCKET_NAME/$SOURCE_DIR"
#save the directories we are interested in an array
mapfile -t folder_list < <(mc ls "$MINIO_ALIAS/$BUCKET_NAME/$SOURCE_DIR" | awk '{print $NF}' | grep '/$')

# for every folder in the s3 database, we check if there is still space on the machine
# Extract available space from `df -m` (which shows MB values)
get_free_space() {
    df -m / | awk 'NR==2 {print $4}'
}

max_number=0
echo " Starting the pipeline ..."
for folder in "${folder_list[@]}"; do
    echo "Processing folder: $folder"
    # 1. load a dataset for a certain month
    if [ "$(get_free_space)" -le 20000 ]; then
        echo "no space left"
        break
    fi
    mc cp --recursive "$MINIO_ALIAS/$BUCKET_NAME/$SOURCE_DIR/$folder" "$DESTINATION_DIR"
    if [ $? -eq 0 ]; then
        echo "Successfully copied files from $MINIO_DIR"
    else
        echo "Error copying files from $MINIO_DIR"
    fi

    #2. filter all the tex file for which the licence is not correct and empty the space
    source env1/bin/activate
    python3 extract_metadata_arxiv.py

    #3. convert the filtered tex file into HTML files + eliminate all the logs file + eliminate the old directory
    python3 latex2html.py
    TEMP_FOLDER1='valid_ouput'
    rm -f "$DESTINATION_DIR"/*.log
    rsync -a --delete empty/ "$DESTINATION_DIR"/"$TEMP_FOLDER1"/

    #4. convert the HTML files into docling
    python3 arxiv_html_to_docling.py "$max_number"
    max_number=$(find "$SEARCH_DIR" -type d -name "doc*" 2>/dev/null | grep -oE 'doc[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1)
    TEMP_FOLDER2='result_folder'
    rsync -a --delete empty/ "$DESTINATION_DIR"/"$TEMP_FOLDER2"/

    #5. Run the syn data generation
    deactivate
    cd synthetic_data_generator
    source env/bin/activate
    cd ..
    python3 "$DESTINATION_DIR"/synthetic_data_generator/synthetic_data_generator_parallel.py
    echo "generated synData"

    #6. save everything in the HF format with and store old data + empty the processing directory
    python3 "$DESTINATION_DIR"/synthetic_data_generator/save_HF_format.py
    echo "expanded HF dataset"
    TEMP_DATASET='synthetic_data_generator/synthetic_data_generation/dataset/demo/doclingdocs'
    rsync -a --delete empty/ "$DESTINATION_DIR"/"$TEMP_DATASET"/
    deactivate

done

echo "pipeline completed"