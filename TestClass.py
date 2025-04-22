import json
import os
from builtins import type

from Data import Requirements, options
from Answers import Answers
from pylatex import Document, Command, Section, MiniPage
from pylatex.utils import NoEscape



class Test(Document):
    def __init__(self):
        super().__init__()

        # For handling correct task numering
        self.task_counter = 1
        self.answers = {}
        self.answers_input_template = {}
        self.answer_index = 1

        self.preamble.append(Command("title", "Թեստ"))
        self.preamble.append(Command("date", NoEscape(r"")))
        self.append(NoEscape(r"\maketitle"))
        self.preamble.append(NoEscape(r'\titlespacing{\title}{0pt}{0pt}{-30pt}'))  # Adjust spacing
        self.preamble.append(NoEscape(r'\titlespacing{\section}{0pt}{0pt}{20pt}'))  # Adjust spacing

        self.preamble.append(NoEscape(r'\usepackage[a4paper, left=0.7in, right=0.7in, top=0.2in, bottom=0.2in]{geometry}'))
        self.preamble.append(NoEscape(r'\renewcommand{\thesection}{\Roman{section}}')) # Section numbering with I, II, III, IV ...
        self.preamble.append(NoEscape(r'\usepackage{indentfirst}'))
        self.preamble.append(NoEscape(r'\usepackage{enumitem}'))
        self.preamble.append(NoEscape(r'\usepackage{fontspec}'))
        self.preamble.append(NoEscape(r'\newlist{tasks}{description}{1}'))
        self.preamble.append(NoEscape(r'\setlist[tasks]{labelindent=30pt, labelwidth=10pt, leftmargin=50pt, labelsep=10pt, font=\normalfont}'))
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
          {\parbox[t]{0.9\textwidth}}
        '''))
    def define_task_type(self, fileName):
        if os.path.basename(os.path.dirname(fileName))[0] in {"2", "3"}:
            return self.add_task
        return self.add_choose_task

    def add_task(self, fileName):
        self.answers_input_template[self.answer_index] = "input"

        with open(fileName, "r", encoding="UTF-8") as task:

            # Loads data from json file, converting it to divt (list)
            Task = json.load(task)

            # Loop through tasks and add to answers_input_template what type of answer requires the task
            for i in range(self.task_counter, self.task_counter + len(Task["data"])):
                self.answers_input_template[i] = "input"

            # Creating Section with corresponding text
            section = os.path.basename(os.path.dirname(fileName))

            with self.create(Section(NoEscape(Requirements[section] if Task["requirement"] == "" else Task["requirement"]))):

                # Adding tasks to pdf iteratively
                for i in range(0, len(Task["data"])):
                    self.append(NoEscape(r"\begin{tasks}"))
                    self.append(NoEscape(fr"\item[{self.task_counter})] \parbox[t]{{0.9\textwidth}}{{ {Task['data'][str(i + 1)]}}}"))
                    self.append(NoEscape(r"\end{tasks}"))
                    self.append(NoEscape(r"\vspace*{7pt} \par "))


                    self.task_counter += 1

    def add_choose_task(self, fileName):
        self.answers_input_template[self.answer_index] = "choose"

        with open(fileName, "r", encoding="UTF-8") as task:

            # Loads data from json file, converting it to dict (list)
            Task = json.load(task)

            # Extracting section from file path
            section = os.path.basename(os.path.dirname(fileName)) # this is correct as we should give path

            # Loop through tasks and add to answers_input_template what type of answer requires the task
            for i in range(self.task_counter, self.task_counter + len(Task["data"])):
                self.answers_input_template[i] = "choose"


            # Creating Section with corresponding text
            with self.create(Section(Requirements[section] if Task["requirement"] == "" else Task["requirement"])):

                # Loop through tasks data and iteratively adding tasks to the document
                for i in range(0, len(Task["data"])):

                    # Adding problem statement
                    #self.append(NoEscape(r"\hangindent=50pt \indent" + f"{self.task_counter})" + r"\hspace{10pt}" + r"\parbox{\dimexpr\textwidth-2em}{\raggedright}" + Task["data"][str(i+1)]["question"]))
                    self.append(NoEscape(r"\noindent\hangindent=50pt \indent" + f"{self.task_counter})" + r"\hspace{10pt}" +r"\begin{minipage}[t]{\dimexpr\textwidth-2em}\begin{flushleft}" +
                                 Task["data"][str(i + 1)]["question"] + r"\end{flushleft}\end{minipage}"))

                    self.append(NoEscape(r"\\"))
                    self.append(NoEscape(r"\\[10pt]"))

                    # Adding choose answers
                    self.append(NoEscape(r"\noindent" + Task["data"][str(i+1)]["chooses"]))
                    self.append(NoEscape(r"\\[5pt] \par"))

                    # Incrementing task_counter for correctly print next task number in document
                    self.task_counter += 1

    def get_task_answer_count(self, section):
        if section[0] == '3':
            return 6
        if section[0] == '2' and section[-1] == '8':
            return 2
        else:
            return 4


    def get_answer(self, section, task_n):
        ans = Answers[section][task_n-1]



        for i in range(0, self.get_task_answer_count(section)):

            if (isinstance(ans, int)):
                self.answers[f"{self.answer_index}"] = str(ans)[i]
                self.answer_index += 1

            if (isinstance(ans, list)):
                self.answers[f"{self.answer_index}"] = str(ans[i])
                self.answer_index += 1

        return self.answers

    def check_answer(self, user_answers):
        user_answers = json.loads(user_answers.json())
        grade = 0

        answers = user_answers["data"]

        for variant in answers:
            if answers[variant] == self.answers[variant]:
                grade += 1

        return grade

