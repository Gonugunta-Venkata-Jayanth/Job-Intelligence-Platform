flowchart LR
    subgraph Scraping
        A[Job Board 1] --> S1[Scraper 1]
        B[Job Board 2] --> S2[Scraper 2]
        S1 & S2 --> R[Raw Data (JSON/CSV)]
    end

    R --> E[ETL & Cleaning]
    E --> N[NLP Skill Extractor]
    N --> M[Salary Prediction Model]

    M -->|Insert/Update| DB[(PostgreSQL DB)]

    DB -->|Direct Query| BI[Power BI Report]
    DB --> API[FastAPI Backend]
    API --> ST[Streamlit App]

    ST --> User[End Users]
    BI --> User
    API --> Devs[Programmatic Users]