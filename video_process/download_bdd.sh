
# Remember to export WORKSPACE before using it.
VIDEO_FOLDER=$(pwd)/video_process

# Define the file path and URL
FILE="${VIDEO_FOLDER}/video_process.tar.gz"
URL="https://drive.usercontent.google.com/download?id=14a3QTkWRelAZs-kW_2U5tjYcAm2l8VbF&export=download&authuser=0&confirm=t&uuid=42f173e7-d4f3-4ee4-a88c-e1bdfb531b69&at=APZUnTUOSlPhljxTnnWF6E0Rn1bd%3A1720179449276"

# Check if the file exists
if [ ! -f "$FILE" ]; then
    echo "File not found. Downloading..."
    wget --no-check-certificate "$URL" -O "$FILE"
else
    echo "File already exists. Skipping download."
fi

# Check if BDDX_Processed and BDDX_Test folder exist
BDDX_Processed="${VIDEO_FOLDER}/BDDX_Processed"
BDDX_Test="${VIDEO_FOLDER}/BDDX_Test"
if [ -d "$BDDX_Processed" ]; then 
    echo "File already exists. Skipping extract."
else
    echo "extract video_process.tar.gz"
    tar -xf "FILE" -C ${VIDEO_FOLDER}/
fi


export PATH=${VIDEO_FOLDER}/rag_env/bin:$PATH
python ${VIDEO_FOLDER}/create_bddx_json.py