Burp Issue Exporter

Burp Issue Exporter is a Burp Suite extension designed to simplify the process of exporting or copying issue details from the Scanner tab. It allows you to:

    Export issues to a CSV file for easy documentation and reporting.

    Copy issue details to the clipboard for quick sharing or pasting into other tools.

The tool handles multiple issues, including those with multiple endpoints, and ensures consistent formatting by marking empty fields as "NA" and truncating long responses.
Key Features

    Export to CSV: Save issue details to a CSV file in the Downloads folder.

    Copy to Clipboard: Copy issue details to the clipboard for easy pasting.

    Handles Multiple Issues: Works with multiple selected issues, including those with multiple endpoints.

    Customizable Output:

        Marks empty fields as "NA".

        Limits response content to 30 lines and appends \n<REDACTED> if truncated.

        Removes HTML tags from mitigation details.

    User-Friendly: Provides a dialog box to choose between exporting to CSV or copying to the clipboard.

Installation

    Install Jython:

        Download the Jython standalone JAR file from the official Jython website.

        In Burp Suite, go to the Extender tab → Options → Python Environment.

        Set the path to the Jython JAR file.

    Load the Extension:

        Go to the Extender tab → Extensions → Add.

        Choose Python as the extension type.

        Paste the script into the editor and load it.

Usage

    Select Issues:

        Go to the Scanner tab.

        Select one or more issues.

    Export/Copy Issue Details:

        Right-click on the selected issues.

        Choose Export/Copy Issue Details from the context menu.

    Choose an Option:

        A dialog box will appear asking whether to Copy to Clipboard or Export to CSV.

        Select your preferred option.
