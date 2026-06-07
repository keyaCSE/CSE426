import gradio as gr
import pandas as pd
import json, re, math, time, ast
from collections import defaultdict
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

STOPWORDS = {
    'the','is','a','an','and','or','of','to','in','for','with','on','by','this',
    'that','it','as','at','from','be','are','was','were','will','you','your'
}

def preprocess(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()
    return [stemmer.stem(word) for word in tokens if word not in STOPWORDS]

df = pd.read_csv("processed_products.csv")

with open("inverted_index.json", "r") as f:
    raw_index = json.load(f)

inverted_index = defaultdict(dict)
for term, docs in raw_index.items():
    for doc_id, data in docs.items():
        inverted_index[term][int(doc_id)] = data

N = len(df)

def get_docs_for_term(term):
    term = stemmer.stem(str(term).lower())
    return set(inverted_index.get(term, {}).keys())

def boolean_search(query):
    query = query.lower().strip()

    if " and " in query:
        terms = query.split(" and ")
        result = get_docs_for_term(terms[0])
        for term in terms[1:]:
            result = result.intersection(get_docs_for_term(term))
        return result

    elif " or " in query:
        terms = query.split(" or ")
        result = set()
        for term in terms:
            result = result.union(get_docs_for_term(term))
        return result

    else:
        terms = preprocess(query)
        if not terms:
            return set()

        result = get_docs_for_term(terms[0])
        for term in terms[1:]:
            result = result.intersection(get_docs_for_term(term))
        return result

def calculate_score(query, doc_id):
    query_terms = preprocess(query)
    score = 0

    for term in query_terms:
        if term in inverted_index and doc_id in inverted_index[term]:
            tf = inverted_index[term][doc_id]["frequency"]
            df_term = len(inverted_index[term])
            idf = math.log((N + 1) / (df_term + 1)) + 1
            score += tf * idf

    return score

def highlight(text, query):
    text = str(text)
    query_terms = query.lower().replace(" and ", " ").replace(" or ", " ").split()

    for term in query_terms:
        text = re.sub(
            f"({re.escape(term)})",
            r"<mark>\1</mark>",
            text,
            flags=re.IGNORECASE
        )
    return text

def get_first_image(image_value):
    try:
        images = ast.literal_eval(str(image_value))
        if isinstance(images, list) and len(images) > 0:
            return images[0]
    except:
        pass
    return ""

def search_products(query, top_k):
    start_time = time.time()

    if query.strip() == "":
        return "<h3>Please enter a search query.</h3>"

    matched_docs = boolean_search(query)

    ranked = []
    for doc_id in matched_docs:
        score = calculate_score(query, doc_id)
        ranked.append((doc_id, score))

    ranked = sorted(ranked, key=lambda x: x[1], reverse=True)
    search_time = round(time.time() - start_time, 4)

    if not ranked:
        return f"<h3>No result found for: {query}</h3><p>Try another keyword.</p>"

    html = f"""
    <div style="font-family: Arial;">
        <p style="color:gray;">Found {len(ranked)} results in {search_time} seconds</p>
    """

    for doc_id, score in ranked[:top_k]:
        row = df.iloc[doc_id]

        title = highlight(row.get("product_name", ""), query)
        desc = highlight(str(row.get("description", ""))[:280], query)
        image_url = get_first_image(row.get("image", ""))
        product_url = row.get("product_url", "#")

        image_html = ""
        if image_url:
            image_html = f"""
            <img src="{image_url}" 
                 style="width:120px; height:120px; object-fit:contain; border:1px solid #eee; border-radius:8px; margin-right:18px;">
            """

        html += f"""
        <div style="
            display:flex;
            gap:18px;
            border:1px solid #ddd;
            padding:18px;
            margin:15px 0;
            border-radius:12px;
            background:white;
        ">
            <div>{image_html}</div>

            <div style="flex:1;">
                <h3 style="color:#1a0dab; margin-bottom:8px;">{title}</h3>
                <p><b>Brand:</b> {row.get("brand", "")}</p>
                <p>
                    <b>Retail Price:</b> ₹{row.get("retail_price", "")}
                    |
                    <b>Discounted Price:</b> ₹{row.get("discounted_price", "")}
                </p>
                <p><b>TF-IDF Score:</b> {round(score, 4)}</p>
                <p>{desc}...</p>
                <a href="{product_url}" target="_blank"
                   style="display:inline-block; padding:8px 14px; background:#1a73e8; color:white; text-decoration:none; border-radius:6px;">
                   View Product
                </a>
            </div>
        </div>
        """

    html += "</div>"
    return html

css = """
.gradio-container {
    max-width: 980px !important;
    margin: auto !important;
}
h1 {
    text-align: center;
}
"""

with gr.Blocks(css=css, title="E-Commerce Search Engine") as demo:
    gr.HTML("""
    <h1>🛒 ShopSearch</h1>
    <p style="text-align:center; color:gray;">
    E-Commerce Product Search Engine using Custom Inverted Index and TF-IDF Ranking
    </p>
    """)

    query = gr.Textbox(
        label="Search Product",
        placeholder="Search for samsung phone, shoes or watch..."
    )

    top_k = gr.Dropdown(
        choices=[5, 10, 20, 50],
        value=10,
        label="Number of Results"
    )

    search_btn = gr.Button("Search")
    output = gr.HTML()

    search_btn.click(
        fn=search_products,
        inputs=[query, top_k],
        outputs=output
    )

demo.launch()
