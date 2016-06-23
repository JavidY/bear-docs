import sys
import os
import inspect

from collections import OrderedDict
from bear_docs_utils import get_bears
from language_generate import language_generate


def text_wrap(*args, delimiter=' ', end='\n', limit=80):
    """
    Breaks it wordwise when going further than ``limit`` chars.
    :param args:
        The stuff you want to have printed.
    :param delimiter:
        Will be placed between all the args.
    :param limit:
        Char limit.
    :param end:
        An ending, will be put as last character and doesn't count into the
        char limit.
    :return:
        A list of strings, each element to be written on its own line.
    """
    output = delimiter.join(args)
    lines = output.splitlines(keepends=True)
    results = []
    for line in lines:
        curr_print = line
        while len(curr_print.rstrip('\n')) > limit:
            splitpos = curr_print[:limit].rfind(' ')
            if splitpos < 0:
                # Word too long, search for a space left from limit at least
                splitpos = curr_print.find(' ')
                if splitpos < 0:
                    break  # Break out and add the long thing in the next line

            results.append(curr_print[:splitpos])
            curr_print = curr_print[splitpos+1:]

        results.append(curr_print)

    return results

if __name__ == "__main__":
    bears = get_bears()
    for bear in bears:
        output = "**" + bear.name + "**\n"
        output += "=" * (4 + len(bear.name)) + "\n\n"
        output += bear.get_metadata().desc + "\n\n"
        output += "`Supported Languages <../README.rst>`_" + "\n-----\n\n"
        output += "\n".join(["* " + x for x in sorted(bear.LANGUAGES)])
        output += "\n\n"
        par = {}
        lmax = -1
        rmax = -1
        meta = bear.get_metadata()
        for param in meta.non_optional_params:
            key = " ``" + param + "`` "
            par[key] = text_wrap(bear.get_metadata().non_optional_params[param][0], limit=60)
            par[key] = [g.strip() for g in par[key]]
            lmax = max(lmax, len(key))
            rmax = max(rmax, max(len(g) for g in par[key]))
        for param in meta.optional_params:
            key = " ``" + param + "`` "
            par[key] = text_wrap(bear.get_metadata().optional_params[param][0], limit=60)
            par[key] = [g.strip() for g in par[key]]
            lmax = max(lmax, len(key))
            rmax = max(rmax, max(len(g) for g in par[key]))
        if len(par):
            lmax = max(lmax, len(" Setting"))
            rmax = max(rmax, len("Meaning"))
            header = False
            for key in sorted(par):
                if not header:
                    output += "Settings\n--------\n\n"
                    output += "+" + "-" * (lmax) + "-+-" + "-" * (1 + rmax) + "+\n"
                    output += "| Setting" + " " * (lmax - len(" Setting")) + " |  Meaning" + " " * (rmax - len("Meaning")) + "|\n"
                    output += "+" + "=" * lmax + "=+=" + "=" * (1 + rmax) + "+\n"
                    header = True
                output += "| " + " " * lmax + "| " + " " * (1 + rmax) + "|\n"
                output += "|" + key + " " + " " * (lmax - len(key)) + "| " + par[key][0] + " " * (1 + rmax - len(par[key][0]))
                if len(par[key]) > 1:
                    output += "|\n"
                else:
                    output += "+\n"
                for text in par[key][1:]:
                    output += "|" + " " * (lmax + 1) + "| " + text + " " * (1 + rmax - len(text)) + "|\n"
                output += "| " + " " * lmax + "| " + " " * (1 + rmax) + "|\n"
                output += "+" + "-" * lmax + "-+-" + "-" * (1 + rmax) + "+\n"
            output += "\n\* denotes required param"

        if len(bear.can_detect):
            output += "\n\nCan Detect\n----------\n\n"
            output += "\n".join(sorted(["* " + x for x in bear.can_detect]))

        if bear.LICENSE:
            output += "\n\nLicense\n-------\n\n"
            output += bear.LICENSE

        if len(bear.AUTHORS):
            output += "\n\nAuthors\n-------\n\n"
            for author, author_email in zip(bear.AUTHORS, bear.AUTHORS_EMAILS):
                output += "* " + author + " (" + author_email + ")\n"

        with open("docs/" + bear.name + ".rst", "w") as bear_file:
            bear_file.write(output)

    language_generate()

    if len(sys.argv) == 1:
        os.system("git add -A && git commit -m 'Docs Update' && git push")
