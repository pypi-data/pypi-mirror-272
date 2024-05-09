"""
MediBot_UI.py brought back in here because of script_paused
"""

from sys import exit
import ctypes
from ctypes import wintypes
import time
import re
from MediBot_Preprocessor import config

"""
User Interaction Refinements
- [ ] Refine the menu options for clearer user guidance during script pauses and errors.
- [ ] Add functionality for user to easily repeat or skip specific entries without script restart.
    Develop more intuitive skip and retry mechanisms that are responsive to user input during data entry sessions.

"""
# Function to check if a specific key is pressed
VK_END = int(config.get('VK_END', ""), 16) # Try F12 (7B). Virtual key code for 'End' (23)
VK_PAUSE = int(config.get('VK_PAUSE', ""), 16) # Try F11 (7A). Virtual-key code for 'Home' (24)

MAPAT_MED_PATH = '' # Initialize global constant for MAPAT path
MEDISOFT_SHORTCUT = '' # Initialize global constant for LNK path

def is_key_pressed(key_code):
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    user32.GetAsyncKeyState.restype = wintypes.SHORT
    user32.GetAsyncKeyState.argtypes = [wintypes.INT]
    return user32.GetAsyncKeyState(key_code) & 0x8000 != 0

def manage_script_pause(csv_data, error_message, reverse_mapping):
    global script_paused
    #print("Debug - Entered manage_script_pause with pause status: {}".format(script_paused))
    user_action = 0 # initialize as 'continue'
    
    if not script_paused and is_key_pressed(VK_PAUSE):
        script_paused = True
        print("Script paused. Opening menu...")
        interaction_mode = 'normal'  # Assuming normal interaction mode for script pause
        user_action = user_interaction(csv_data, interaction_mode, error_message, reverse_mapping)
    
    while script_paused:
        if is_key_pressed(VK_END):
            script_paused = False
            print("Continuing...")
        elif is_key_pressed(VK_PAUSE):
            user_action = user_interaction(csv_data, 'normal', error_message, reverse_mapping)
        time.sleep(0.1)
    
    return user_action

# Menu Display & User Interaction
def display_patient_selection_menu(csv_data, reverse_mapping, proceed_as_medicare):
    selected_patient_ids = []
    selected_indices = []

    def display_menu_header(title):
        print("\n" + "-" * 60)
        print(title)
        print("-" * 60)

    def display_patient_list(csv_data, reverse_mapping, medicare_filter=False, exclude_medicare=False):
        medicare_policy_pattern = r"^[a-zA-Z0-9]{11}$"  # Regex pattern for 11 alpha-numeric characters
        primary_policy_number_header = reverse_mapping.get('Primary Policy Number', 'Primary Policy Number')
        primary_insurance_header = reverse_mapping.get('Primary Insurance', 'Primary Insurance')  # Adjust field name as needed
        
        displayed_indices = []
        displayed_patient_ids = []

        for index, row in enumerate(csv_data):
            policy_number = row.get(primary_policy_number_header, "")
            primary_insurance = row.get(primary_insurance_header, "").upper()
            
            if medicare_filter and (not re.match(medicare_policy_pattern, policy_number) or "MEDICARE" not in primary_insurance):
                continue
            if exclude_medicare and re.match(medicare_policy_pattern, policy_number) and "MEDICARE" in primary_insurance:
                continue

            patient_id_header = reverse_mapping['Patient ID #2']
            patient_name_header = reverse_mapping['Patient Name']
            patient_id = row.get(patient_id_header, "N/A")
            patient_name = row.get(patient_name_header, "Unknown")
            surgery_date = row.get('Surgery Date', "Unknown Date")  # Access 'Surgery Date' as string directly from the row
            
            print("{0:02d}: {3:.5s} (ID: {2}) {1} ".format(index+1, patient_name, patient_id, surgery_date))

            displayed_indices.append(index)
            displayed_patient_ids.append(patient_id)

        return displayed_indices, displayed_patient_ids

    if proceed_as_medicare:
        display_menu_header("MEDICARE Patient Selection for Today's Data Entry")
        selected_indices, selected_patient_ids = display_patient_list(csv_data, reverse_mapping, medicare_filter=True)
    else:
        display_menu_header("PRIVATE Patient Selection for Today's Data Entry")
        selected_indices, selected_patient_ids = display_patient_list(csv_data, reverse_mapping, exclude_medicare=True)

    print("-" * 60)
    proceed = input("\nDo you want to proceed with the selected patients? (yes/no): ").lower().strip() in ['yes', 'y']

    if not proceed:
        display_menu_header("Patient Selection for Today's Data Entry")
        selected_indices, selected_patient_ids = display_patient_list(csv_data, reverse_mapping)
        print("-" * 60)
        
        while True:
            selection = input("\nEnter the number(s) of the patients you wish to proceed with \n(e.g., 1,3,5): ").strip()
            
            if not selection:
                print("Invalid entry. Please provide at least one number.")
                continue
            
            selection = selection.replace('.', ',')  # Replace '.' with ',' in the user input just in case
            selected_indices = [int(x.strip()) - 1 for x in selection.split(',') if x.strip().isdigit()]  
            
            if not selected_indices:
                print("Invalid entry. Please provide at least one integer.")
                continue
            
            proceed = True
            break

    patient_id_header = reverse_mapping['Patient ID #2']
    selected_patient_ids = [csv_data[i][patient_id_header] for i in selected_indices if i < len(csv_data)]

    return proceed, selected_patient_ids, selected_indices

