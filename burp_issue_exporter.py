from burp import IBurpExtender, IContextMenuFactory, IScanIssue
from java.util import ArrayList
from javax.swing import JMenuItem, JOptionPane
from java.awt.datatransfer import StringSelection
from java.awt import Toolkit
import re
import csv
import os

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Export/Copy Issue Details")
        callbacks.registerContextMenuFactory(self)
        print("[*] Export/Copy Issue Details extension loaded.")
        return

    def createMenuItems(self, invocation):
        self._invocation = invocation
        menu = ArrayList()
        menu_item = JMenuItem("Export/Copy Issue Details", actionPerformed=self.export_or_copy_issues)
        menu.add(menu_item)
        return menu

    def export_or_copy_issues(self, event):
        # Get selected issues from the context menu invocation
        context = self._invocation.getSelectedIssues()
        if not context:
            print("[!] No issues selected.")
            self._callbacks.issueAlert("No issues selected.")
            return

        # Ask the user whether to export to CSV or copy to clipboard
        options = ["Copy to Clipboard", "Export to CSV"]
        choice = JOptionPane.showOptionDialog(
            None,
            "Do you want to copy the issue details to the clipboard or export them to a CSV file?",
            "Export/Copy Issue Details",
            JOptionPane.DEFAULT_OPTION,
            JOptionPane.QUESTION_MESSAGE,
            None,
            options,
            options[0]
        )

        if choice == 0:  # Copy to Clipboard
            self.copy_issues_to_clipboard(context)
        elif choice == 1:  # Export to CSV
            self.export_issues_to_csv(context)

    def copy_issues_to_clipboard(self, issues):
        # Extract details for all selected issues
        issues_data = []
        for issue in issues:
            try:
                issues_data.append(self.get_issue_data(issue))
            except Exception as e:
                print("[!] Error processing issue '{}': {}".format(issue.getIssueName(), str(e)))

        if not issues_data:
            print("[!] No valid issue data to copy.")
            self._callbacks.issueAlert("No valid issue data to copy.")
            return

        # Combine all issues into a single string
        combined_issues_data = "\n\n".join(issues_data)

        # Copy the combined issue data to the clipboard
        toolkit = Toolkit.getDefaultToolkit()
        clipboard = toolkit.getSystemClipboard()
        clipboard.setContents(StringSelection(combined_issues_data), None)

        # Notify the user
        print("[*] Issue details copied to clipboard.")
        self._callbacks.issueAlert("Issue details copied to clipboard.")

    def export_issues_to_csv(self, issues):
        # Define the CSV file path in the Downloads folder
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        output_file = os.path.join(downloads_folder, "exported_issues.csv")

        # Extract details for all selected issues
        issues_data = []
        for issue in issues:
            try:
                issues_data.append(self.get_issue_data_for_csv(issue))
            except Exception as e:
                print("[!] Error processing issue '{}': {}".format(issue.getIssueName(), str(e)))

        if not issues_data:
            print("[!] No valid issue data to export.")
            self._callbacks.issueAlert("No valid issue data to export.")
            return

        # Write the issues to a CSV file
        try:
            with open(output_file, "wb") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Finding Name", "Severity", "Affected Endpoints",
                    "Description", "Mitigation", "Request", "Response"
                ])
                for issue in issues_data:
                    writer.writerow(issue)
            print("[*] Issues exported to {}".format(output_file))
            self._callbacks.issueAlert("Issues exported to {}".format(output_file))
        except Exception as e:
            print("[!] Failed to export issues: {}".format(str(e)))
            self._callbacks.issueAlert("Failed to export issues.")

    def get_issue_data(self, issue):
        # Extract and format issue details for clipboard
        issue_data = (
            "Finding Name: {}\n"
            "Severity: {}\n"
            "Affected Endpoints:\n{}\n"
            "Description: {}\n"
            "Mitigation: {}\n"
            "Request:\n{}\n"
            "Response:\n{}\n"
        ).format(
            issue.getIssueName() or "NA",
            issue.getSeverity() or "NA",
            self.get_affected_endpoints(issue),
            issue.getIssueDetail() or "NA",
            self.remove_html_tags(issue.getRemediationBackground()),
            self.get_request(issue),
            self.get_response(issue)
        )
        return issue_data

    def get_issue_data_for_csv(self, issue):
        # Extract and format issue details for CSV
        return [
            issue.getIssueName() or "NA",
            issue.getSeverity() or "NA",
            self.get_affected_endpoints(issue),
            issue.getIssueDetail() or "NA",
            self.remove_html_tags(issue.getRemediationBackground()),
            self.get_request(issue),
            self.get_response(issue)
        ]

    def get_affected_endpoints(self, issue):
        # Get all unique endpoints for the issue
        endpoints = set()
        for message in issue.getHttpMessages():
            endpoints.add(str(message.getUrl()))
        return "\n".join(endpoints) if endpoints else "NA"

    def get_request(self, issue):
        # Get the request for the issue (if available)
        messages = issue.getHttpMessages()
        if messages:
            return self._helpers.bytesToString(messages[0].getRequest()) or "NA"
        return "NA"

    def get_response(self, issue):
        # Get the response for the issue (if available)
        messages = issue.getHttpMessages()
        if messages:
            return self.limit_response_lines(self._helpers.bytesToString(messages[0].getResponse()))
        return "NA"

    def remove_html_tags(self, text):
        # Remove HTML tags from the text
        if not text:
            return "NA"
        clean_text = re.sub(r'<[^>]+>', '', text)  # Remove all HTML tags
        clean_text = re.sub(r'\s+', ' ', clean_text)  # Replace multiple spaces with a single space
        return clean_text.strip()

    def limit_response_lines(self, response):
        # Limit the response to the first 30 lines
        if not response:
            return "NA"
        lines = response.splitlines()
        if len(lines) > 30:
            return "\n".join(lines[:30]) + "\n<REDACTED>"
        return response

# Register the extension
BurpExtender()
