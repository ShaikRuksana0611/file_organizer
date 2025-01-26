import os
import shutil
import logging

# Set up logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/file_logs.txt", 
    level=logging.INFO, 
    format="%(asctime)s - %(message)s"
)

# File type mappings
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar"],
    "Others": []
}


def organize_files(directory):
    try:
        for folder in FILE_TYPES.keys():
            folder_path = os.path.join(directory, folder)
            os.makedirs(folder_path, exist_ok=True)

        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                # Determine the file's category
                file_ext = os.path.splitext(file)[1].lower()
                moved = False
                for folder, extensions in FILE_TYPES.items():
                    if file_ext in extensions:
                        shutil.move(file_path, os.path.join(directory, folder, file))
                        logging.info(f"Moved: {file} -> {folder}/")
                        moved = True
                        break

                if not moved:
                    shutil.move(file_path, os.path.join(directory, "Others", file))
                    logging.info(f"Moved: {file} -> Others/")

        print("Files have been successfully organized.")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print("An error occurred. Check the logs for details.")
