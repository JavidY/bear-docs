import os
import inspect

from bear_docs_utils import get_bears

def language_generate():
    lang_dict = {}
    for bear in get_bears():
        for language in bear.LANGUAGES:
            if language in lang_dict:
                lang_dict[language].append(bear.name)
            else:
                lang_dict[language] = [bear.name]

    with open("README.rst", "w") as lang_file:
        lang_file.write("Documentation for coala bears\n")
        lang_file.write("=============================\n\n")

        deprecation_notice = ("This repository has been deprecated in favor of "
                              "http://coala.io/#!/languages - please use that. Only "
                              "absolutely critical issues in this repo will be looked into.\n")
        lang_file.write(deprecation_notice)
        lang_file.write("-" * len(deprecation_notice) + "\n\n\n")

        lang_file.write("**This is repository is automatically generated. Please "
                        "make submit any changes to** "
                        "`coala-bears <https://github.com/coala/coala-bears>`_ "
                        "**instead.**\n\n")
        lang_file.write("**Note**: The ``master`` branch contains docs for the latest "
                        "stable version. If you want to view the docs for the "
                        "latest development version, see the ``pre`` branch.\n\n")
        lang_file.write("**Supported Languages ({})**\n----------------------------\n\n"
                        ".. contents::\n"
                        "    :local:\n"
                        "    :depth: 1\n"
                        "    :backlinks: none\n\n".format(len(lang_dict)))
        for language in sorted(lang_dict):
            lang_file.write(language + "\n" + "=" * len(language) + "\n")
            for bear in sorted(lang_dict[language]):
                lang_file.write("* `" + bear + " <docs/" + bear + ".rst>`_\n")
            lang_file.write("\n")
