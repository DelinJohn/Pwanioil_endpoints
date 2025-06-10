# 🧠 AI-Powered Content Generation Platform

This is a modular, full-stack AI content generation system for generating marketing assets using LLMs and image models. It supports text, image, and hybrid output generation using FastAPI as the backend and Streamlit for testing endpoints interactively.

---

## 📁 Project Structure

```
.
├── __databases/              # Storage: MongoDB, TinyDB, and sample JSON data
│   ├── *.json
│   └── *.db
├── __data_loaders/           # Data access layer
│   ├── __init__.py
│   ├── json_reader.py
│   ├── Mongoclient.py
│   └── Tiny_dbaccess.py
├── __image_data/             # Sample image data used in prompts
│   └── *.png
├── __llm/                    # LLM and image generation logic
│   ├── __init__.py
│   ├── image_generation.py
│   ├── text_generation.py
│   └── model_loader.py
├── __Output_structure/       # Output formatting before returning from endpoints
│   ├── __init__.py
│   └── Output_formatter.py
├── __Utils/                  # Utility functions and API routing
│   ├── __init__.py
│   ├── helper.py             # Base64 conversion, input normalizing, etc.
│   ├── logger.py             # Logging setup (TBD)
│   └── routes.py             # All FastAPI endpoints
├── .env                      # Environment configuration file
├── config.py                 # Config loader for .env
├── main.py                   # Application entry point (runs FastAPI)
├── requirements.txt          # Python dependencies
├── .gitignore
└── test.py                   # Streamlit interface to test endpoints
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Set Up Environment

Install dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Create a `.env` file (or modify the existing one):

```ini
MONGO_URI=your_mongo_uri
GPT_model=model
GPT_model_provider=model_provider
API_KEY=your_api_key
```

### 3. Run the FastAPI Server

```bash
uvicorn main:app --reload
```

Access the API docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4. Test with Streamlit

Run:

```bash
streamlit run test.py
```

---

## ✨ Features

- ✅ **Text, Image, and Hybrid Generation** via LLMs
- 📦 Modular architecture (LLMs, formatting, routing, utils separated)
- 🧩 Works with MongoDB and TinyDB
- 🌐 RESTful API using FastAPI
- 🧪 Built-in Streamlit test interface

---



---

## 👨‍💻 Author

**Delin Shaji John**

---


# Pwanioil_endpoints
