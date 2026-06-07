# CSE426
E-Commerce Product Search Engine using Custom Inverted Index, Boolean Query Processing, TF-IDF Ranking, and Hugging Face Deployment.

# E-Commerce Product Search Engine

## Project Overview

This project is a specialized E-Commerce Product Search Engine developed using Information Retrieval techniques. The system is built from scratch using a custom Inverted Index and TF-IDF ranking algorithm without relying on pre-built search engine frameworks such as Elasticsearch or Whoosh.

The search engine efficiently retrieves and ranks products based on user queries and provides a clean web-based interface for searching products from a large e-commerce dataset.

---

## Features

* Custom Inverted Index Implementation
* Keyword Search
* Multi-word Query Search
* Boolean Query Processing (AND / OR)
* TF-IDF Ranking
* Product Information Retrieval
* Product Image Display
* Product URL Integration
* Keyword Highlighting
* Web-Based User Interface
* Online Deployment using Hugging Face Spaces

---

## Dataset

This project uses the Flipkart E-Commerce Product Dataset.

The dataset contains:

* Product Name
* Product Description
* Brand Name
* Retail Price
* Discounted Price
* Product URL
* Product Image URL

---

## Technologies Used

* Python
* Pandas
* NumPy
* NLTK
* JSON
* Gradio
* Hugging Face Spaces

---

## Project Workflow

Dataset

↓

Text Preprocessing

↓

Inverted Index Construction

↓

Query Processing

↓

TF-IDF Ranking

↓

Result Retrieval

↓

Web Interface

---

## Supported Search Queries

### Single Keyword Search

Example:

```text
samsung
```

### Multi-word Search

Example:

```text
samsung phone
```

### Boolean AND Query

Example:

```text
samsung AND phone
```

### Boolean OR Query

Example:

```text
watch OR shoes
```

---

## Ranking Method

The search engine ranks retrieved products using the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm.

This approach prioritizes more relevant products by assigning higher scores to important terms within the dataset.

---

## Web Interface Features

* Search Box
* Search Result Count
* TF-IDF Score Display
* Product Information Cards
* Product Image Support
* View Product Button
* Highlighted Search Keywords

---

## Live Demo

Hugging Face Deployment:

https://keyacse-shopsearch-engine.hf.space

---

## Repository Structure

```text
ECommerce-Search-Engine/
│
├── search_engine.ipynb
├── app.py
├── requirements.txt
├── README.md
└── Report.pdf
```

---

## Note

Due to GitHub file size limitations, large generated files such as:

* processed_products.csv
* inverted_index.json

are not included in this repository.

The complete working application can be accessed through the deployed Hugging Face Space provided above.

---

## Author

**Yeasmin Kabir Keya**

Department of Computer Science and Engineering (CSE)

University of Information Technology and Sciences (UITS)

---

## Conclusion

This project demonstrates the practical implementation of Information Retrieval concepts through the development of an E-Commerce Product Search Engine using a custom Inverted Index and TF-IDF ranking mechanism. The system efficiently retrieves and ranks relevant products while providing a user-friendly web-based search experience.
