from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd


class Query(BaseModel):
    country: str | None = None
    languageHaveWorkedWith: str | None = None
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
    print('start')
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
    print(languages_str_list)
    return {"languagehaveworkedwith": languages_str_list}


@app.post("/so-da/")
def so_da(query: Query):
    print("start")

    res_df = df.copy()
    if query.country:
        res_df = res_df[(res_df['Country'] == query.country)]
    if query.languageHaveWorkedWith:
        res_df = res_df.dropna(subset=['LanguageHaveWorkedWith'])
        res_df = res_df[(res_df['LanguageHaveWorkedWith'].str.contains(query.languageHaveWorkedWith))]

    print(query)
    result = len(res_df)
    print(result)
    print("finish")
    return {"Number of developers": result}
