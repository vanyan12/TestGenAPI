
import Data
import random
from Answers import Answers
from Functions import *
from TestClass import Test
from fastapi import FastAPI
from pylatex import Command, Document, Section, Subsection
from pylatex.utils import NoEscape, italic
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    Sections = Data.Faculties["manual"]

    Count = [Data.Database[sec] for sec in Sections]

    Randoms = [random.randint(1, Count[Sections.index(sec)]) for sec in Sections]

    Tasks = list(zip(Sections, Randoms))

    pdf = Test()

    for section, task_n in Tasks:
        file = f"./Texts/{section}/{section}-{task_n}.json"

        pdf.define_task_type(file)(file)

    pdf.generate_pdf("Math_test", compiler="xelatex", clean_tex=True)

    return FileResponse(path="./Math_test.pdf", media_type="application/pdf", filename="Math_test.pdf")








