from pathlib import Path
import pydicom
from pynetdicom import AE

# Details of the DICOM Listener (SCP) you are testing
SCP_IP = "54.189.242.61"  # IP address of the listener
SCP_PORT = 104  # Port the listener is running on
SCP_AET = "SIMONMED_AE"  # AE Title of the listener
SCU_AET = "PYNET_SCU"  # AE Title for your client


def process_file_pathlib(file_path) -> bool:
    """Placeholder function to process the file."""
    # file_path is a Path object here
    # print(f"Processing: {file_path}")
    # Add your actual file processing logic here
    # --- Configuration ---

    # The DICOM file you want to send
    DICOM_FILE_PATH = file_path

    # --- 1. Load the DICOM file ---
    try:
        ds = pydicom.dcmread(DICOM_FILE_PATH)
        # print(f"Successfully loaded file: {DICOM_FILE_PATH}")
    except FileNotFoundError:
        print(
            f"Error: DICOM file not found at {DICOM_FILE_PATH}. Please provide a valid file."
        )
        return False

    # --- 2. Create the Application Entity (AE) ---
    ae = AE(ae_title=SCU_AET)

    # Add a presentation context for the specific SOP Class of the file.
    # The Transfer Syntax is automatically derived from the dataset's encoding.
    ae.add_requested_context(ds.SOPClassUID)

    # SUPPORTED_SOP_CLASSES = [
    #     '1.2.840.10008.5.1.4.1.1.13.1.3',  # Breast Tomosynthesis Image Storage
    #     '1.2.840.10008.5.1.4.1.1.2',       # CT Image Storage
    #     '1.2.840.10008.5.1.4.1.1.4',       # MR Image Storage
    #     '1.2.840.10008.5.1.4.1.1.1',       # Computed Radiography Image Storage
    #     '1.2.840.10008.5.1.4.1.1.1.1',     # Digital X-Ray Image Storage - For Presentation
    #     '1.2.840.10008.5.1.4.1.1.1.1.1',   # Digital X-Ray Image Storage - For Processing
    #     '1.2.840.10008.5.1.4.1.1.6.1',     # Ultrasound Image Storage
    #     '1.2.840.10008.5.1.4.1.1.12.1',    # X-Ray Angiographic Image Storage
    #     '1.2.840.10008.5.1.4.1.1.13.1.1',  # X-Ray 3D Angiographic Image Storage
    #     '1.2.840.10008.5.1.4.1.1.13.1.2',  # X-Ray 3D Craniofacial Image Storage
    #     '1.2.840.10008.5.1.4.1.1.7',       # Secondary Capture Image Storage
    #     '1.2.840.10008.5.1.4.1.1.88.67',   # VL Photographic Image Storage
    #     '1.2.840.10008.5.1.4.1.1.1.2',     # Digital X-Ray Image Storage - For Presentation
    #     '1.2.840.10008.5.1.4.1.1.11.1',    # RT Image Storage
    #     '1.2.840.10008.5.1.4.1.1.88.50',   # VL Endoscopic Image Storage
    # ]

    # TRANSFERRED_SYNTAXES = [
    #     '1.2.840.10008.1.2.4.70', # JPEG Lossless, Non-Hierarchical, First-Order Prediction (PRIORITY)
    #     '1.2.840.10008.1.2.4.57', # JPEG Lossless, Non-Hierarchical (Process 14)
    #     '1.2.840.10008.1.2.4.50', # JPEG Baseline (Process 1)
    #     '1.2.840.10008.1.2.4.51', # JPEG Extended (Process 2 & 4)
    #     '1.2.840.10008.1.2.4.90', # JPEG 2000 Image Compression (Lossless Only)
    #     '1.2.840.10008.1.2.4.91', # JPEG 2000 Image Compression
    #     '1.2.840.10008.1.2.5',    # RLE Lossless
    #     '1.2.840.10008.1.2.1',    # Explicit VR Little Endian
    #     '1.2.840.10008.1.2',      # Implicit VR Little Endian
    #     '1.2.840.10008.1.2.2',    # Explicit VR Big Endian
    # ]
    # --- 3. Start the Association ---
    # print(f"Attempting to associate with {SCP_AET} at {SCP_IP}:{SCP_PORT}...")
    assoc = ae.associate(SCP_IP, SCP_PORT, ae_title=SCP_AET)

    if assoc.is_established:
        # print("Association established successfully.")

        # --- 4. Send the C-STORE Request ---
        # The `send_c_store` method handles building the DIMSE message.
        try:
            status, dataset = assoc.send_c_store(ds)

            # --- 5. Check the Response Status ---
            if status:
                # Status code (0x0000) indicates success
                if status.Status == 0x0000:
                    print("C-STORE successful! Image accepted by the listener.")
                else:
                    print(f"C-STORE failed. Status code: {status.Status}")
                    # print(f"Status description: {status.ErrorComment}") # Uncomment for more detail
            else:
                print("C-STORE failed: No response received.")
        except Exception as e:
            print(f"An error occurred during C-STORE operation: {e}")
            assoc.release()
            return False

        # --- 6. Release the Association ---
        assoc.release()
        # print("Association released.")

    else:
        print("Association failed: Could not connect to the listener.")

    return True


def recursive_file_loop_pathlib(root_dir, extension):
    """
    Recursively loops through a directory and processes files
    with the given extension using pathlib.
    """
    # Create a Path object for the root directory
    root_path = Path(root_dir)
    file_count = 0
    success_count = 0
    # Convert extension to the pattern needed for glob, e.g., '*.txt'
    if extension.startswith("."):
        pattern = "*" + extension
    else:
        pattern = "*." + extension

    print(f"Starting recursive search in: {root_path} for files matching: {pattern}\n")

    # .rglob() is the recursive glob function (glob means pattern matching)
    # It returns a generator yielding all matching files/directories recursively.
    for file_path in root_path.rglob(pattern):
        # file_path is a Path object
        if file_path.is_file():  # Ensure it's a file, not a directory
            file_count += 1
            print(f"File {file_count} (success {success_count}): {file_path}")
            if process_file_pathlib(file_path):
                success_count += 1
                print(f"Successfully processed file {file_count}: {file_path}\n")


# --- Example Usage ---
# Replace 'your_directory_path' with the starting directory
# Replace 'csv' with your desired file extension
recursive_file_loop_pathlib("DICOM", "dcm")
