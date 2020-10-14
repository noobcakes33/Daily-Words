import time
from time import gmtime, strftime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class DailyWords:
    def __init__(self):
        self.to_send_words = 'wordlist.txt'
        self.already_sent_words = 'sent_words.txt'
        self.words = ""
        self.num_of_words = 5
        self.sender_email = "testm.markiewiczalsaeedi@gmail.com"
        self.receiver_emails = ["testm.markiewiczalsaeedi@gmail.com", "m.markiewiczalsaeedi@gmail.com"]
        self.password = "VA170803"

    def get_words(self):
        with open(self.to_send_words) as newList:
            with open(self.already_sent_words, "w") as oldList:
                all_words = newList.readlines()
                for each_line in range(0, len(all_words), self.num_of_words):
                    words_of_today = all_words[each_line: each_line+self.num_of_words]
                    oldList.write("------------------------------------------")
                    oldList.write("Today's words sent at: {}\n\n".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
                    for word in words_of_today:
                        oldList.write(word)
                        self.words += "<br>{}<br>\n".format(word)
                    self.send_email_with_words()
                    print("Daily Words sent at: {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
                    self.words = ""
                    time.sleep(60*60*24)  # delay for 24 hours
                    #break

    def send_email_with_words(self):
    	message = MIMEMultipart("alternative")
    	message["Subject"] = "Let's study arabic words!"
    	message["From"] = self.sender_email

    	# Create the plain-text and HTML version of your message
    	html = """
    	<html>
    	  <body>
    	    <h3>New Words for Today.</h3><br>""" + self.words + """
    	  </body>
    	</html>"""

    	part2 = MIMEText(html, "html", _charset="UTF-8")

    	# Add HTML/plain-text parts to MIMEMultipart message
    	# The email client will try to render the last part first
    	message.attach(part2)

    	# Create secure connection with server and send email
    	for i in range(len(self.receiver_emails)):
    		message["To"] = self.receiver_emails[i]
    		context = ssl.create_default_context()
    		with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    		    server.login(self.sender_email, self.password)
    		    server.sendmail(
    		        self.sender_email, self.receiver_emails[i], message.as_string()
    		    )


if __name__ == "__main__":
    dw = DailyWords()
    dw.get_words()
