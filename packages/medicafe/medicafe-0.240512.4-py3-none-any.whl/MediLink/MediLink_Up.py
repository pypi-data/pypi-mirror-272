from datetime import datetime
import os
import re
import subprocess
import MediLink_837p_encoder
from MediLink_ConfigLoader import log
from tqdm import tqdm
from MediLink_DataMgmt import operate_winscp

"""
Handles the transmission of files to endpoints and related tasks for the MediLink script.

Functions:
- check_internet_connection(): Checks for an active internet connection.
- UPDATE THIS: transmit_files_to_endpoint(converted_files, endpoint_config, local_storage_path): Transmits files to a specified endpoint using WinSCP.
- handle_transmission_result(transmission_result): Handles the result of the file transmission process.
- submit_claims(detailed_patient_data_grouped_by_endpoint, config): Submits claims to respective endpoints based on patient data and configuration.
- confirm_transmission(detailed_patient_data_grouped_by_endpoint): Displays patient data ready for transmission and asks for confirmation.

This module provides functionality for transmitting files, confirming transmissions, and ensuring connectivity for the MediLink script.
"""

# Internet Connectivity Check
def check_internet_connection():
    """
    Checks if there is an active internet connection.
    Returns: Boolean indicating internet connectivity status.
    """
    try:
        # Run a ping command to a reliable external server (e.g., Google's DNS server)
        ping_process = subprocess.Popen(["ping", "-n", "1", "8.8.8.8"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ping_output, ping_error = ping_process.communicate()

        # Check if the ping was successful
        if "Reply from" in ping_output.decode("utf-8"):
            return True
        else:
            return False
    except Exception as e:
        print("An error occurred checking for internet connectivity:", e)
        return False

def submit_claims(detailed_patient_data_grouped_by_endpoint, config):
    # Accumulate submission results
    submission_results = {}
    
    if not detailed_patient_data_grouped_by_endpoint:
        print("No new files detected for submission.")
        return

    # Wrap the iteration with tqdm for a progress bar
    for endpoint, patients_data in tqdm(detailed_patient_data_grouped_by_endpoint.items(), desc="Progress", unit="endpoint"):
        if not patients_data:  # Skip if no patient data for the endpoint
            continue

        # Attempt submission to each endpoint
        if True: #confirm_transmission({endpoint: patients_data}): # Confirm transmission to each endpoint with detailed overview
            if check_internet_connection():
                # Process files per endpoint
                converted_files = MediLink_837p_encoder.convert_files_for_submission(patients_data, config)
                if converted_files:  # Check if files were successfully converted
                    # Transmit files per endpoint
                    try:
                        transmission_result = operate_winscp("upload", converted_files, config['MediLink_Config']['endpoints'][endpoint], config['MediLink_Config']['local_claims_path'], config)
                        success_dict = handle_transmission_result(transmission_result, config)
                        submission_results[endpoint] = success_dict
                        # TODO Future work: Availity SentFiles: Retrieve and interpret the response file from Availity SentFiles to acknowledge successful transfers.
                    except Exception as e:
                        print("Failed to transmit files to {0}. Error: {1}".format(endpoint, str(e)))
                        submission_results[endpoint] = {"success": False, "error": str(e)}
                else:
                    
                    print("No files were converted for transmission to {0}.".format(endpoint))
            else:
                print("No internet connection detected.")
                try_again = input("Do you want to try again? (Y/N): ").strip().lower()
                if try_again != 'y':
                    print("Exiting transmission process. Please try again later.")
                    return  # Exiting the function if the user decides not to retry
        else:
            print("Transmission canceled for endpoint {0}.".format(endpoint))
        
        # Continue to next endpoint regardless of the previous outcomes

    # Build and display receipt
    build_and_display_receipt(submission_results, config)
    
    print("Claim submission process completed.\n")    

def handle_transmission_result(transmission_result, config):
    """
    Analyze the outcomes of file transmissions based on WinSCP log entries.
    
    :param transmission_result: List of paths for files that were attempted to be transmitted.
    :param config: Configuration dictionary containing paths and settings.
    :return: Dictionary mapping each file path to a boolean indicating successful transmission.
    """    
    log_path = os.path.join(config['MediLink_Config']['local_storage_path'], "winscp_download.log")
    success_dict = {}

    try:
        with open(log_path, 'r') as log_file:
            log_contents = log_file.readlines()

        # Consider checking only the last few lines of the log for recent transactions
        last_lines = log_contents[-15:]

        for file_path in transmission_result:
            # Construct the success message expected in the log
            success_message = "Transfer done: '{}'".format(file_path)
            # Search for this success message in the last few lines of the log
            success = any(success_message in line for line in last_lines)
            log("Success: {0} - Transfer done for file: {1}".format(success, file_path)) # Log the outcome of the search
            success_dict[file_path] = success

    except Exception as e:
        error_msg = "Error processing the transmission log: {}".format(str(e))
        print(error_msg)
        log(error_msg)
        # If log processing fails, default to False for all files
        success_dict = {file_path: False for file_path in transmission_result}

    return success_dict

def build_and_display_receipt(submission_results, config):
    """
    Define Submission Receipt:

    A receipt of submitted claims is typically attached to each printed facesheet for recordkeeping confirming submission.

    input: accumulated success_dict
    (historical record won't work because the winscp logs will be incomplete, use clearinghouse to check historical records.)

    2.) Parse each of the 837p files from filepaths in success_dict:
    
    Note: each file will only have one receiver name and one date & time of submission. The dictionary should be organized such that the receiver name (for that file) is the key for a list of patients with patient data.

    output: print to screen a pretty ASCII human-readable organized 'receipt' by receiver name using the dictionary data, then dump to a notepad called Receipt_[date of submission].txt at config[MediLink_Config][local_storage_path] and subprocess open the file to the user to see.
    """
    # Prepare data for receipt
    # Organize submission results into a format suitable for the receipt
    log("Preparing receipt data...")
    receipt_data = prepare_receipt_data(submission_results)

    # Build the receipt
    receipt_content = build_receipt_content(receipt_data)

    # Print the receipt to the screen
    log("Printing receipt...")
    print(receipt_content)

    # Save the receipt to a text file
    save_receipt_to_file(receipt_content, config)
    
    # Probably return receipt_data since its the easier to use dictionary
    return receipt_data

def prepare_receipt_data(submission_results):
    # Perform any necessary data processing to prepare the submission results for the receipt
    # This includes extracting from a multi-patient 837p the patient names, dates of service, amounts billed.
    # Also the date & time of batch claim submission from the header segment. 
    # Get the receiver name from the 1000B receiver name segment (will be common for that file).
    # Organize the data in dictionary by endpoint (receiver name) and then patient information.
    # This function should completely fill out the dictionary with the necessary information for the receipt. 
    
    receipt_data = {}
    for endpoint, success_files in submission_results.items():
        # Assuming the success_files dictionary contains file paths and success statuses
        for file_path, success in success_files.items():
            if success:
                # Parse the 837p file for patient data
                patient_data = parse_837p_file(file_path)
                date_of_submission = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # We probably want to grab the submit from the 837p too.
                
                if endpoint not in receipt_data:
                    receipt_data[endpoint] = {
                        "date_of_submission": date_of_submission,
                        "patients": []
                    }
                receipt_data[endpoint]["patients"].extend(patient_data)
    
    return receipt_data

def parse_837p_file(file_path):
    patient_details = []
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            log("Parsing submitted 837p...")
            
            # Patient Names
            names = re.findall(r'NM1\*[^*]*\*1\*([^\*]+)\*([^\*]+)\*([^\*]+)', content)  # Updated regex to include middle name
            
            # Service Dates
            dates = re.findall(r'DTP\*472\D8\*([0-9]{8})', content)
            
            # Amounts Billed
            amounts = re.findall(r'CLM\*[^\*]*\*([0-9]+\.?[0-9]*)\*', content)
            
            # Assuming each match is aligned across the three lists
            for name, date, amount in zip(names, dates, amounts):
                patient_name = "{0} {1} {2}".format(name[1], name[0], name[2])  # First, Middle, and Last Name
                service_date = "{0}-{1}-{2}".format(date[:4], date[4:6], date[6:])  # Convert YYYYMMDD to YYYY-MM-DD
                amount_billed = float(amount)
                
                patient_details.append({
                    "name": patient_name,
                    "service_date": service_date,
                    "amount_billed": amount_billed
                })
    except Exception as e:
        print("Error reading or parsing the 837p file {0}: {1}".format(file_path, str(e)))

    return patient_details

def build_receipt_content(receipt_data):
    # Build the receipt content in a human-readable ASCII format
    # Format the receipt content to display endpoint-wise with associated patient information
    # Use ASCII art or other formatting techniques to make the receipt visually appealing
    receipt_lines = ["Submission Receipt", "="*60, ""]  # Header
    for endpoint, data in receipt_data.items():
        header = "Endpoint: {0} (Submitted: {1})".format(endpoint, data['date_of_submission'])
        receipt_lines.extend([header, "-"*len(header)])
        
        # Adding patient information
        for patient in data["patients"]:
            patient_info = "Patient: {0}, Service Date: {1}, Amount Billed: ${2}".format(patient['name'], patient['service_date'], patient['amount_billed'])
            receipt_lines.append(patient_info)
        
        receipt_lines.append("")  # Blank line for separation
    
    receipt_content = "\n".join(receipt_lines)
    return receipt_content

def save_receipt_to_file(receipt_content, config):
    # Save the receipt content to a text file named Receipt_[date_of_submission].txt
    # Use the configured local storage path to determine the file location
    # Use subprocess to open the saved file for the user to review
    file_name = "Receipt_{0}.txt".format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    file_path = os.path.join(config['MediLink_Config']['local_storage_path'], file_name)
    
    with open(file_path, 'w') as file:
        file.write(receipt_content)
    
    # Open the file automatically for the user
    subprocess.run(['open', file_path], check=True)

# Secure File Transmission
def confirm_transmission(detailed_patient_data_grouped_by_endpoint):
    """
    Displays detailed patient data ready for transmission and their endpoints, 
    asking for user confirmation before proceeding.

    :param detailed_patient_data_grouped_by_endpoint: Dictionary with endpoints as keys and 
            lists of detailed patient data as values.
    :param config: Configuration settings loaded from a JSON file.
    """ 
    print("\nReview of patient data ready for transmission:")
    for endpoint, patient_data_list in detailed_patient_data_grouped_by_endpoint.items():
        print("\nEndpoint: {0}".format(endpoint))
        for patient_data in patient_data_list:
            patient_info = "({1}) {0}".format(patient_data['patient_name'], patient_data['patient_id'])
            print("- {:<35} | {:<5}, ${:<6}, Primary: {}".format(
                patient_info, patient_data['surgery_date'][:5], patient_data['amount'], patient_data['primary_insurance']))
    
    confirmation = input("\nProceed with transmission to all endpoints? (Y/N): ").strip().lower()
    return confirmation == 'y'

# Entry point if this script is run directly. Probably needs to be handled better.
if __name__ == "__main__":
    print("Please run MediLink directly.")