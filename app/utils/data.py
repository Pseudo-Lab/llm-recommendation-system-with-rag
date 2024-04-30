def convert_to_dicts(movies):
    metadatas = []
    texts = []
    for movie, synopsis_prep in movies:
        movie_dic = {
            "movieId" : movie.movieId,
            "titleKo" : movie.titleKo or "",
            "titleEn" : movie.titleEn or "",
            "synopsis" : movie.synopsis or "",
            # # "cast" : movie.cast,
            "mainPageUrl" : movie.mainPageUrl or "",
            "posterUrl" : movie.posterUrl or "",
            "numOfSiteRatings" : movie.numOfSiteRatings or "",
            "lead_role_etd_str" : synopsis_prep.lead_role_etd_str or "",
            "supporting_role_etd_str" : synopsis_prep.supporting_role_etd_str or "",
            "director_etd_str" : synopsis_prep.director_etd_str or ""
        }
        metadatas.append(movie_dic)
        texts.append(synopsis_prep.synopsis_prep)
    return metadatas, texts