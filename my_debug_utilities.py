def log(content, comment=None, style=None):
    if style == 'blue':
        style = Styles.blue
    elif style == 'cyan':
        style = Styles.cyan
    elif style == 'pink':
        style = Styles.pink
    elif style == 'yellow':
        style = Styles.yellow
    elif style == 'red':
        style = Styles.red
    elif style == 'green':
        style = Styles.green
    else:
        style = None
    if comment:
        print(wrap('LOG: ' + str(comment) + ' >>> ' + str(content), style))
    else:
        print(wrap('LOG: ' + str(content), style))


def warning(content):
    print(wrap('WARNING: ' + str(content), Styles.yellow))


def error(content):
    print(wrap('ERROR: ' + str(content), Styles.red))


class Styles:
    pink = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


def wrap(string, style):
    if style:
        return style + string + Styles.end
    else:
        if style is not None:
            warning('unknown style - nothing was changed')
        return string


