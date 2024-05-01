# llm-recommendation-system-with-rag

### Dev Run
```
docker-compose -f docker-compose.yml --env-file .env.dev up -d
```
### Dev Stop
```
docker-compose -f docker-compose.yml --env-file .env.dev down
```

### Local Run
```
main.py --env local
```


### 📖 참고 글
[Book Recommendation using Retrieval Augmented Generation][link1]
| Book title, Genres, Description 데이터로 임베딩 진행

[MovieGPT: A Gen AI Movie Recommender][link2]
| 위키피디아로 영화 데이터 활용

[Transforming Retail with RAG: The Future of Personalized Shopping][link3]
| 개인화 상품 추천 RAG with rerank

[A Real-time Retrieval System for RAG on Social Media Data][link4]
| rerank에 cross encoder 적용

[Search, Rank, and Recommendations][link5]
| 유저 데이터로 rerank 대상 추가





[link1]: <https://medium.com/@mrunmayee.dhapre/book-recommendation-using-retrieval-augmented-generation-52965b71ed16>
[link2]: <https://github.com/rafaelpierre/moviegpt/blob/main/README.md>
[link3]: <https://eduand-alvarez.medium.com/transforming-retail-with-rag-the-future-of-personalized-shopping-1ac0565d98ed>
[link4]: <https://medium.com/decodingml/a-real-time-retrieval-system-for-rag-on-social-media-data-9cc01d50a2a0>
[link5]: <https://subirverma.medium.com/search-rank-and-recommendations-35cc717772cb>
