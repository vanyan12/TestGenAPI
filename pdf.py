import Data
import random
import re
from Answers import Answers
from PIL import Image
from fpdf import FPDF
import datetime


# Functions ==========================================================
def get_height(path):
    return Image.open(path).height // 30

def vect_add(x, y):
    return x[0] + y[0], x[1] + y[1]


def current():
    return pdf.get_x(), pdf.get_y()

def source(sec, rand):
    return f"Pictures/{sec}/{sec}-{rand}.png"

def space_check(sec, rand):
    path = source(sec, rand)
    y = current()[1] + get_height(path)
    return True if y - 28 > 0 else False

def remove_dub(list):
    result = []
    for elem in list:
        if elem not in result:
            result.append(elem)
    return result

def task_freq(randoms):
    sections,o = zip(*randoms)
    keys = remove_dub(sections)
    values = []
    for sec in keys:
        for elem in randoms:
            if elem[0] == sec:
                values.append(elem[1])
    return dict(zip(keys, values))

def get_random_for_sec(sec):
    global randoms
    return [randoms[i][1] for i in range(0, len(randoms)) if randoms[i][0] == sec][0]

def T_F_to_str(str):
    return "Ճիշտ" if str == "1" else "Սխալ"

def str_for_table(answer):
    if str(type(answer)) == "<class 'int'>":
        answer = str(answer)
        return " ".join(f"{char}," for char in answer)[:-1]
    elif str(type(answer) == "<class 'list'>"):
        answer = re.sub(r"[\[\], ]", '', str(answer)) if len(answer) == 6 else re.sub(r"[\[\]]", '', str(answer))
        return answer

# ============================================================
global randoms

def generate_test(fac):

    #Choosing corresponding max counts of sections and Generating random numbers for them ==========================================
    Sections = Data.Faculties['IMA'] if fac == 'IMA' else (Data.Faculties['KFM'][random.randint(0,len(Data.Faculties['KFM'])-1)] if fac == 'KFM' else Data.Faculties['manual'])

    Count = [Data.Database[sec] for sec in Sections]

    Tasks = list(zip(Sections, Count))

    global randoms
    randoms = list(zip(Sections, [random.randint(1, Count[Sections.index(sec)]) for sec in Sections]))
    print(randoms)
    Data.Task = randoms[:]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


    global pdf
    # Making pdf and adding configs =====================
    pdf = FPDF("P", "cm", "A4")
    pdf.set_creator("Van")
    pdf.add_page()
    pdf.set_margin(1)
    pdf.add_font("Mariam", '', r'C:\Users\van\Desktop\Server\GHEAMariamBld.ttf')
    pdf.set_font("Mariam", '', 18)

    # Adding title ===========================================
    pdf.cell(0, 1, "Թեստ", 0, align="C")
    pdf.set_xy(1, current()[1] + 2)

    # Adding tasks =========================================

    # Creating iters for checking next whether next image will be contained in the current page ==========
    section, o = zip(*Tasks)
    section1, o = zip(*Tasks)
    section1 = iter(section1)
    o, section2 = zip(*randoms)
    section2 = iter(section2)
    task_numbering = iter((i for i in range(1, len(section)+1)))

    for sec in section:
        global rand_self

        # Check whether there is need to add page ================

        if space_check(next(section1, 0), next(section2, 0)):
            pdf.add_page()
            pdf.set_margin(1)

        # Writing task number ==========================================

        pdf.cell(0, 1, f"[{next(task_numbering)}]", 0, align="C")
        pdf.set_xy(1, pdf.get_y() + 1)

        # Adding image ================================================
        pdf.image(source(sec, get_random_for_sec(sec)), current()[0], current()[1], pdf.epw)


        # Changing position =============================================
        margin = (0, get_height(source(sec, get_random_for_sec(sec))) + 1)
        pdf.set_xy(vect_add(current(), margin)[0], vect_add(current(), margin)[1])

        randoms.pop(0)



    file_name = f"./Files/Math_test_{fac}_{timestamp}.pdf" if fac == "IMA" or fac == "KFM" else f"./Files/Math_test_{timestamp}.pdf"
    pdf.output(file_name)

# def generate_answer():


    answer = FPDF("P", "cm", "A4")
    answer.add_page()
    answer.set_auto_page_break(True)
    answer.add_font("Mariam", 'B', r'C:\Users\van\Desktop\Server\GHEAMariamBld.ttf')
    answer.add_font("Mariam_B", 'B', r'C:\Users\van\Desktop\Server\GHEAMariamBld.ttf')

    sections, task_nums = zip(*Data.Task)


    TABLE_COLS = ("№", "Պատասխաններ")
    TABLE_DATA = []

    for i in range(0, len(Data.Task)):
        if sections[i][:1] == "3":
            for k in range(0,6):
                TABLE_DATA.append((f"{i+1}-{k+1}", T_F_to_str(str_for_table(Answers[sections[i]][task_nums[i]-1])[k])))
        else:
            TABLE_DATA.append((str(i+1), str_for_table(Answers[sections[i]][task_nums[i]-1])))

    TABLE_DATA.insert(0,TABLE_COLS)

    TABLE_DATA = tuple(TABLE_DATA)


    with answer.table(width=13, col_widths=(4,9), padding=(0,1), text_align=("CENTER", "LEFT")) as table:
        for row in TABLE_DATA:
            answer.set_font("Mariam", "B", 16)

            line = table.row()
            for data in row:
                if data == "№" or data == "Պատասխաններ":
                    answer.set_font("Mariam_B", "B", 16)
                line.cell(data)

    answer.output(f"./Files/Answers_{timestamp}.pdf")
    return timestamp


