MOVIE_DATA_SOURCE = """\
```json
{{
    "content": "Description of a movie",
    "attributes": {{
        "titleKo": {{
            "type": "string",
            "description": "한국어 영화 제목"
        }},
        "titleEn": {{
            "type": "integer",
            "description": "영어 영화 제목"
        }},
        "synopsis": {{
            "type": "string",
            "description": "간단한 줄거리나 개요"
        }},
        "numOfSiteRatings": {{
            "type": "integer",
            "description": "영화 평가 점수"
        }},
        "lead_role_etd_str": {{
            "type": "string",
            "description": "영화 주연 배우의 이름"
        }},
        "supporting_role_etd_str": {{
            "type": "string",
            "description": "영화 조연 배우의 이름"
        }},
        "director_etd_str": {{
            "type": "string",
            "description": "영화 감독의 이름"
        }}
    }}
}}
```\
"""

MOVIE_NO_FILTER_ANSWER = """\
```json
{{
    "query": "",
    "filter": "NO_FILTER"
}}
```\
"""

MOVIE_FULL_ANSWER = """\
```json
{{
    "query": "멜로 감성",
    "filter": "and(or(like(\\"lead_role_etd_str\\", \\"장동건\\"), like(\\"supporting_role_etd_str\\", \\"장동건\\")))"
}}
```\
"""

MOVIE_DIRECTOR_ANSWER = """\
```json
{{
    "query": "",
    "filter": "like(\\"director_etd_str\\", \\"봉준호\\")"
}}
```\
"""

MOVIE_DEFAULT_EXAMPLES = [
    {
        "i": 1,
        "data_source": MOVIE_DATA_SOURCE,
        "user_query": "장동건이 출연하는 멜로 감성의 영화를 추천해줘",
        "structured_request": MOVIE_FULL_ANSWER,
    },
    {
        "i": 2,
        "data_source": MOVIE_DATA_SOURCE,
        "user_query": "봉준호 감독의 영화가 뭐가 있어?",
        "structured_request": MOVIE_DIRECTOR_ANSWER,
    },
    {
        "i": 3,
        "data_source": MOVIE_DATA_SOURCE,
        "user_query": "오늘의 날씨는 뭐야?",
        "structured_request": MOVIE_NO_FILTER_ANSWER,
    },
]