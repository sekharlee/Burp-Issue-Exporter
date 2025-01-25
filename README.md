### Burp Issue Exporter

Burp Issue Exporter is a powerful Burp Suite extension designed to simplify the process of exporting or copying issue details from the Scanner tab. Whether you need to document findings, share vulnerabilities with your team, or generate reports, this tool makes it easy to export or copy issue details in a structured and consistent format.
Features

    Export to CSV: Save issue details to a CSV file in the Downloads folder.

    Copy to Clipboard: Copy issue details to the clipboard for quick sharing or pasting into other tools.

    Handles Multiple Issues: Works with multiple selected issues, including those with multiple endpoints.

    Customizable Output:

        Marks empty fields as "NA" for consistency.

        Limits response content to 30 lines and appends \n<REDACTED> if truncated.

        Removes HTML tags from mitigation details.

    User-Friendly: Provides a dialog box to choose between exporting to CSV or copying to the clipboard.

Installation
Prerequisites

    Burp Suite: Ensure you have Burp Suite installed.

    Jython: Download the Jython standalone JAR file from the official Jython website.

Steps

    Configure Jython in Burp Suite:

        Go to the Extender tab → Options → Python Environment.

        Set the path to the Jython JAR file.

    Load the Extension:

        Go to the Extender tab → Extensions → Add.

        Choose Python as the extension type.

        Paste the script into the editor and load it.

![image](https://github.com/user-attachments/assets/c72c1376-c861-4770-b498-2d218ad059af)
![image](https://github.com/user-attachments/assets/1e612063-fda3-46e7-864a-0b3d5ecac4ea)


Usage

    Select Issues:

        Navigate to the Scanner tab in Burp Suite.

        Select one or more issues.

    Export/Copy Issue Details:

        Right-click on the selected issues.

        Choose Export/Copy Issue Details from the context menu.

    Choose an Option:

        A dialog box will appear with two options:

            Copy to Clipboard: Copies the issue details to the clipboard.

            Export to CSV: Saves the issue details to a CSV file in the Downloads folder.

Troubleshooting

    Extension Not Loading:

        Ensure Jython is properly configured in Burp Suite.

        Check the Errors tab in the Extender section for any error messages.

    No Issues Selected:

        If no issues are selected, the extension will notify you with an alert.

    CSV File Not Saved:

        Ensure you have write permissions to the Downloads folder.
