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
│   ├── image_generation_rethink.py
│   ├── text_generation_rethink.py
│   └── model_loader.py
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


---
## Input Prompts

### Image prompt genrators

```
messages = [
    SystemMessage("""
ROLE: You are a top-tier advertising strategist specialized in crafting culturally grounded, emotionally compelling visual prompts for image generation tools.

OBJECTIVE: Generate high-impact, brand-aligned image prompts that reflect authentic product usage scenarios and resonate with the target demographic. The prompts must be optimized for the visual and emotional tone of the target platform.

TONE: Culturally authentic, emotionally resonant, visually clear, and aligned with digital platform trends.
"""),

    HumanMessage(f"""
CAMPAIGN BRIEF:
- Product: {product_info.get('product')}
- Category: {product_info.get('category')}, SKU: {product_info.get('sku')}
- Platform: {product_info.get('platform')} | Channel: {product_info.get('channel')}
- Campaign Type: {product_info.get('campaign_type')} | Category: {product_info.get('campaign_category')}
- Tone: {product_info.get('tone')}

AUDIENCE INSIGHTS:
- Region: {product_info['demographics'].get('region')}
- Age Range: {product_info['demographics'].get('age_range')}
- Gender: {', '.join(product_info['demographics'].get('gender', []))}
- Income Level: {product_info['demographics'].get('income')}
- Urban/Rural: {product_info['demographics'].get('urban_or_rural')}

PRODUCT DETAILS:
{product_details}

TASK:
Create one imaginative and visually striking image prompt that adheres to the following:

✅ CORE REQUIREMENTS:
- The product must be shown in a **realistic and culturally accurate usage scenario**.
  - E.g., laundry soap should appear in actual washing contexts: backyard wash areas, water taps, washing lines — **not in irrelevant places like living rooms or rooftops**.
- Reflect the creative instruction: **{image_prompt}**
- Include **authentic emotional cues** (e.g., pride in cleanliness, joy in daily life, family care).
- Emphasize that the **product itself must not be visually altered** — retain its original appearance.
- Ensure the visual concept is suitable for **{product_info.get('platform')}** trends and aesthetics.

🚫 AVOID:
- Illogical or trendy scenes disconnected from actual product use.
- Generic backdrops (e.g., empty streets, plain rooms) that don’t support the product narrative.
- Overly complicated or abstract imagery.

🎨 VISUAL STYLE GUIDELINES:
- Be concise and visual in your description.
- Use culturally resonant symbols, environments, and emotions.
- Favor clarity and storytelling over detail overload.
- Ensure every visual element supports the product’s purpose and message.

Make sure the image prompt helps users immediately understand **what the product is, how it’s used, and why it matters**, through a meaningful, emotionally resonant visual story.
""")
]
```

###  Text content Generators

```
messages =[ SystemMessage(f"""
ROLE:  
You are a **top-tier advertising strategist** specializing in **original, hyper-local campaigns**.

OBJECTIVE:  
Design a standout **{product_data.get('campaign_type')}** campaign for **Pwani** — promoting **{product_data.get('product')}, {product_data.get('category')}, {product_data.get('sku', 'N/A')}**.  
The campaign will target **{product_data.get('channel')}** customers via **{product_data.get('platform')}**.

PRODUCT DETAILS:
product details={product_details}

TONE & STYLE:  
The tone should be **{product_data.get('tone')}**, in line with the platform and target audience behavior.

CAMPAIGN CATEGORY:  
{product_data.get('campaign_category')}

CONTEXT:  
You will receive from the User:
- `product_details`: key benefits, unique selling points, and emotional anchors  
- `target_audience`:  
    - Region: {product_data['demographics'].get('region')}  
    - Gender: {', '.join(product_data['demographics'].get('gender', []))}  
    - Age Range: {product_data['demographics'].get('age_range')}  
    - Income Level: {product_data['demographics'].get('income')}  
    - Demographics Insights: regional, gender-specific, and locality-based behavior

IMPORTANT MUST-HAVES:

- **Output should be of type**: {product_data.get('content_type')}  
- **Language**: {product_data.get('language')}  
- **Tone**: {product_data.get('tone')}  
- **Platform-optimized**: Aligned with trends effective on **{product_data.get('platform')}**
- **Cultural relevance**: Use local references, humor, or trends that resonate with the target audience.
- **Unique selling proposition**: Highlight what makes Pwani’s product stand out.
- **Call to action**: Encourage immediate engagement or purchase.
- **Brand voice**: Reflect Pwani’s identity and values.
- **Avoid jargon**: Use clear, relatable language.
- **content_type**:{product_data.get('content_type')}


"""),
HumanMessage(text_prompt)]
```
---
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

## Recommended Guidliness for Getting the best Campaign Creative 

**1. Focus on the Product’s Unique Features**  
• Highlight the product’s key selling points.  
• Examples:  
    • “Highlight the smooth texture and rich foam of our luxury soap.”  
    • “Showcase the compact, sleek design of our wireless earbuds.”  
    • “Focus on the creamy, tropical vibe of our mango ice cream.”  
⸻  

🎨 **2. Set the Scene and Mood Clearly**  
• Describe the environment or setting you envision.  
• Examples:  
    • “Fresh morning bathroom scene for a soap ad.”  
    • “Techy, futuristic workspace for a gadget ad.”  
    • “Beachside, summer vibe for a cold drink ad.”  
⸻  

🎯 **3. Specify the Target Audience’s Lifestyle**  
• Think about who you’re selling to and what resonates with them.  
• Examples:  
    • “Designed for busy professionals on the go.”  
    • “Perfect for adventurous, outgoing Gen Z.”  
    • “Ideal for health-conscious parents.”  
⸻  

🖼️ **4. Use Strong Visual Cues**  
• Mention specific colors, objects, or themes.  
• Examples:  
    • “Bright, tropical colors for a summer campaign.”  
    • “Clean, minimalist design for premium electronics.”  
    • “Natural, earthy tones for organic products.”  
⸻  

📱 **5. Match the Creative to the Channel**  
• Consider how the ad will look on the intended platform.  
• Examples:  
    • “Vertical, eye-catching for Instagram Stories.”  
    • “Professional, polished for LinkedIn posts.”  
    • “High-contrast, direct for WhatsApp promos.”  
⸻  

💥 **6. Add Emotional Triggers (When Possible)**  
• Play on emotions that drive action.  
• Examples:  
    • “Excitement for summer flavors.”  
    • “Peace of mind for safety tech.”  
    • “Luxury feel for premium products.”  
⸻  

🛑 **7. Avoid Common Creative Pitfalls**  
• ❌ Don’t just say “Make it look good” — be specific.  
• ❌ Avoid generic words like “awesome” or “cool” without context.  
• ❌ Don’t forget the product context (e.g., size, shape, use case).  
⸻  

💡 **8. Examples for Inspiration (Clickable in UI)**  
• “Show a young couple enjoying mango ice cream on a sunny beach.”  
• “Feature a professional in a modern workspace using high-tech earbuds.”  
• “Highlight the vibrant, bubbly foam of a luxury soap bar.”

---

## 👨‍💻 Author

**Delin Shaji John**

---


# Pwanioil_endpoints
