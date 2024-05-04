from langchain.chains.query_constructor.base import AttributeInfo
# https://wikidocs.net/234475

# metadata_field_info = [
#     AttributeInfo(
#         name="titleKo",
#         description="Title of the movie in korean",
#         type="string",
#     ),
#     AttributeInfo(
#         name="titleEn",
#         description="Title of the movie in English",
#         type="integer",
#     ),
#     AttributeInfo(
#         name="synopsis",
#         description="A brief summary outlining the main events, characters, and plot points, providing a quick overview of the film's storyline",
#         type="string",
#     ),
#     AttributeInfo(
#         name="numOfSiteRatings",
#         description="A rating for the movie",
#         type="string",
#     ),
#     AttributeInfo(
#         name="lead_role_etd_str",
#         description="A central role in the production",
#         type="integer",
#     ),
#     AttributeInfo(
#         name="supporting_role_etd_str",
#         description="A supporting actor/actress, also known as a 'supporting actor/actress,' plays a significant role in a production",
#         type="string",
#     ),
#     AttributeInfo(
#         name="director_etd_str",
#         description="Director of the movie",
#         type="string"
#     ),
# ]


metadata_field_info = [
    AttributeInfo(
        name="titleKo",
        description="한국어 영화 이름",
        type="string",
    ),
    AttributeInfo(
        name="titleEn",
        description="영어 영화 이름",
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
        type="string",
    ),
    AttributeInfo(
        name="lead_role_etd_str",
        description="영화 주연 배우의 이름",
        type="integer",
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