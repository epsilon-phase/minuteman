__author__ = 'awhite'

from datetime import datetime

from pylatex import Document, Section, Subsection, \
    Table, Package, Enumerate

document = Document()

stack = []
document.packages.append(Package('geometry', options=['tmargin=1cm', "lmargin=2.4cm"]))
stack.append((document, 0))
document.append("hello")

context = 0
maxlist = 3
symbols = dict()
labels = dict()
settings=dict()
settings['auto-para']=False

def get_qualified_name(item):
    global symbols
    p = ""
    writething = ""
    l = type(item)
    if l == str:
        p = item
    if l == Document:
        p = "Document"
    if l == Enumerate:
        p = "List"
    if l == Table:
        p = "Table"
    if l == Section:
        p = "Section:" + str(item)
    if l == Subsection:
        p = 'Subsection:' + str(item)
    if item in labels:
        writething=labels[item]
    return "{0}\t{1}".format(p, writething)


def printwithin(l, i, j):
    ll = len(l)
    print("Current element has {0} Elements\n".format(ll))
    for z in range(i, i+j):
        if z < ll:
            print(str(z) + ":" + get_qualified_name(l[z]))


def append_to_thing(thing, item):
    if type(thing) == Enumerate:
        thing.add_item(item)
    else:
        #Break the paragraph
        if settings['auto-para']:
            thing.append("")
        thing.append(item)


def append_mode(i):
    n = True
    while n:
        line = input("")
        g = line.split(" ")
        for z in g:
            if z == "\\quit" or z == '\\exit':
                n = False
        if n:
            append_to_thing(i, line)

#todo rewrite to be more functional, so that things can be interpreted in a more meaningingful manner, without as much work.
def main():
    global context
    i, context = stack[0]
    quityet = False
    while not quityet:
        printwithin(i, context, maxlist)
        prompt = ""
        if type(i) == type(Table):
            prompt = "Table>"
        if type(i) == Document:
            prompt = "Document>"
        if type(i) == Subsection:
            prompt = "Subsection>"
        if type(i) == Section:
            prompt = "Section>"
        if type(i) == Enumerate:
            prompt = "List>"

        line = input(prompt)
        g = line.split(" ")
        if len(g) == 1:
            if g[0] == '\\append':
                v = input("line")
                append_to_thing(i, v)
                if len(i) - maxlist > context:
                    context += 1
            if g[0] == '\\list':
                v = Enumerate()
                append_to_thing(i, v)
                stack.append((i, context))
                context = 0
                i = v
            if g[0] == '\\append-mode':
                append_mode(i)
            if g[0] == '\\date':
                append_to_thing(i, str(datetime.now()))
            if g[0] == '\\table':
                v = Table('rc|cl')
                append_to_thing(i, v)
                stack.append((i, context))
                context = 0
                i = v
            if g[0]=='\\para':
                append_to_thing(i,"")
            if g[0]=='\\para-auto':
                settings['auto-para']=settings['auto-para']
        else:
            if g[0] == "\\enter":
                v = i[int(g[1])]
                if type(v) == str:
                    print("It seems unwise to attempt that with a raw string.")
                else:
                    stack.append((i, context))
                    context = 0
                    i = v
            if g[0] == '\\exit':
                i, context = stack.pop()
            if g[0] == '\\generate':
                document.generate_pdf(g[1])
            if g[0] == '\\cursor':
                context = int(g[1])
            if g[0] == "\\delete" or g[0] == "\\remove":
                i.remove(i[int(g[1])])
            if g[0] == '\\append':
                v = int(g[1])
                if type(i[v]) == str:
                    i[v] += input()
            if g[0] == '\\alias':
                symbols[g[1]] = i[int(g[2])]
            if g[0] == '\\addrow':
                # Append the arguments to the thing
                i.add_row(g[1::])
            if g[0] == '\\label':
                labels[i[int(g[1])]] = g[2]


main()


