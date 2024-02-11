# Funktion zum Feststellen, ob die formula ein Ausdruck ist, der komplett von Klammern umschlossen ist
def uselessbraces(form):
    if isvariable(form):
        return False
    if form[0] == "(" and form[-1] == ")":
        numberofopening = 0
        numberofclosing = 0
        for i in range(len(form)):
            x = form[i]
            if x == "(":
                numberofopening += 1
            elif x == ")":
                numberofclosing += 1
            if numberofopening == numberofclosing and not i == len(form) - 1:
                return False
        else:
            return True


# Funktion zum testen ob etwas nur eine Variable ist
def isvariable(form):
    for x in form:
        if x in {"|", "&", "!", "(", ")", ">", "="}:
            return False
    return True


# Funktion um alle Variablen in einer Formel zu finden und diese als Liste, sortiert nach Position in der Formel, zurückzugeben
def allvariables(form):
    variables = []
    for x in subformulas(form):
        if isvariable(x):
            variables.append(x)
    helper = []
    for var in variables:
        helper.append([var, form.index(var)])
    helper.sort(key=lambda var2: var2[1])
    for i in range(len(helper)):
        variables[i] = helper[i][0]
    return variables


# Funktion um zu testen ob etwas eine Negation von etwas ist
def isnegation(form):
    if form[0] == "!" and (uselessbraces(form[1:]) or isvariable(form[1:])):
        return True
    return False


# Funktion um zu schauen, ob etwas ein regelkonformer Klammerausdruck ist
def correctbraces(form):
    opening = 0
    closing = 0
    for x in form:
        if x == "(":
            opening += 1
        elif x == ")":
            closing += 1
        if closing > opening:
            return False
    if not closing == opening:
        return False
    return True


def elminateuselessbraces(form):
    if uselessbraces(form):
        return form[1:-1]
    return form


def subformulas(form):
    if len(form) == 0:
        return set()

    # Entferne alle unnötigen Klammern (Aber nur die, die komplett aussenrum sind)
    form = elminateuselessbraces(form)

    toreturn = set()
    toreturn.add(form)
    for x in directsubformulas(form)[0]:
        toreturn.add(x)
        toreturn.update(subformulas(x))
    return toreturn


# Funktion um alle unmittelbaren Subformulas zu finden (Nächste Ebene im Syntaxbaum). Funktion gibt auch das höchste
# Element im Syntaxbaum zurück und dessen Position in der Formel (In der Version ohne unnötige Klammern)
def directsubformulas(form):
    if form == "":
        return [], "e", 0

    dirsubformulas = []

    # Entferne alle unnötigen Klammern (Aber nur die, die komplett aussenrum sind)
    if uselessbraces(form):
        return directsubformulas(form[1:-1])

    # Checken ob form einfach nur eine einzige Variable ist
    if isvariable(form):
        return [], "v", 0

    # Nun muss man das oberste Element im Syntaxbaum finden

    # Checken ob das oberste Element ein logisches Nicht ist
    if isnegation(form):
        dirsubformulas.append(elminateuselessbraces(form[1:]))
        return dirsubformulas, "!", 0

    # Checken ob das oberste Element eine logische Äquivalenz ist. Äquivalenz wird RECHTSASSOZIATIV behandelt
    for i in range(len(form)):
        if form[i] == "=" and correctbraces(form[i + 1:]):
            dirsubformulas.append(elminateuselessbraces(form[:i]))
            dirsubformulas.append(elminateuselessbraces(form[i + 1:]))
            return dirsubformulas, "=", i

    # Checken ob das oberste Element eine logische Implikation ist
    for i in range(len(form)):
        if form[i] == ">" and correctbraces(form[i + 1:]):
            dirsubformulas.append(elminateuselessbraces(form[:i]))
            dirsubformulas.append(elminateuselessbraces(form[i + 1:]))
            return dirsubformulas, ">", i

    # Checken ob das oberste Element ein logisches Oder ist
    for i in range(len(form)):
        if form[-i] == "|" and correctbraces(form[-i + 1:]):
            dirsubformulas.append(elminateuselessbraces(form[-i + 1:]))
            dirsubformulas.append(elminateuselessbraces(form[:-i]))
            return dirsubformulas, "|", i

    # Nun muss das oberste Element ein logisches UND sein
    for i in range(len(form)):
        if form[-i] == "&" and correctbraces(form[-i + 1:]):
            dirsubformulas.append(elminateuselessbraces(form[-i + 1:]))
            dirsubformulas.append(elminateuselessbraces(form[:-i]))
            return dirsubformulas, "&", i

    raise ValueError("Formel ist nicht syntaktisch korrekt")


# & ist das logische Und, | ist das logische Oder, > ist die logische Implikation, = ist die logische Äquivalenz und
# ! ist das logische Nicht
# Variablen dürfen logischerweise kein logisches Zeichen oder Klammern beinhalten. Die
# eingegebene Formel muss syntaktisch korrekt sein

if __name__ == "__main__":
    formula = input("Gib jetzt die Formel ein: ")

    print(subformulas(formula))