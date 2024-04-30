from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, text, ForeignKey, Text, UUID
from sqlalchemy.orm import relationship
from app.database.database import Base


class DaumMovie(Base):
    __tablename__ = 'daum_movies'

    movieId = Column(Integer, primary_key=True, autoincrement=True)
    titleKo = Column(String(100), default=None)
    titleEn = Column(String(100), default=None)
    synopsis = Column(Text)
    cast = Column(String(10000), default=None)
    mainPageUrl = Column(Text)
    posterUrl = Column(Text)
    numOfSiteRatings = Column(Integer, default=None)

    synopsis_prep = relationship("DaumMovieSynopsisPrep", back_populates="daum_movie")

    def __repr__(self):
        return (f"<DaumMovie(movieId={self.movieId}, "
                f"titleKo={self.titleKo}, "
                f"titleEn={self.titleEn}, "
                f"synopsis={self.synopsis}, "
                f"cast={self.cast}, "
                f"mainPageUrl={self.mainPageUrl}, "
                f"posterUrl={self.posterUrl}, "
                f"numOfSiteRatings={self.numOfSiteRatings})>")

    def __init__(self, titleKo=None, titleEn=None, synopsis=None, cast=None, mainPageUrl=None, posterUrl=None,
                 numOfSiteRatings=None):
        self.titleKo = titleKo
        self.titleEn = titleEn
        self.synopsis = synopsis
        self.cast = cast
        self.mainPageUrl = mainPageUrl
        self.posterUrl = posterUrl
        self.numOfSiteRatings = numOfSiteRatings


class DaumMovieSynopsisPrep(Base):
    __tablename__ = 'daum_movies_synopsis_prep'

    movieId = Column(Integer, ForeignKey('daum_movies.movieId'), primary_key=True)
    synopsis_prep = Column(Text)
    lead_role_etd_str = Column(Text)
    supporting_role_etd_str = Column(Text)
    director_etd_str = Column(Text)
    daum_movie = relationship("DaumMovie", back_populates="synopsis_prep")

    def __repr__(self):
        return f"<DaumMovieSynopsisPrep(movieId={self.movieId}, " \
               f"synopsis_prep={self.synopsis_prep}), " \
               f"lead_role_etd_str={self.lead_role_etd_str}," \
               f"supporting_role_etd_str={self.supporting_role_etd_str}," \
               f"director_etd_str={self.director_etd_str}>"

    def __init__(self, movieId, synopsis_prep, lead_role_etd_str, supporting_role_etd_str, director_etd_str):
        self.movieId = movieId
        self.synopsis_prep = synopsis_prep
        self.lead_role_etd_str = lead_role_etd_str
        self.supporting_role_etd_str = supporting_role_etd_str
        self.director_etd_str = director_etd_str


class Workspace(Base):
    __tablename__ = "workspace"

    id = Column(String(36), primary_key=True)
    vector_path = Column(String(100), nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    updated_time = Column(TIMESTAMP(timezone=True), server_default=text('now()'), onupdate=text('now()'))

    def __repr__(self):
        return f"<Workspace(id={self.id}, vector_path={self.vector_path}, created_time={self.created_time}, updated_time={self.updated_time})>"

    def __init__(self, id, vector_path, created_time=None, updated_time=None):
        self.id = id
        self.vector_path = vector_path
        self.created_time = created_time
        self.updated_time = updated_time
