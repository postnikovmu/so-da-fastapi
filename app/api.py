from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd


class Query(BaseModel):
    country: str | None = None
    languageHaveWorkedWith: str | None = None
    webframeHaveWorkedWith: str | None = None
    parameter3: str | None = None


app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173",
    'http://127.0.0.1:5173',
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

df = pd.read_csv('./data/survey_results_public.csv')


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/country/")
def country():
    countries = df.Country.unique().tolist()
    countries_str = []
    for country in countries:
        if type(country) == str:
            countries_str.append(country)

    countries_str.sort()
    return {"countries": countries_str}


@app.get("/languagehaveworkedwith/")
def languagehaveworkedwith():
    languages = df.LanguageHaveWorkedWith.unique().tolist()
    languages_str = set()
    for language in languages:
        if type(language) != str:
            continue
        one_person_languages = language.split(';')
        for one_person_language in one_person_languages:
            if type(one_person_language) == str:
                languages_str.add(one_person_language)
    languages_str_list = list(languages_str)
    languages_str_list.sort()
    return {"languagehaveworkedwith": languages_str_list}


@app.get("/webframehaveworkedwith/")
def webframehaveworkedwith():
    print('start')
    web_frames = df.WebframeHaveWorkedWith.unique().tolist()
    web_frames_str = set()
    for web_frame in web_frames:
        if type(web_frame) != str:
            continue
        one_person_web_frames = web_frame.split(';')
        for one_person_web_frame in one_person_web_frames:
            if type(one_person_web_frame) == str:
                web_frames_str.add(one_person_web_frame)
    web_frames_str_list = list(web_frames_str)
    web_frames_str_list.sort()
    print(web_frames_str_list)
    return {"webframehaveworkedwith": web_frames_str_list}


@app.post("/so-da/")
def so_da(query: Query):
    print("start")

    res_df = df.copy()
    if query.country:
        res_df = res_df[(res_df['Country'] == query.country)]
    if query.languageHaveWorkedWith:
        res_df = res_df.dropna(subset=['LanguageHaveWorkedWith'])
        res_df = res_df[(res_df['LanguageHaveWorkedWith'].str.contains(query.languageHaveWorkedWith))]
    if query.webframeHaveWorkedWith:
        res_df = res_df.dropna(subset=['WebframeHaveWorkedWith'])
        res_df = res_df[(res_df['WebframeHaveWorkedWith'].str.contains(query.webframeHaveWorkedWith))]
    print(query)
    result = len(res_df)
    print(result)
    print("finish")
    return {"Number of developers": result}
