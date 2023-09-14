import pdfkit
from datetime import datetime
import data_visualization
TITLE = "Message Track Pro"

def generate_html(title, headers, data):
    # Obtenez la date et l'heure actuelles
    current_datetime = datetime.now().strftime("%I:%M %p, %B %d, %Y")

    # Début de la page HTML
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8"> 
        <title>{}</title>
    </head>
    <body>
    """.format(title)
    html+= f"<h1>{title}</h1>"
    # Tableau des données
    html += "<table border='1'>"

    # Insérer les en-têtes de colonnes
    html += "<tr>"
    for header in headers:
        html += "<th>{}</th>".format(header)
    html += "</tr>"

    # Insérer les données
    for row in data:
        html += "<tr>"
        for cell in row:
            html += "<td>{}</td>".format(cell)
        html += "</tr>"

    # Fin du tableau et de la page
    html += "</table>"

    # Pied de page avec la date et l'heure actuelles
    html += """
    <p>Generated with MessageTrackPro, <a href="https://github.com/ValentinLibouton/MessageTrackPro">https://github.com/ValentinLibouton/MessageTrackPro</a>, {},</p>
    </body>
    </html>
    """.format(current_datetime)

    return html

def html_to_pdf(html_filename, pdf_filename):
    # Convertir HTML en PDF
    pdfkit.from_file(html_filename, pdf_filename, options={'page-size': 'A3'})

def write_html_page(html_content):
    # Écriture du contenu HTML dans un fichier
    with open("output.html", "w") as html_file:
        html_file.write(html_content)
    html_to_pdf("output.html", "output.pdf")


if __name__ == "__main__":
    first_name = "Valentin"
    last_name = "Lbtn"
    contact_id = data_visualization.get_contact_id(first_name=first_name, last_name=last_name)
    print(contact_id)
    headers, messages = data_visualization.get_messages_linked_to_contact_id(contact_id=contact_id)
    #headers, messages = data_visualization.find_messages_with_word(contact_id=data_visualization.get_contact_id(first_name=first_name, last_name=last_name), word='anniversary')
    html_content = generate_html(TITLE, headers, messages)
    write_html_page(html_content)




