# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


global config
with open("config.json", "r") as f:
    config = json.load(f)

sender_email = config.get("email").get("address")


def send_email(recipient_email, subject, content, from_email=sender_email):
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(content, "html", "utf-8"))  # Käytetään HTML-muotoilua

    try:
        mail = smtplib.SMTP(
            config.get("email").get("server"), config.get("email").get("port")
        )
        mail.ehlo()
        mail.starttls()
        mail.login(
            config.get("email").get("address"), config.get("email").get("password")
        )
        mail.sendmail(msg["From"], msg["To"], msg.as_string())
        mail.close()
        print("Sähköposti lähetetty onnistuneesti.")
    except Exception as e:
        print(f"Virhe sähköpostia lähettäessä: {str(e)}")


def join_email(recipient, language):
    if language == "en":
        subject = f"Thanks for joinings us!"
        content = f"""Hi {recipient.get('name')},
        
        Thank you very much for joining us!
        
        We use telegram on communication, so you should download it, if you don't already have it.
        
        Link to our main channel is:
        https://t.me/+OpSHLCqznS5hMThk
        
        When you joined us on our website, you said that your skills are:
        """

        for role in recipient.get("roles"):
            content += role + "," + "\n"

        content += """Is the information correct? If not, you can inform us about that, by answering this email.
        
        
        """

    if language == "fi":
        subject = f"Kiitos kun liityit meihin!"

        content = f"""Hei {recipient.get('name')},
        
        Kiitos kun liityit meihin!
        
        Käytämme sisäisessä kommunikaatiossa telegramia, joten sinun kannattaa ladata se, ellei sinulla jo ole sitä.
        
        Pääryhmämme linkki on:
        https://t.me/+OpSHLCqznS5hMThk

        Ilmoittautuessasi mukaan, ilmoitit että taitojasi ovat:
        """.replace(
            "\n", "<br>"
        )

        for role in recipient.get("roles"):
            content += role + "," + "\n"

        content += """Ovatko tiedot oikein? Mikäli eivät, voit saattaa asian tietoomme vastaamalla sähköpostiin.
    
        
        Ystävällisin terveisin,
        SMHV Bot
        """

    msg = MIMEMultipart()
    msg["From"] = config.get("email").get("address")
    msg["To"] = recipient.get("email")
    msg["Subject"] = subject
    # We use utf-8 formatting
    msg.attach(MIMEText(content.replace("\n", "<br>"), "html", "utf-8"))

    try:
        mail = smtplib.SMTP(
            config.get("email").get("server"), config.get("email").get("port")
        )
        mail.ehlo()
        mail.starttls()
        mail.login(
            config.get("email").get("address"), config.get("email").get("password")
        )
        mail.sendmail(msg["From"], msg["To"], msg.as_string())
        mail.close()
        print("Sähköposti lähetetty onnistuneesti.")

    except Exception as e:
        print(f"Virhe sähköpostia lähettäessä: {str(e)}")


def list_join_email(language, email, confirmation_link):
    if language == "fi":
        subject = "Vahvista liittymisesi sähköpostilistalle."
        email_content = "<p>Hei,</p>"
        email_content += "<p>Kiitos, että liityit sähköpostilistallemme! Voit vahvistaa sähköpostiosoitteesi klikkaamalla alla olevaa linkkiä:</p>"
        email_content += (
            """<a href="%s" target="_blank">Vahvista sähköpostiosoite</a>"""
            % confirmation_link
        )
        email_content += "<p>Mikäli et ole liittynyt sähköpostilistallemme, voit jättää tämän viestin huomiotta.</p>"
        email_content += "<p>Kiitos!</p>"

    if language == "en":
        subject = "Confirm joining to our email list."
        email_content = "<p>Hello,</p>"
        email_content += "<p>Thank you for joining our email list! You can confirm your email address by clicking the link below:</p>"
        email_content += (
            """<a href="%s" target="_blank">Confirm Email Address</a>"""
            % confirmation_link
        )
        email_content += (
            "<p>If you haven't joined our email list, you can ignore this message.</p>"
        )
        email_content += "<p>Thank you!</p>"

    msg = MIMEMultipart()
    msg["From"] = config.get("email").get("address")
    msg["To"] = email
    msg["Subject"] = subject
    # We use utf-8 formatting
    msg.attach(MIMEText(email_content.replace("\n", "<br>"), "html", "utf-8"))

    try:
        mail = smtplib.SMTP(
            config.get("email").get("server"), config.get("email").get("port")
        )
        mail.ehlo()
        mail.starttls()
        mail.login(
            config.get("email").get("address"), config.get("email").get("password")
        )
        mail.sendmail(msg["From"], msg["To"], msg.as_string())
        mail.close()
        print("Sähköposti lähetetty onnistuneesti.")

    except Exception as e:
        print(f"Virhe sähköpostia lähettäessä: {str(e)}")
