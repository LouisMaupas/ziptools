# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import os
from dotenv import load_dotenv
load_dotenv() # Permet de charger les variables d'environnement du fichier .env dans ce fichier pour qu'il soit accessible avec os


def SendEmail(destinataire, sujet, corps, signature, fichier):
    # On crée un message multipart car on a le corps et aussi une pièce-jointe
    msg = MIMEMultipart()

    # On crée le corps du mail
    corps_mail = MIMEText(corps + "\n" + signature, 'plain')
    msg['Subject'] = sujet
    msg['From'] = os.getenv('EMAIL')
    msg['To'] = destinataire 

    # Ajout du corps au mail
    msg.attach(corps_mail)

    # Ajout de la pièce-jointe au mail
    with open(fichier,'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name='ziptools.zip'))

    # Envoi le mail via un serveur SMTP
    smtp = smtplib.SMTP(os.getenv('SERVER'), 587)
    smtp.connect(os.getenv('SERVER'), 587)
    smtbLogin = smtp.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))
    smtp.sendmail(os.getenv('EMAIL'), [destinataire], msg.as_string())
    smtp.quit()
    return smtbLogin[1]