def display_menu_header(title):
    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)

def handle_user_interaction(interaction_mode, error_message):
    while True:
        # If interaction_mode is neither 'triage' nor 'error', then it's normal mode.
        title = "Error Occurred" if interaction_mode == 'error' else "Data Entry Options"
        display_menu_header(title)

        if interaction_mode == 'error':
            print("\nERROR: ", error_message)

        # Need to tell the user which patient we're talking about because it won't be obvious anymore.
        # Also, this ERROR might be called from a location where the menu below isn't relevant like selecting patients 
        # -- need a better way to handle that.
        print("1: Retry last entry")
        print("2: Skip to next patient and continue")
        print("3: Go back two patients and redo")
        print("4: Exit script")
        print("-" * 60)
        choice = input("Enter your choice (1/2/3/4): ").strip()
        
        if choice == '1':
            print("Selected: 'Retry last entry'. Please press 'F12' to continue.")
            return -1
        elif choice == '2':
            print("Selected: 'Skip to next patient and continue'. Please press 'F12' to continue.")
            return 1
        elif choice == '3':
            print("Selected: 'Go back two patients and redo'. Please press 'F12' to continue.")
            # Returning a specific value to indicate the action of going back two patients
            # but we might run into a problem if we stop mid-run on the first row?
            return -2
        elif choice == '4':
            print("Exiting the script.")
            exit()
        else:
            print("Invalid choice. Please enter a valid number.")

def user_interaction(csv_data, interaction_mode, error_message, reverse_mapping):
    # Consider logging the actions taken during user interaction for audit purposes.
    global MAPAT_MED_PATH, MEDISOFT_SHORTCUT # Initialize global constants
    selected_patient_ids = []
    selected_indices = []

    if interaction_mode == 'triage':
    
        display_menu_header("            =(^.^)= Welcome to MediBot! =(^.^)=")
        
        while True:
            response = input("\nAm I processing Medicare patients? (yes/no): ").lower().strip()
            if response:  # Check if the response is not empty
                if response in ['yes', 'y']:
                    proceed_as_medicare = True
                    break
                elif response in ['no', 'n']:
                    proceed_as_medicare = False
                    break
                else:
                    print("Invalid entry. Please enter 'yes' or 'no'.")
            else:
                print("A response is required. Please try again.")

        MAPAT_MED_PATH = config.get('MEDICARE_MAPAT_MED_PATH', "") if proceed_as_medicare else config.get('MAPAT_MED_PATH', "")
        MEDISOFT_SHORTCUT = config.get('MEDICARE_SHORTCUT', "") if proceed_as_medicare else config.get('PRIVATE_SHORTCUT', "")
        
        fixed_values = config.get('fixed_values', {})  # Get fixed values from config json 
        if proceed_as_medicare:
            medicare_added_fixed_values = config.get('medicare_added_fixed_values', {})
            fixed_values.update(medicare_added_fixed_values) # Add any medicare-specific fixed values from config
        
        proceed, selected_patient_ids, selected_indices = display_patient_selection_menu(csv_data, reverse_mapping, proceed_as_medicare)
        return proceed, selected_patient_ids, selected_indices, fixed_values
    
    return handle_user_interaction(interaction_mode, error_message)


"""
MediBot starts here.
"""

