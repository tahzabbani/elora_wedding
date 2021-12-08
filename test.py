import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

apikey = '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'

sg = sendgrid.SendGridAPIClient(api_key=apikey)
from_email = Email("noreply@fahadandelora.com")  # Change to your verified sender
to_email = To("tarobbani@gmail.com")  # Change to your recipient
subject = "Thanks for your RSVP"
content = Content("text/plain", "and u a bitch")
mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()

# Send an HTTP POST request to /mail/send
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)