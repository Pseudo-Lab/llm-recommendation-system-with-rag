from langchain_core.documents import Document


def convert_to_dicts(movies):
    if len(movies) == 0:
        return []
    else:
        doc = []
        for movie, synopsis_prep in movies[0:100]:
            movie_dic = {
                "movieId": movie.movieId,
                "titleKo": movie.titleKo or "",
                "titleEn": movie.titleEn or "",
                "synopsis": movie.synopsis or "",
                # # "cast" : movie.cast,
                "mainPageUrl": movie.mainPageUrl or "",
                "posterUrl": movie.posterUrl or "",
                "numOfSiteRatings": movie.numOfSiteRatings or "",
                "lead_role_etd_str": synopsis_prep.lead_role_etd_str or "",
                "supporting_role_etd_str": synopsis_prep.supporting_role_etd_str or "",
                "director_etd_str": synopsis_prep.director_etd_str or ""
            }
            doc.append(Document(page_content=synopsis_prep.synopsis_prep, metadata=movie_dic))
        return doc