import subprocess
import os
import tempfile
import traceback
import re  #for addresses
from collections import OrderedDict
#import MediBot_UI
import MediBot_dataformat_library
import MediBot_Preprocessor
from MediBot_Preprocessor import initialize, AHK_EXECUTABLE, CSV_FILE_PATH, field_mapping
import MediBot_Preprocessor_lib

# Add parent directory of the project to the Python path
import sys
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_dir)

from MediLink import MediLink_ConfigLoader

"""
# Development Task List for MediBot

Error Handling Improvements
- [ ] Develop a centralized error handling and logging mechanism for improved troubleshooting.
- [ ] Implement validation checks during patient data entry to prevent submission of incomplete or incorrect records.

Insurance Mode Adjustments
- [ ] Integrate a comprehensive list of insurance company codes for automatic selection.
- [ ] Automate insurance-specific data entry adjustments, such as character replacements specific to Medicare.

Diagnosis Entry
- [ ] Automate data extraction from Surgery Schedule to import to CSV a column indicating diagnosis code per px.

Script Efficiency and Reliability
- [ ] Ensure robust handling of Medisoft's field navigation quirks, particularly for fields that are skipped or require special access.

Documentation and Support
- [ ] Create detailed documentation for setup, configuration, and usage of the script.
- [ ] Establish a support channel for users to report issues or request features.

Future Directions
- [ ] Consider developing a graphical user interface (GUI) for non-technical users for easier script management and execution.

Medisoft Field Navigation: 
    Investigate and optimize navigation for fields that Medisoft skips or requires backward navigation to access.

Insurance Mode Features: 
    Evaluate the feasibility and implement the use of the F6 search for insurance address verification, enhancing user verification processes. 

Error Handling and Logging: 
    Implement a check for AHK script execution status, providing feedback or troubleshooting steps if the script encounters issues.
"""

def identify_field(header, field_mapping):
    for medisoft_field, patterns in field_mapping.items():
        for pattern in patterns:
            if re.search(pattern, header, re.IGNORECASE):
                return medisoft_field
    return None

    # Add this print to a function that is calling identify_field
    #print("Warning: No matching field found for CSV header '{}'".format(header))

# Function to execute an AutoHotkey script
def run_ahk_script(script_content):
    temp_script_name = None
    try:
        # Create a temporary AHK script file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ahk') as temp_script:
            temp_script_name = temp_script.name
            temp_script.write(script_content.encode('utf-8'))
            temp_script.flush()
        # Attempt to run the AHK script
        subprocess.check_call([AHK_EXECUTABLE, temp_script_name])
    except subprocess.CalledProcessError as e:
        # This exception will catch any non-zero exit status from the AHK script
        print("AHK script failed with exit status:", e.returncode)
        print("Output from AHK script:", e.output)
    except Exception as e:
        # This catches any other exceptions that may occur
        print("An unexpected error occurred while running the AHK script:", e)
        traceback.print_exc()  # Print the stack trace of the exception
    finally:
        # Delete the temporary script file
        if temp_script_name:
            try:
                os.unlink(temp_script_name)
            except OSError as e:
                print("Error deleting temporary script file:", e)

# Global variable to store the last processed entry
last_processed_entry = None
# Global variable to store temporarily parsed address components
parsed_address_components = {}

def process_field(medisoft_field, csv_row, parsed_address_components, reverse_mapping, csv_data, fixed_values):
    global last_processed_entry
    
    try:
        value = ''
        if medisoft_field in parsed_address_components:
            value = parsed_address_components.get(medisoft_field, '')
        elif medisoft_field in fixed_values:
            value = fixed_values[medisoft_field][0]  # Use the fixed value
        elif medisoft_field in reverse_mapping:
            csv_header = reverse_mapping[medisoft_field]
            value = csv_row.get(csv_header, '')

        formatted_value = MediBot_dataformat_library.format_data(medisoft_field, value, csv_data, reverse_mapping, parsed_address_components) if value else 'Send, {Enter}'
        run_ahk_script(formatted_value)

        last_processed_entry = (medisoft_field, value)
        return 'continue', last_processed_entry
    except Exception as e:
        return handle_error(e, medisoft_field, last_processed_entry, csv_data)

def handle_error(error, medisoft_field, last_processed_entry, csv_data):
    print("An error occurred while processing {0}: {1}".format(medisoft_field, error))
    # Assuming the interaction mode is 'error' in this case
    interaction_mode = 'error'
    response = user_interaction(csv_data, interaction_mode, error, reverse_mapping)
    return response, last_processed_entry

