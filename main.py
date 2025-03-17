
import random, uuid
from Functions import *
import Data
from TestClass import Test
from fastapi import FastAPI
from pylatex import Command, Document, Section, Subsection
from pylatex.utils import NoEscape, italic
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse


app = FastAPI()

app.mount("/pdfs", StaticFiles(directory="./Tests"), name="pdfs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/pdf")
async def root():
    Sections = Data.Faculties["manual"]

    Count = [Data.Database[sec] for sec in Sections]

    Randoms = [random.randint(1, Count[Sections.index(sec)]) for sec in Sections]

    Tasks = list(zip(Sections, Randoms))

    pdf = Test()

    for section, task_n in Tasks:
        file = f"./Texts/{section}/{section}-{task_n}.json"

        pdf.define_task_type(file)(file)

    path_for_test = f"./Tests/{uuid.uuid4()}-math_test"

    pdf.generate_pdf(path_for_test, compiler="xelatex", clean_tex=True)

    # # Convert relative path to absolute
    # pdf_path = os.path.abspath(path_for_test)

    return {
        "task-count": pdf.task_counter-1,
        "pdf-path": f"{path_for_test}.pdf"
    }

    #return FileResponse(path=pdf_path, media_type="application/pdf", filename="Math_test.pdf")

@app.get("/pdf/{filename:path}")
async def pdf(filename: str):
    return FileResponse(path=filename, media_type="application/pdf")