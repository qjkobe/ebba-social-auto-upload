import os
import shutil
import time
from pathlib import Path

def process_files(source_dir, target_dir, operation='copy'):

    """
    Process video files from the source directory and move or copy them to the target directory.

    :param source_dir: Root directory containing the original files.
    :param target_dir: Destination directory for the processed files.
    :param operation: Specify 'copy' or 'move' to determine the file operation.
    """
    # Ensure the target directory exists
    target_dir = Path(target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    # Iterate through all subdirectories and files
    for root, dirs, files in os.walk(source_dir):
        if(len(files) > 0):
            print(files)

        root_path = Path(root)
        if len(root_path.parts) < 3 or len(files) == 0:
            continue

        # Extract metadata from the path
        date_dir = root_path.parts[-3]  # First-level directory: Date
        session_dir = root_path.parts[-2]  # Second-level directory: Session or location
        team_dir = root_path.parts[-1]  # Third-level directory: Black or White team

        for file in files:
            if file.startswith("highlight_") and file.endswith((".mp4", ".mov")):
                # Prepare new file name with date and timestamp suffix
                timestamp = int(time.time())
                original_name = Path(file).stem
                extension = Path(file).suffix
                new_name = f"{date_dir}_{timestamp}_{original_name}{extension}"
                new_txt_name = f"{date_dir}_{timestamp}_{original_name}.txt"

                # Prepare target paths for video and text file
                target_file = target_dir / new_name
                txt_file = target_dir / new_txt_name

                # Generate text content
                player_name = original_name.split("_")[1] if "_" in original_name else "未知"
                text_content = f"{date_dir} {session_dir} {team_dir}\n#早鸟篮球 #{player_name} #高光时刻"

                # Perform the operation (copy or move)
                source_file = root_path / file
                if operation == 'copy':
                    shutil.copy2(source_file, target_file)
                elif operation == 'move':
                    shutil.move(source_file, target_file)
                else:
                    print(f"Unsupported operation: {operation}")
                    return

                # Write the text file
                with open(txt_file, 'w', encoding='utf-8') as txt:
                    txt.write(text_content)

                print(f"Processed: {source_file} -> {target_file}")
                print(f"Text file created: {txt_file}")

if __name__ == "__main__":

    # Configure source and target directories
    # source_directory = input("Enter the source directory: ").strip()
    source_directory = "./"
    # target_directory = input("Enter the target directory: ").strip()
    target_directory = "../videos"

    # Specify the operation: copy or move
    # operation_type = input("Enter the operation (copy/move): ").strip().lower()
    operation_type = "copy"
    if operation_type not in ['copy', 'move']:
        print("Invalid operation. Please choose 'copy' or 'move'.")
    else:
        process_files(source_directory, target_directory, operation_type)


