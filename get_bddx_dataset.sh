
export WORKSPACE=$(pwd)

# Define the file path and URL
FILE="${WORKSPACE}/video_process/video_process.tar.gz"
URL="https://drive.usercontent.google.com/download?id=14a3QTkWRelAZs-kW_2U5tjYcAm2l8VbF&export=download&authuser=0&confirm=t&uuid=42f173e7-d4f3-4ee4-a88c-e1bdfb531b69&at=APZUnTUOSlPhljxTnnWF6E0Rn1bd%3A1720179449276"

# Check if the file exists
if [ ! -f "$FILE" ]; then
    echo "File not found. Downloading..."
    wget --no-check-certificate "$URL" -O "$FILE"
else
    echo "File already exists. Skipping download."
fi

# Check if BDDX_Processed and BDDX_Test folder exist
BDDX_Processed="${WORKSPACE}/video_process/BDDX_Processed"
BDDX_Test="${WORKSPACE}/video_process/BDDX_Test"
if [ -d "$BDDX_Processed" ]; then 
    echo "File already exists. Skipping extract."
else
    echo "extract video_process.tar.gz"
    tar -xf "FILE" -C ${WORKSPACE}/video_process/
    mv ${WORKSPACE}/video_process/video_process/* ${WORKSPACE}/video_process/ 
fi


export PATH=${WORKSPACE}/rag_env/bin:$PATH
python ${WORKSPACE}/video_process/create_bddx_json.py