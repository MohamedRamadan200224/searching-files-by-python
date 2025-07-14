# 📚 Text Processing Pipeline with Advanced Indexing

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)

A sophisticated text processing pipeline that builds search indexes and implements TF-IDF with cosine normalization for information retrieval.

## 🌟 Features

### 🗂️ Text Loading & Tokenization
```python
- Reads all text files from `/files` directory (naturally sorted)
- Tokenizes using NLTK's `word_tokenize()`
- Custom stopword removal (preserves "where", "in", "to")
- Output: List of documents (each document = list of words)
