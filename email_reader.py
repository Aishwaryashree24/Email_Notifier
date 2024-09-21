from imapclient import IMAPClient

import time
# import imaplib
# import email
from email.header import decode_header

def extract_address(address_obj):
    if isinstance(address_obj, tuple):
        if hasattr(address_obj[0], 'decode'):
            return address_obj[0].decode('utf-8')
        else:
            return address_obj[0]
    else:
        return str(address_obj)

def read_emails_real_time(username, password):
    # Connect to the IMAP server (Gmail example)
    with IMAPClient('imap.gmail.com') as client:
        # Log in to your email account
        client.login(username, password)

        # Select the mailbox you want to monitor (e.g., 'inbox')
        client.select_folder('inbox')

        # Set to store processed email IDs
        processed_ids = set()

        # Variable to store email content
        email_template = ""

        print("Monitoring for new emails. Press Ctrl+C to exit.")

        try:
            while True:
                # Search for unseen (new) messages
                messages = client.search(['UNSEEN'])

                for uid, message_data in client.fetch(messages, ['ENVELOPE']).items():
                    envelope = message_data[b'ENVELOPE']
                    email_id = envelope.message_id

                    # Check if the email has been processed already
                    if email_id not in processed_ids:
                        subject = envelope.subject

                        # Check if the subject is None and provide a default value
                        subject_str = subject.decode('utf-8') if subject else "No Subject"
                        from_email = extract_address(envelope.from_)  # Extract 'From' address

                        # Store the content in the email_template variable
                        email_template = f"New Email Received - From: {from_email}, Subject: {subject_str}"

                        print(email_template)  # Optional: Print the content

                        # Add the email ID to the processed set
                        processed_ids.add(email_id)

                # Wait for a few seconds before checking again
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nExiting program.")

if __name__ == "__main__":
    # Replace 'your_email@gmail.com' and 'your_email_password' with your actual credentials
    read_emails_real_time('your_email@gmail.com', 'your_email_password')
