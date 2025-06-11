
Database = {
    'Section1': 8,#37
    'Section7': 8,#20,
    'Section3': 7,#63,
    'Section4': 8,#49,
    'Section10': 7,#26,
    'Section6': 3,#23,
    'Section5': 3,#45, #66 task but there is not answers
    'Section2': 4,#73,
    'Section8': 4,#68,
    'Section9': 2,#23,
    '2Section8': 10, #86,
    '2Section1': 18,#43
    '2Section3': 10,#19
    '2Section2': 10,#19
    '2Section6': 10,#43,
    '2Section7': 10, #29,
    '2Section4': 10,#23,
    '2Section5': 10,#35,
    '3Section1': 1,#46,
    '3Section4': 1,#16,
    '3Section2': 1,#77
}


Faculties = {
    "IMA": [['Section1', 'Section7', 'Section3', 'Section4', 'Section9', 'Section6', 'Section5', 'Section2', 'Section8','3Section4',
             '2Section8', '2Section1', '2Section3', '2Section2', '2Section6', '2Section4', '2Section5', '3Section2', '3Section1'],

            ['Section1', 'Section2', 'Section3', 'Section4', 'Section5', 'Section6', 'Section9', 'Section8', 'Section7', '3Section4',
             '2Section8', '2Section1', '2Section5', '2Section4', '2Section6', '2Section2', '2Section3', '3Section2', '3Section1']],

    "KFM": [['Section1', '3Section4', 'Section3', 'Section5', 'Section7', 'Section4', 'Section10',
             '2Section5', '2Section1', '2Section2', '2Section4', "2Section3", "2Section6", "2Section3", "3Section2", "3Section1"],

            ['3Section4', 'Section2', 'Section3', 'Section4', 'Section10', 'Section5','Section7',
             '2Section4', '2Section3', '2Section2', '2Section6', '2Section5', '2Section3', '2Section1', '3Section2', '3Section1']],

    "manual": ["Section1", "2Section3", "2Section4",  "2Section5", "2Section6", "2Section7", "2Section8",
               "2Section2", "2Section3", "2Section4",  "2Section5", "2Section6", "2Section7", "2Section8",
               "2Section2", "2Section3", "2Section4",  "2Section5", "2Section6", "2Section7", "2Section8", "2Section8"]
}

Requirements = {
    'Section1': "Կատարել առաջադրանքները",
    'Section2': "Գտնել արտահայտության արժեքը",
    'Section3': "",
    'Section4': "Լուծել անհավասարումը",
    'Section5': "",
    'Section6': "Կատարել առաջադրանքները",
    'Section7': "",
    'Section8': "",
    'Section9': "",
    'Section10': "",
    '2Section1': "Գտնել արտահայտության արժեքը",
    '2Section2': "",
    '2Section3': "",
    '2Section4': "Կատարել առաջադրանքները",
    '2Section5': "",
    '2Section6': "Կատարել առաջադրանքները",
    '2Section7': "",
    '2Section8': "Կատարել առաջադրանքները",
    '3Section1': "",
    '3Section2': "",
    '3Section3': ""
}

# For helper function in TestClass.py
four = ["Section1", "Section2", "Section3", "Section4", "Section5", "Section6", "Section7", "Section8", "Section9",
        "Section10",
        "2Section1", "2Section2", "2Section3", "2Section4", "2Section5", "2Section6", "2Section7"]

six = ["3Section1", "3Section2", "3Section4"]

options = {}

for sec in four:
    options[sec] = 4
for sec in six:
    options[sec] = 6
options["2Section8"] = 2



