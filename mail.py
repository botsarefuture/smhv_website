# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


global config
with open("config.json", "r") as f:
    config = json.load(f)


def signup_email(event: dict, recipient: dict, language: str):
    """true

    Args:
        event (dict): the dict of the event
        recipient (dict): the dict of the recipient
        language (str): the language
    """
    introductions = event.get("introductions")

    if language == "en":
        subject = f'Thank you for signing up for event "{event.get("title_en")}"'

        content = f"""<h2>Thank you for signing up!</h2>
        
        Hi {recipient.get('name')},
        
        <br><br>
        
        You have signed up for the following event: <br>

        <strong>{event.get('title_en')}</strong>
        
        <br><br>
        
        When you signed up, you gave us the following informatiedot:
        
        <br><br>
        
        Roles:
        
        <ul>
        """
        for role in recipient.get("roles"):
            content += f"<li>{role}</li>"  # Every role is part of list

        content += f"""
        </ul>
                        
        <h2>Info of event:/h2>
        
        
        Date: {event.get('date')}
        Location: {event.get('location_en')}
        Telengram group (please join): {event.get('telegram_group')}       
        """

        if not len(introductions) == 0:
            content += f"""<br><br>There is introductions for the roles that you have selcted, information below: <br><br>"""

        for introduction in introductions:
            text = f"""
        Date and time: {introduction.get('date')} {introduction.get('time')} <br>
        Address: {introduction.get('location')}<br>
        <br>
        """

            # HACK to make sure that we don't send same brief multiple times...
            if not text in content:
                content += text

            else:
                continue

        if not len(introductions) == 0:
            content += "If you're unable to come into the introduction, please let us know, so we can send you instructions."

    if language == "fi":
        subject = f'Kiitos ilmoittautumisestasi tapahtumaan "{event.get("title_fi")}"'

        content = f"""<h2>Kiitos ilmoittautumisestasi!</h2>
        
        Hei {recipient.get('name')},
        
        <br><br>
        
        Olet ilmoittautunut seuraavaan tapahtumaan: <br>

        <strong>{event.get('title_fi')}</strong>
        
        <br><br>
        
        Ilmoittautuessasi annoit seuraavat tiedot:
        
        <br><br>
        
        Roolit:
        
        <ul>
        """
        for role in recipient.get("roles"):
            content += f"<li>{role}</li>"  # Every role is part of list

        content += f"""
        </ul>
                        
        <h2>Tapahtuman tiedot</h2>
        
        
        Päivämäärä: {event.get('date')}
        Sijainti: {event.get('location_fi')}
        Telegram ryhmä (kannattaa liittyä): {event.get('telegram_group')}       
        """

        if not len(introductions) == 0:
            content += f"""<br><br>Valitsemillesi rooleille järjestetään briiffejä, tiedot alla: <br><br>"""

        for introduction in introductions:
            text = f"""
        Päiväys ja aika: {introduction.get('date')} {introduction.get('time')} <br>
        Osoite: {introduction.get('location')}<br>
        <br>
        """

            # HACK to make sure that we don't send same brief multiple times...
            if not text in content:
                content += text

            else:
                continue

        if not len(introductions) == 0:
            content += "Mikäli et pääse briiffiin, ilmoitathan siitä niin voimme toimittaa kirjallisen briiffimateriaalin."

    msg = MIMEMultipart()
    msg["From"] = config.get("email").get("address")
    msg["To"] = recipient.get("email")
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
        email_content = """
            <!DOCTYPE html>
            <html lang="fi">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Vahvista sähköpostiosoitteesi</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                    }

                    p {
                        margin-bottom: 15px;
                    }

                    a {
                        display: inline-block;
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: #fff;
                        text-decoration: none;
                        border-radius: 5px;
                    }
                </style>
            </head>
            <body>
                <p>Hei,</p>
                <p>Kiitos, että rekisteröidyit palveluumme! Voit vahvistaa sähköpostiosoitteesi klikkaamalla alla olevaa linkkiä:</p>
                <a href="%s" target="_blank">Vahvista sähköpostiosoite</a>
                <p>Mikäli et ole rekisteröitynyt palveluumme, voit jättää tämän viestin huomiotta.</p>
                <p>Kiitos!</p>
            </body>
            </html>
        """ % confirmation_link

    if language == 'en':
        subject = "Confirm joining to our email list."

        email_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Confirm Your Email</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                    }

                    p {
                        margin-bottom: 15px;
                    }

                    a {
                        display: inline-block;
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: #fff;
                        text-decoration: none;
                        border-radius: 5px;
                    }
                </style>
            </head>
            <body>
                <p>Hello,</p>
                <p>Thank you for registering with our service! You can confirm your email address by clicking the link below:</p>
                <a href="%s" target="_blank">Confirm Email Address</a>
                <p>If you did not register with our service, you can ignore this message.</p>
                <p>Thank you!</p>
            </body>
            </html>
        """ % confirmation_link

    
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
        