# iterating through each field defined in the field_mapping.
def iterate_fields(csv_row, field_mapping, parsed_address_components, reverse_mapping, csv_data, fixed_values):
    global last_processed_entry
    # Check for user action at the start of each field processing
    for medisoft_field in field_mapping.keys():
        action = manage_script_pause(csv_data,'',reverse_mapping) # per-field pause availability. Necessary to provide frequent opportunities for the user to pause the script.
        if action != 0:  # If action is either 'Retry' (-1) or 'Skip' (1)
            return action  # Break out and pass the action up
        
        # Process each field in the row
        _, last_processed_entry = process_field(medisoft_field, csv_row, parsed_address_components, reverse_mapping, csv_data, fixed_values)
        
    return 0 # Default action to continue

def data_entry_loop(csv_data, field_mapping, reverse_mapping, fixed_values):
    global last_processed_entry, parsed_address_components, script_paused
    script_paused = False
    error_message = ''  # Initialize error_message once
    current_row_index = 0

    while current_row_index < len(csv_data):
        row = csv_data[current_row_index]
        
        # Handle script pause at the start of each row (patient record). 
        manage_script_pause(csv_data, error_message, reverse_mapping)
        error_message = ''  # Clear error message for the next iteration
        
        if script_paused:
            continue  # Skip processing this row if the script is paused

        # I feel like this is overwriting what would have already been idenfitied in the mapping. 
        # This probably needs to be initialized differently.
        # parsed_address_components = {'City': '', 'State': '', 'Zip Code': ''}
        parsed_address_components = {}

        # Process each field in the row
        action = iterate_fields(row, field_mapping, parsed_address_components, reverse_mapping, csv_data, fixed_values)
        # TODO (Low) add a feature here where if you accidentally started overwriting a patient that you could go back 2 patients.
        # Need to tell the user which patient we're talking about because it won't be obvious anymore.
        if action == -1:  # Retry
            continue  # Remain on the current row. 
        elif action == 1:  # Skip
            if current_row_index == len(csv_data) - 1:  # If it's the last row
                print("Reached the end of the patient list. Looping back to the beginning.")
                current_row_index = 0  # Reset to the first row
            else:
                current_row_index += 1 # Move to the next row
            continue
        elif action == -2:  # Go back two patients and redo
            current_row_index = max(0, current_row_index - 2)  # Go back two rows, but not below 0
            continue

        # Code to handle the end of a patient record
        # print("\nA patient record was completed.")
        script_paused = True
        # Handle script pause at the end of each row (patient record).
        current_row_index += 1  # Move to the next row by default

def open_medisoft(shortcut_path):
    try:
        os.startfile(shortcut_path)
        print("Medisoft is being opened...\n")
    except subprocess.CalledProcessError as e:
        print("Failed to open Medisoft:", e)
        print("Please manually open Medisoft.")
    except Exception as e:
        print("An unexpected error occurred:", e)
        print("Please manually open Medisoft.")
    finally:
        print("Press 'F12' to begin data entry.")

# Placeholder for any cleanup
def cleanup():
    print("\n**** Medibot Finished! ****\n")
    # THis might need to delete the staging stuff that gets set up by mostly MediLink but maybe other stuff too.
    pass 

class ExecutionState:
    def __init__(self, config_path, crosswalk_path) -> None:
        try:
            config, crosswalk = MediLink_ConfigLoader.load_configuration(config_path, crosswalk_path)
            self.verify_config_type(config)
            self.crosswalk = crosswalk
            self.config = config
            MediLink_ConfigLoader.log("Config loaded successfully...")
            
            MediBot_Preprocessor.crosswalk_update(config, crosswalk)
            MediLink_ConfigLoader.log("Crosswalk update complete...")
            
            initialize(config)
            MediLink_ConfigLoader.log("Constants initialized...")
            
        except Exception as e:
            print("Failed to load or update configuration: {}".format(e))
            raise # Re-throwing the exception or using a more sophisticated error handling mechanism might be needed
            # Handle the exception somehow (e.g., retry, halt, log)??
        
    def verify_config_type(self, config):
        if not isinstance(config, (dict, OrderedDict)):
            raise TypeError("Error: Configuration must be a dictionary or an OrderedDict. Check unpacking.")

