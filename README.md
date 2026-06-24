# SkinSmart
<h1 align="center">🧴 Facial Skincare Recommendation System</h1>
<h3 align="center">A Hybrid Machine Learning Approach using KNN, CNN & EfficientNet-B0</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
  <img src="https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Validation%20Accuracy-80%25-success?style=flat-square" />
  <img src="https://img.shields.io/badge/Training%20Accuracy-87.10%25-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Published-IEEE-00629B?style=flat-square&logo=ieee&logoColor=white" />
</p>

---

## 📑 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Machine Learning Models](#-machine-learning-models)
- [How the Recommender Works](#-how-the-recommender-works)
- [Experimental Results](#-experimental-results)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Published Paper](#-published-paper)
- [Keywords](#-keywords)

---

## 🔍 Overview

Recommender systems have become pivotal across both commercial and academic domains. This project presents an automated **facial skincare recommendation system** that advises consumers on tailored product choices based on individual skin types, concerns, and preferences.

Traditional models relying purely on collaborative or content-based filtering often fall short of addressing real user concerns. To overcome this, we propose a **hybrid approach** integrating:

- 🧠 **K-Nearest Neighbors (KNN)**
- 🖼️ **Convolutional Neural Networks (CNN)**
- ⚡ **Transfer Learning with EfficientNet-B0**
- 🎯 **Content-Based Filtering**

User inputs such as skin tone, skin type, and acne severity guide the algorithm to recommend the most suitable products. With EfficientNet-B0, the model achieves a **validation accuracy of 80%** and a **training accuracy of 87.10%** — delivering enhanced precision and a more personalized skincare experience.

---

## ✨ Key Features

- 📸 **Real-time face capture** through the web interface
- 🎨 **Skin tone detection** via segmentation + K-Means clustering
- 🔬 **Skin type classification** (Normal · Oily · Dry) using CNN + EfficientNet-B0
- 🩹 **Acne severity scoring** across Low, Moderate, and Severe levels
- 🛍️ **Personalized product recommendations** via cosine similarity
- 🌐 **Web-based & accessible** from virtually anywhere

---

## 🏗️ Architecture

![Architecture Diagram](https://github.com/vinit714/A-Recommendation-system-for-Facial-Skin-Care-using-Machine-Learning-Models/assets/52816788/6971ee9a-4108-43bd-bed7-1687422baecb)

The system architecture is a symbolic representation of the application's component architecture, describing component-to-component connections and overall operation.

When a user accesses the application, their face is captured. Based on the model results and additional user inputs, the system predicts and recommends products matching their concerns. Since the foundation is a **web application**, it remains accessible almost everywhere — with a transparent, user-friendly GUI at its core.

---

## 🤖 Machine Learning Models

The proposed model assesses **acne severity**, **skin type**, and **skin tone**. It combines well-known algorithms such as K-Means and EfficientNet alongside a content-based recommendation model. Each module is broken down below.

### 🎨 Skin Tone Recommendation

Skin tone is determined by first locating and isolating skin pixels, then mapping their color values to a target skin-tone category. The skin-detection technique involves three core operations: **initial segmentation**, **skin-pixel prediction**, and **K-Means clustering**.

![Skin Tone Detection](https://github.com/vinit714/A-Recommendation-system-for-Facial-Skin-Care-using-Machine-Learning-Models/assets/52816788/c9c3f04f-169f-4d04-a93f-f7ed96e765c9)

The threshold for initial segmentation is the average of **TOTSU** and **TMAX**, derived from the grayscale image's histogram.



## 📊 Experimental Results

Training is performed in **Python** with **TensorFlow**, while plotting and data processing tasks use supporting libraries. The trained model then determines the skin type of the measured individual.

### Skin Tone Categories

The system classifies skin tone into six categories:

| Category | Description |
|---|---|
| **Fair** | Light eyes & hair, burns easily, rarely tans |
| **Light** | Hazel/brown eyes, light-brown hair, occasional burning, gradual tanning |
| **Medium** | Brown eyes, dark-brown hair, medium/olive tone, rarely burns, tans easily |
| **Olive/Tan** | Brown eyes, black hair, dark-brown tone, rarely burns, tans quickly |
| **Brown** | Black eyes & hair, deeply pigmented, never burns, tans easily |
| **Dark/Black** | Black hair & eyes, never burns, tans readily |

![Results](https://github.com/vinit714/A-Recommendation-system-for-Facial-Skin-Care-using-Machine-Learning-Models/assets/52816788/bd53c8a3-3646-4a79-aa31-9cf36b3a0089)

CNN analysis classifies skin into *Normal*, *Oily*, and *Dry*, with EfficientNet-B0 raising accuracy to **87.10%** (training) against **80%** (validation) — making it an ideal classifier across the skin spectrum.

![Comparison](https://github.com/vinit714/A-Recommendation-system-for-Facial-Skin-Care-using-Machine-Learning-Models/assets/52816788/60eaa9ca-a701-4580-8ab1-0fb35c863a6d)

### Acne Severity Scale

Although categorical, acne severity is mapped to numeric values:

| Value | Level |
|:---:|---|
| 0 | No Acne |
| 1 | Clear |
| 2 | Almost Clear |
| 3 | Mild |
| 4 | Moderate |
| 5 | Severe |

![Acne Distribution](https://github.com/vinit714/A-Recommendation-system-for-Facial-Skin-Care-using-Machine-Learning-Models/assets/52816788/4e595c22-c4cd-4b5d-9f96-0626f14d386f)

The dataset shows an **uneven class distribution**, with acne predominantly falling into *Class 3 (Mild)*. A key challenge was noisy dermatologist labels and numerous near-duplicate images in the training set.

---

## 🧰 Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python, Flask |
| **Frontend** | React, HTML, CSS |
| **ML / DL** | TensorFlow, Keras, scikit-learn, EfficientNet-B0 |
| **Computer Vision** | OpenCV, K-Means Clustering |
| **Techniques** | CNN, KNN, Transfer Learning, Content-Based Filtering, Cosine Similarity |

---

## 🚀 Getting Started

Clone this repo, head to the root directory, and create a [Python Virtual Environment](https://www.geeksforgeeks.org/python-virtual-environment/).

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Start the backend** — open a terminal from the root folder:
```bash
cd backend
python app.py
```

**3. Start the frontend** — open a second terminal:
```bash
cd frontend
npm install
npm start
```

Once running, the web app launches on your local host. After capturing a photo, it automatically detects facial features and — on submit — redirects you to a personalized recommended-products page. ✨

---

## 📄 Published Paper

This project has been published as an **IEEE paper**. For an in-depth understanding of the methodology and contributions:

> 📘 **[Efficient Net-based Expert System for Personalized Facial Skincare Recommendations](https://ieeexplore.ieee.org/document/10142790)**

---

## 🏷️ Keywords

`Deep Learning` · `Recommendation System` · `Skin Tone` · `Skin Type` · `Acne` · `Transfer Learning` · `EfficientNet`

---

<p align="center">
  ⭐ If you found this project helpful, consider giving it a star!
</p>
