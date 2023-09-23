import pdfkit
from datetime import datetime


def generate_html(title, list_of_messages_obj):
    """
    Generate an HTML report with the given title and list of message object.

    Args:
        title (str): The title of the HTML report.
        list_of_messages_obj (list): A list of message objects to be included in the report.

    Returns:
        str: The generated HTML content as a string.
    """
    # Obtenez la date et l'heure actuelles
    current_datetime = datetime.now().strftime("%I:%M %p, %B %d, %Y")

    # Début de la page HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8"> 
        <title>{}</title>
        <style>
            @page {{
                size: A4;
                margin: 0;
            }}
            body {{
                font-size: 11px;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 100%;
                padding: 20px;
                box-sizing: border-box;
            }}
            .email-header {{
                background-color: #007bff;
                color: #fff;
                padding: 10px;
            }}
            .email-body {{
                padding: 20px;
            }}
        </style>
    </head>
    <body>
    <h1>{}</h1>
    <p>Generated with MessageTrackPro, <a href="https://github.com/ValentinLibouton/MessageTrackPro">https://github.com/ValentinLibouton/MessageTrackPro</a>, {},</p>
    """.format(title, title, current_datetime)

    # Insérer les données
    for i, message in enumerate(list_of_messages_obj):
        # Numéro de message (optionnel)
        html += "<h2>Message {}</h2>".format(i + 1)

        # Insérer les détails du message
        html += "<b>Date:</b> {} {}&nbsp;&nbsp;&nbsp;&nbsp;<b>Message id:</b> {}&nbsp;&nbsp;&nbsp;&nbsp;<b>Filename:</b> {}<br>".format(
            message.date, message.time, message.message_id, message.filename)
        html += "<b>Sender:</b> {} {}<br>".format(message.sender_name, message.sender_address)
        html += "<b>Recipient:</b> {} {}&nbsp;&nbsp;&nbsp;&nbsp;<b>Recipient type:</b> {}<br>".format(message.recipient_name,
                                                                                        message.recipient_address,
                                                                                        message.recipient_type)
        html += "<b>Attachments:</b> {}<br>".format(message.attachments)
        html += "<b>Tags:</b> {}<br>".format(message.tags)
        html += "<b>Body:</b><br>{}".format(message.content)

        # Séparation entre les messages
        if i < len(list_of_messages_obj) - 1:
            html += "<hr>"

    # Fin du conteneur de l'email
    html += """
        </div>
    </div>
    """

    # Pied de page avec la date et l'heure actuelles
    html += """
    <br>
    <p>Generated with MessageTrackPro, <a href="https://github.com/ValentinLibouton/MessageTrackPro">https://github.com/ValentinLibouton/MessageTrackPro</a>, {},</p>
    </body>
    </html>
    """.format(current_datetime)

    return html


def html_to_pdf(html_filename, pdf_filename):
    """
    Convert an HTML file to a PDF file using the specified filenames.

    Args:
        html_filename (str): The filename of the input HTML file.
        pdf_filename (str): The filename of the output PDF file.

    Returns:
        None
    """
    # Convertir HTML en PDF
    pdfkit.from_file(html_filename, pdf_filename, options={'page-size': 'A4', 'no-images': None})


def write_messages(title, list_of_messages_obj):
    """
    Generate an HTML report with the provided title and list of message objects, and convert it to a PDF.

    Args:
        title (str): The title of the HTML report.
        list_of_messages_obj (list): A list of message objects to be included in the report.

    Returns:
        None
    """
    # Generation du code HTML
    html_content = write_messages(title=title, list_of_messages_obj=list_of_messages_obj)

    # Écriture du contenu HTML dans un fichier
    with open("output.html", "w") as html_file:
        html_file.write(html_content)
    # Convertion en PDF
    html_to_pdf("output.html", "output.pdf")


if __name__ == "__main__":
    pass
