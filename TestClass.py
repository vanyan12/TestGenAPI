import json
import os
from Data import Requirements
from Answers import Answers
from pylatex import Document, Command, Section
from pylatex.utils import NoEscape


class Test(Document):
    def __init__(self):
        super().__init__()

        # For handling correct task numering
        self.task_counter = 1
        self.answers = {}

        self.preamble.append(Command("title", "Թեստ"))
        self.preamble.append(Command("date", NoEscape(r"")))
        self.append(NoEscape(r"\maketitle"))
        self.preamble.append(NoEscape(r'\titlespacing{\title}{0pt}{0pt}{-30pt}'))  # Adjust spacing

        self.preamble.append(NoEscape(r'\usepackage[a4paper, left=0.7in, right=0.7in, top=0.2in, bottom=0.2in]{geometry}'))
        self.preamble.append(NoEscape(r'\renewcommand{\thesection}{\Roman{section}}')) # Section numbering with I, II, III, IV ...
        self.preamble.append(NoEscape(r'\usepackage{indentfirst}'))
        self.preamble.append(NoEscape(r'\usepackage{fontspec}'))
        self.packages.append(NoEscape(r'\usepackage{amsmath}'))
        self.preamble.append(NoEscape(r'\usepackage{polyglossia}'))
        self.packages.append(NoEscape(r'\usepackage{titlesec}'))

        self.preamble.append(NoEscape(r'\setmainfont{GHEAMariam}'))

        self.preamble.append(NoEscape(r'\setlength{\parindent}{25pt}'))

        self.preamble.append(NoEscape(r"\renewcommand{\baselinestretch}{1.5}")) # Line spacing
        self.preamble.append(NoEscape(r'\renewcommand{\normalsize}{\fontsize{14pt}{14pt}\selectfont}'))


        # Settings for Section text to wrap automatically when text is exceeding the page
        self.append(NoEscape(r'''
        \titleformat{\section}[block]
          {\normalfont\Large\bfseries}
          {\thesection}{1em}
          {\parbox{\dimexpr\textwidth-2em}{\raggedright}}
        '''))
    def define_task_type(self, fileName):
        if os.path.basename(os.path.dirname(fileName))[0] in {"2", "3"}:
            return self.add_task
        return self.add_choose_task

    def add_task(self, fileName):
        with open(fileName, "r", encoding="UTF-8") as task:

            # Loads data from json file, converting it to divt (list)
            Task = json.load(task)

            section = os.path.basename(os.path.dirname(fileName)) # this is correct as we should give path

            with self.create(Section(NoEscape(Requirements[section] if Task["requirement"] == "" else Task["requirement"]))):

                # Adding tasks to pdf iteratively
                for i in range(0, len(Task["data"])):
                    self.append(NoEscape(fr"\hangindent=50pt {self.task_counter}) \hspace{{10pt}}" + Task["data"][str(i+1)]))
                    self.append(NoEscape(r"\vspace*{5pt} \par "))

                    self.task_counter += 1

    def add_choose_task(self, fileName):
        with open(fileName, "r", encoding="UTF-8") as task:

            # Loads data from json file, converting it to dict (list)
            Task = json.load(task)

            # Extracting section from file path
            section = os.path.basename(os.path.dirname(fileName)) # this is correct as we should give path

            # Creating Section with corresponding text
            with self.create(Section(Requirements[section] if Task["requirement"] == "" else Task["requirement"])):

                # Loop through tasks data and iteratively adding tasks to the document
                for i in range(0, len(Task["data"])):

                    # Adding problem statement
                    self.append(NoEscape(r"\hangindent=50pt \indent" + f"{self.task_counter})" + r"\hspace{10pt}" + Task["data"][str(i+1)]["problem"]))
                    self.append(NoEscape(r"\\[2pt]"))

                    # Adding choose answers
                    self.append(NoEscape(r"\noindent" + r"\hspace*{3cm}" + Task["data"][str(i+1)]["choose"]))
                    self.append(NoEscape(r"\\[2pt] \par"))

                    # Incrementing task_counter for correctly print next task number in document
                    self.task_counter += 1

