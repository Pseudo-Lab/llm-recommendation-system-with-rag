from langchain.chains.query_constructor.base import AttributeInfo
# https://wikidocs.net/234475
metadata_field_info = [
    AttributeInfo(
        name="titleKo",
        description="한국어 영화 제목",
        type="string",
    ),
    AttributeInfo(
        name="titleEn",
        description="영어 영화 제목",
        type="integer",
    ),
    AttributeInfo(
        name="synopsis",
        description="간단한 줄거리나 개요",
        type="string",
    ),
    AttributeInfo(
        name="numOfSiteRatings",
        description="영화 평가 점수",
        type="integer",
    ),
    AttributeInfo(
        name="lead_role_etd_str",
        description="영화 주연 배우의 이름",
        type="string",
    ),
    AttributeInfo(
        name="supporting_role_etd_str",
        description="영화 조연 배우의 이름",
        type="string",
    ),
    AttributeInfo(
        name="director_etd_str",
        description="영화 감독의 이름",
        type="string"
    ),
]