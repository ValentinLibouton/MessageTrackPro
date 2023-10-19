with open('message_1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

def parse(html_content):
    i = 0
    balises = []
    while i < len(html_content):
        word = ""
        if html_content[i] == "<":
            word += html_content[i]
            while html_content[i] != ">" and i < len(html_content):

                i += 1
                word += html_content[i]
                if html_content[i] == "<":
                    print("Pas une balise! ou balise incomplète:", word)
                    word = ""
            if word:
                balises.append(word)
        i += 1
    return balises

def tokenize(balises):
    tokens = []
    unknow_balises = []
    for balise in balises:
        if balise.startswith("<style ") and balise.endswith(">"):
            tokens.append("open_style")

        elif balise.startswith('<div class=') and balise.endswith('>'):
            tokens.append('open_div_class')
        elif balise.startswith('<meta ') and balise.endswith("/>"):
            tokens.append("meta")
        elif balise.startswith('<base ') and balise.endswith("/>"):
            tokens.append("base")
        elif balise.startswith('<body ') and not balise.endswith("/>") and balise.endswith(">"):
            tokens.append('open_body')
        elif balise.startswith("<div ") and balise.endswith('>'):
            tokens.append('open_div')
        elif balise.startswith("<h1 ") and balise.endswith('>'):
            tokens.append('open_h1')
        elif balise.startswith("<a ") and balise.endswith('>'):
            tokens.append('open_a')
        elif balise.startswith("<span ") and balise.endswith('>'):
            tokens.append('open_span')
        elif balise.startswith("<img ") and balise.endswith('/>'):
            tokens.append('img')
        elif balise.startswith('<ul ') and balise.endswith('>'):
            tokens.append('open_ul')


        #ToDO:les autres cas
        elif balise == "</style>":
            tokens.append("close_style")
        elif balise == "</div>":
            tokens.append("close_div")
        elif balise == "<html>":
            tokens.append("open_html")
        elif balise == "<head>":
            tokens.append("open_head")
        elif balise == "<title>":
            tokens.append("open_title")
        elif balise == "</title>":
            tokens.append("close_title")
        elif balise == "</head>":
            tokens.append("close_head")
        elif balise == '<div>':
            tokens.append('open_div')
        elif balise == '</span>':
            tokens.append('close_span')
        elif balise == '</a>':
            tokens.append('close_a')
        elif balise == '</h1>':
            tokens.append('close_h1')
        elif balise == '</body>':
            tokens.append('close_body')
        elif balise == '</html>':
            tokens.append('close_html')
        elif balise == '<li>':
            tokens.append('start_li')
        elif balise == '</li>':
            tokens.append('close_li')
        elif balise == '</ul>':
            tokens.append('close_ul')
        elif balise == '<br />':
            tokens.append("br /")

        else:
            unknow_balises.append(balise)
    if unknow_balises:
        print("Some balises not passed")

    return tokens, unknow_balises


tokens, unknow_balises = tokenize(parse(html_content))



for token in tokens:
    print(token)
print("Balises non reconnues:")
print(unknow_balises)