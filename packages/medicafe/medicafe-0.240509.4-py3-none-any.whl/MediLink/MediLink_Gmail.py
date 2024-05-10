"""
TODO All of this needs to get re-written to match the current implementation and the lessons learned.

NOTE: Also download the surgery schedule. So sometimes it doesn't need the OTP.

This script facilitates the process of accessing a notification email from Outlook 365, which contains a secure link to view a message. The script automates the retrieval of this link and the OTP sent by email to authenticate and access the content securely.

**Challenges:**
1. Extracting a 'Read the message' link from an email notification sent via Outlook 365.
2. Monitoring Gmail programmatically for an OTP email sent as part of Microsoft's secure email authentication process.
3. Using the OTP to authenticate and access the secured email content.
4. Securely downloading an attachment (e.g., Carol's CSV with PHI data) directly from Microsoft's servers to the client machine without it ever passing through Google's servers.
5. Handling potential errors and edge cases, such as delays in receiving the OTP email or issues with the link extraction.
6. Ensuring HIPAA compliance in handling PHI data, especially during data transfer directly from Microsoft's secured environment.

**Suggested Approach:**
1. **Authentication and Accessing Gmail**: Use the Gmail API in a client-side Python script to monitor and extract necessary details (links and OTPs) from emails.
2. **Extracting the 'Read the Message' Link**: Identify and extract the URL from the notification email which navigates to Microsoft's secure email portal.
3. **Monitoring for the OTP**: Continuously check the Gmail inbox for an incoming OTP email following the initiation of the authentication process through the extracted link.
4. **Using the OTP**: Use the OTP to complete the authentication process on the Microsoft portal and gain access to the secure content.
5. **Downloading the Attachment**: Once authenticated, directly download the PHI-containing document from the Microsoft portal to the client machine, ensuring encryption and security throughout the transfer process.

**Steps Involved:**
1. Set up the Python client to monitor Gmail and interact with the Google Apps Script for initial link extraction.
2. Extract the 'Read the message' link from the relevant email using the Google Apps Script.
3. Use the Python client to handle user interactions required to navigate the Microsoft authentication portal, enter the OTP, and download the secured content.
4. Ensure secure handling of all PHI data, with strong emphasis on HIPAA compliance throughout the process.

**Breakdown:**

**Python Script (Client Side)**
- **Functionality**:
    - Interface with the user to initiate the process.
    - Monitor Gmail for emails that contain the secure link and OTP.
    - Handle the navigation to the secure Microsoft portal and input the OTP.
    - Directly download the secure content once access is granted.
- **Libraries and APIs**:
    - Google API Python Client to interact with Gmail.
    - Requests for HTTP requests to handle link extraction and OTP monitoring.
    - OS and Sys libraries for local system interactions.

**Google Apps Script (Server Side)**
- **Functionality**:
    - Authenticate and access Gmail to extract the 'Read the message' link.
    - Provide support for initial email filtering and link extraction.
    - Not involved in the decryption or direct handling of PHI data to ensure compliance with HIPAA.

This architecture ensures the system handles sensitive PHI data in compliance with HIPAA regulations while maintaining robust and reliable email processing and file handling mechanisms. All sensitive data transfers occur directly from Microsoft's secure environment, minimizing the risk of unauthorized access during transit.

TODO (High GMail)

Notes: So the XP system can't do auth natively outside a browser and the libraries available wouldnt be
able to do auth on the fly so we'd basically be stuck getting tokens manually that only last an hour and 
then copy pasting those into the script like a rotating key which is not very UX friendly. So, any of the interactions 
necessary should move to an HTML page that's served by Google Apps Script so there's no "interaction" that has to 
happen outside of the webapp/browser. The only thing XP can do is send pre-defined actions. So, basically the XP client-side 
has to pretty much just be a URL to open. There essentially can't be any communication.
"""
import sys
import requests
import subprocess
import webbrowser
from MediLink_ConfigLoader import log

def open_browser_with_executable(url, browser_path=None):
    """
    Tries to open a browser with the specified URL using a provided browser executable path or the default browser.
    """
    try:
        if browser_path:
            # Use the provided executable path to open the browser
            subprocess.Popen([browser_path, url])
            log("Browser opened with provided executable path.")
        else:
            # Fall back to the default browser
            webbrowser.open(url)
            log("Default browser opened.")
    except Exception as e:
        log("Failed to open browser: {}".format(e))

def initiate_link_retrieval():
    """
    Sends a request to initiate the 'get_link' action, which handles the selection of emails
    and link retrieval through the web application.
    """
    log("Initiating link retrieval process.")
    url = "https://script.google.com/macros/s/AKfycbzlq8d32mDlLdtFxgL_zvLJernlGPB64ftyxyH8F1nNlr3P-VBH6Yd0NGa1pbBc5AozvQ/exec"
    params = {'action': 'get_link'}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Assuming the server redirects to the URL or provides it in the response for opening in the browser
            link_url = response.text  # You might need to parse this if it's in JSON or a different format
            browser_path = sys.argv[1] if len(sys.argv) > 1 else None
            open_browser_with_executable(link_url, browser_path)
        else:
            log("Failed to initiate link retrieval: HTTP status {}".format(response.status_code))
    except Exception as e:
        log("Error during link retrieval initiation: {}".format(e))

if __name__ == "__main__":
    initiate_link_retrieval()