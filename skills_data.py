# ============================================================
# SKILLS DATA  (single source of truth for all static data)
# ============================================================

skills_database = [
    "Python", "Java", "C++", "SQL", "Excel",
    "Machine Learning", "Deep Learning", "AI",
    "TensorFlow", "Keras", "PyTorch",
    "Pandas", "NumPy", "Scikit-learn", "Matplotlib", "Statistics",
    "NLP", "Natural Language Processing", "Transformers", "LLM",
    "Generative AI", "RAG", "LangChain", "Vector Database",
    "Embeddings", "Semantic Search",
    "Git", "GitHub", "Docker",
    "FastAPI", "Flask", "REST API", "Streamlit",
    "OpenCV", "YOLO", "CNN", "RNN", "LSTM", "Computer Vision",
    "HTML", "CSS", "JavaScript", "React",
    "AWS", "Azure", "Google Cloud", "Power BI",
]


skill_aliases = {
    "python": "Python",

    "ml": "Machine Learning",
    "machine learning": "Machine Learning",
    "machine-learning": "Machine Learning",

    "dl": "Deep Learning",
    "deep learning": "Deep Learning",

    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",

    "keras": "Keras",

    "torch": "PyTorch",
    "pytorch": "PyTorch",

    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",

    "np": "NumPy",
    "numpy": "NumPy",

    "pd": "Pandas",
    "pandas": "Pandas",

    "nlp": "NLP",
    "natural language processing": "Natural Language Processing",

    "llm": "LLM",
    "llms": "LLM",
    "large language model": "LLM",
    "large language models": "LLM",

    "genai": "Generative AI",
    "generative ai": "Generative AI",

    "rag": "RAG",
    "langchain": "LangChain",

    "vector db": "Vector Database",
    "vector database": "Vector Database",

    "embeddings": "Embeddings",
    "embedding": "Embeddings",

    "semantic search": "Semantic Search",

    "git": "Git",
    "github": "GitHub",
    "docker": "Docker",

    "fastapi": "FastAPI",
    "fast api": "FastAPI",
    "flask": "Flask",

    "rest api": "REST API",
    "restful api": "REST API",
    "api": "REST API",

    "opencv": "OpenCV",
    "yolo": "YOLO",
    "cnn": "CNN",
    "rnn": "RNN",
    "lstm": "LSTM",
    "computer vision": "Computer Vision",

    "sql": "SQL",
    "excel": "Excel",
    "power bi": "Power BI",

    "aws": "AWS",
    "azure": "Azure",
    "google cloud": "Google Cloud",
}


role_learning_order = {
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning", "TensorFlow", "NLP",
        "Transformers", "LLM", "RAG", "Vector Database", "FastAPI",
        "Docker", "Git",
    ],
    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Pandas", "NumPy", "Scikit-learn",
        "SQL", "Statistics", "TensorFlow", "Git",
    ],
    "Data Scientist": [
        "Python", "SQL", "Pandas", "NumPy", "Machine Learning",
        "Statistics", "Scikit-learn", "Matplotlib",
    ],
    "Deep Learning Engineer": [
        "Python", "Deep Learning", "TensorFlow", "PyTorch", "CNN", "RNN",
        "LSTM", "Computer Vision", "Git",
    ],
    "NLP Engineer": [
        "Python", "NLP", "Natural Language Processing", "Transformers",
        "LLM", "PyTorch", "TensorFlow",
    ],
    "Generative AI Engineer": [
        "Python", "LLM", "Generative AI", "RAG", "LangChain",
        "Vector Database", "Embeddings", "FastAPI", "Docker",
    ],
    "Data Analyst": [
        "Python", "SQL", "Pandas", "Excel", "Statistics", "Matplotlib",
        "Power BI",
    ],
    "Computer Vision Engineer": [
        "Python", "OpenCV", "YOLO", "Deep Learning", "TensorFlow",
        "PyTorch", "CNN", "Computer Vision",
    ],
    "Backend AI Engineer": [
        "Python", "FastAPI", "Flask", "REST API", "Docker", "Git", "SQL",
        "Machine Learning",
    ],
    "AI/ML Intern": [
        "Python", "SQL", "Machine Learning", "Pandas", "Scikit-learn", "Git",
    ],
}


learning_information = {
    "Python": "Learn Python syntax, functions, OOP, modules and problem solving.",
    "Machine Learning": "Learn supervised learning, unsupervised learning, evaluation and model selection.",
    "Deep Learning": "Learn neural networks, CNNs, RNNs, LSTMs and deep learning workflows.",
    "TensorFlow": "Learn model building, training, evaluation and deployment with TensorFlow.",
    "NLP": "Learn text preprocessing, tokenization, text classification and language processing.",
    "Transformers": "Learn attention, transformer architecture and modern NLP models.",
    "LLM": "Learn large language models, prompting, embeddings and LLM applications.",
    "RAG": "Learn retrieval augmented generation and grounding LLM responses in external knowledge.",
    "Vector Database": "Learn vector storage, similarity search and semantic retrieval.",
    "FastAPI": "Learn how to build production-ready Python APIs.",
    "Docker": "Learn containerization and deployment.",
    "Git": "Learn version control, branches, commits and collaboration.",
    "SQL": "Learn databases, queries, joins, aggregation and data analysis.",
    "Pandas": "Learn data cleaning, transformation and analysis.",
    "NumPy": "Learn numerical computing and array operations.",
    "Scikit-learn": "Learn practical machine learning implementation.",
    "Statistics": "Learn descriptive statistics, probability and statistical testing.",
    "PyTorch": "Learn deep learning development using PyTorch.",
    "CNN": "Learn convolutional neural networks for image understanding.",
    "RNN": "Learn recurrent neural networks for sequence data.",
    "LSTM": "Learn long short-term memory networks.",
    "Computer Vision": "Learn image processing and visual AI.",
    "OpenCV": "Learn computer vision operations and image/video processing.",
    "YOLO": "Learn real-time object detection.",
    "LangChain": "Learn LLM application orchestration and retrieval pipelines.",
    "Embeddings": "Learn numerical representations of text for semantic similarity.",
    "Semantic Search": "Learn meaning-based search using embeddings.",
    "GitHub": "Learn repository management and professional project presentation.",
}