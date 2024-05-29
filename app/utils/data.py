from langchain_core.documents import Document
import pandas as pd
import numpy as np
from typing import List


def convert_to_document(data: pd.DataFrame) -> List[Document]:
    dic = data.to_dict(orient='records')
    doc = []
    for metadata in dic:
        synopsis_prep = metadata['synopsis_prep']
        titleKo = metadata['titleKo']
        titleEn = metadata['titleEn']
        lead_role = metadata['lead_role_etd_str']
        support_role = metadata['supporting_role_etd_str']
        metadata.pop('synopsis_prep')

        page_content = f'<meta> {titleKo} {titleEn} {lead_role} {support_role} </meta>\n {synopsis_prep}'
        doc.append(Document(page_content=page_content, metadata=metadata))
    return doc


def convert_to_dataframe(movies):
    data = convert_to_dicts(movies)
    df = pd.DataFrame(data)
    df.replace('', np.nan, inplace=True)
    df_cleaned = df.dropna()
    return df_cleaned

def convert_to_dicts(movies):
    if len(movies) == 0:
        return []
    else:
        doc = []
        for movie, synopsis_prep in movies:
            #TODO or "" 제거
            movie_dic = {
                "movieId": movie.movieId,
                "titleKo": movie.titleKo or "",
                "titleEn": movie.titleEn or "",
                # "synopsis": movie.synopsis or "",
                # # "cast" : movie.cast,
                "mainPageUrl": movie.mainPageUrl or "",
                "posterUrl": movie.posterUrl or "",
                "numOfSiteRatings": movie.numOfSiteRatings or "",
                "lead_role_etd_str": synopsis_prep.lead_role_etd_str or "",
                "supporting_role_etd_str": synopsis_prep.supporting_role_etd_str or "",
                "director_etd_str": synopsis_prep.director_etd_str or "",
                "synopsis_prep": synopsis_prep.synopsis_prep[:200] # 200자만
            }
            doc.append(movie_dic)
        return doc