# Main script execution wrapped in try-except for error handling
if __name__ == "__main__":
    e_state = None
    try:
        # Default paths
        default_config_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'config.json')
        default_crosswalk_path = os.path.join(os.path.dirname(__file__), '..', 'json', 'crosswalk.json')

        # Check if command-line arguments are provided
        if len(sys.argv) > 1:
            # If arguments are provided, use them
            config_path = sys.argv[1]
            crosswalk_path = sys.argv[2] if len(sys.argv) > 2 else default_crosswalk_path
        else:
            # If no arguments are provided, use default paths
            config_path = default_config_path
            crosswalk_path = default_crosswalk_path
        
        e_state = ExecutionState(config_path, crosswalk_path)
        
        #print("Loading CSV Data...")
        csv_data = MediBot_Preprocessor_lib.load_csv_data(CSV_FILE_PATH)
        
        #print("Pre-processing CSV Data...")
        MediBot_Preprocessor.preprocess_csv_data(csv_data, e_state.crosswalk)  # Pre-process CSV data to add combined fields & crosswalk values.
        headers = csv_data[0].keys() # Including Patient Name and Patient Address
        
        #print("Performing Intake Scan...")
        # identified_fields is an OrderedDict
        identified_fields = MediBot_Preprocessor.intake_scan(headers, field_mapping)
        
        # Reverse the identified_fields mapping for lookup
        reverse_mapping = {v: k for k, v in identified_fields.items()}

        # CSV Patient Triage
        interaction_mode = 'triage'  # Start in triage mode
        error_message = ""  # This will be filled if an error has occurred
        #print("Debug - Identified fields mapping (main): {}".format(identified_fields)) # Debug Line
        
        proceed, selected_patient_ids, selected_indices, fixed_values = user_interaction(csv_data, interaction_mode, error_message, reverse_mapping)

        if proceed:
            # Filter csv_data for selected patients from Triage mode.
            csv_data = [row for index, row in enumerate(csv_data) if index in selected_indices]
            existing_patients, patients_to_process = MediBot_Preprocessor.check_existing_patients(selected_patient_ids, MAPAT_MED_PATH)
            
            if existing_patients:
                print("\nNOTE: The following patient(s) already EXIST in the system and \n      will be excluded from processing:")
                for patient_id, patient_name in existing_patients:
                    print("(ID: {0}) {1}".format(patient_id, patient_name))
                # Update csv_data to exclude existing patients
                csv_data = [row for row in csv_data if row[reverse_mapping['Patient ID #2']] in patients_to_process]
            else:
                print("\nSelected patient(s) are NEW patients and will be processed.")

            if len(patients_to_process) == 0:
                proceed = input("\nAll patients have been processed. Continue anyway?: ").lower().strip() in ['yes', 'y']
            else:
                proceed = input("\nDo you want to proceed with the {} remaining patient(s)? (yes/no): ".format(len(patients_to_process))).lower().strip() in ['yes', 'y']

            if proceed:
            
            #    Would be nice to have some kind of self-test here.
            #    print("\nDebug - Starting AHK script. Reload AHK if failed...")
            #    try:
            #        subprocess.call([AHK_EXECUTABLE, r"G:\My Drive\CocoWave\XP typing bot\notepad_test.ahk"])
            #        run_ahk_script('MsgBox, Test AHK Script Execution')
            #    except subprocess.CalledProcessError as e:
            #        print("Error running AHK script. Please reload AHK and try again. Error: {}".format(e))
            #        exit(1)
            #    except Exception as e:
            #        print("An unexpected error occurred while running the AHK script: {}".format(e))
            #        exit(1)

                print("\nRemember, when in Medisoft:")
                print("  Press 'F8'  to create a New Patient.")
                print("  Press 'F12' to begin data entry.")
                print("  Press 'F11' at any time to Pause.")
                input("\n*** Press [Enter] when ready to begin! ***\n")
                open_medisoft(MEDISOFT_SHORTCUT)
                global script_paused
                script_paused = True
                _ = manage_script_pause(csv_data, error_message, reverse_mapping)
                data_entry_loop(csv_data, field_mapping, reverse_mapping, fixed_values)
                cleanup()                
            else:
                print("Data entry canceled by user. Exiting MediBot.")
    except Exception as e:
        if e_state:
            interaction_mode = 'error'  # Switch to error mode
            error_message = str(e)  # Capture the error message
        print("An error occurred while running MediBot: {0}".format(e))
        # Handle the error by calling user interaction with the error information
        # Ensure that identified_fields is defined before using it in user interaction
        if 'identified_fields' in locals():
            _ = user_interaction(csv_data, interaction_mode, error_message, reverse_mapping)
        else:
            print("Please ensure CSV headers match expected field names in config file, then re-run Medibot.")