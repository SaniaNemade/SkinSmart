import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

# load CSVs (paths are relative to where app runs)
df2 = pd.read_csv('./models/recommender/final.csv')
makeup = pd.read_csv('./models/recommender/makeup_final.csv')

LABELS = list(df2.label.unique())

features = ['normal', 'dry', 'oily', 'combination', 'acne', 'sensitive',
            'fine lines', 'wrinkles', 'redness', 'dull', 'pore',
            'pigmentation', 'blackheads', 'whiteheads', 'blemishes',
            'dark circles', 'eye bags', 'dark spots']


def wrap(info_arr):
    return {
        'brand': info_arr[0],
        'name': info_arr[1],
        'price': info_arr[2],
        'url': info_arr[3],
        'img': info_arr[4],
        'skin type': info_arr[5],
        'concern': str(info_arr[6]).split(',')
    }


def wrap_makeup(info_arr):
    return {
        'brand': info_arr[0],
        'name': info_arr[1],
        'price': info_arr[2],
        'url': info_arr[3],
        'img': info_arr[4],
        'skin type': info_arr[5],
        'skin tone': info_arr[6]
    }


# ---------- helpers ----------

def parse_price(price_str):
    """Convert price string like '₹ 1,299' or '1299' to integer (naive)."""
    if pd.isna(price_str):
        return None
    s = str(price_str)
    digits = ''.join(ch for ch in s if ch.isdigit())
    if digits == '':
        return None
    try:
        return int(digits)
    except:
        return None


def price_bucket(price_int):
    """Option B buckets: low <500, medium 500-1500, high >1500"""
    if price_int is None:
        return None
    if price_int < 500:
        return "low"
    if 500 <= price_int <= 1500:
        return "medium"
    return "high"


# Precompute numeric price and bucket columns once
if 'price_numeric' not in df2.columns:
    df2['price_numeric'] = df2['price'].apply(parse_price)
if 'price_bucket' not in df2.columns:
    df2['price_bucket'] = df2['price_numeric'].apply(price_bucket)


def name2index(name):
    res = df2[df2["name"] == name].index.tolist()
    return res[0] if res else None


# ---------- scoring function ----------

def compute_score_for_product(product_row, user_type, user_features_dict, weights, price_range):
    """
    product_row: pandas Series for a product
    user_type: string e.g. "Oily"
    user_features_dict: dict of features {feature_name: 0/1}
    weights: dict with keys 'skin', 'acne', 'price' (float values like 0.1-1.0)
    price_range: 'low'|'medium'|'high'
    """

    # default weights safety
    w_skin = float(weights.get('skin', 0.5))
    w_acne = float(weights.get('acne', 0.5))
    w_price = float(weights.get('price', 0.5))

    score = 0.0

    # 1) skin match (product's skin type equals user's type or 'all')
    prod_skin_type = str(product_row.get('skin type', '')).strip().lower()
    if prod_skin_type == 'all' or prod_skin_type == str(user_type).strip().lower():
        skin_match = 1.0
    else:
        skin_match = 0.0
    score += w_skin * skin_match

    # 2) acne match: if user has acne flag and product mentions acne in concern
    user_has_acne = bool(int(user_features_dict.get('acne', 0)))
    prod_concern = str(product_row.get('concern', '')).lower()
    acne_match = 1.0 if (user_has_acne and ('acne' in prod_concern)) else 0.0
    score += w_acne * acne_match

    # 3) price match: product bucket equals user's selected price_range
    prod_bucket = product_row.get('price_bucket', None)
    price_match = 1.0 if (price_range is not None and prod_bucket == price_range) else 0.0
    score += w_price * price_match

    # 4) small tie-breaker: overlap between user's other concerns and product concerns
    user_concerns = set()
    for f in features[5:]:
        if int(user_features_dict.get(f, 0)) == 1:
            user_concerns.add(f)
    prod_concern_tokens = set([c.strip() for c in prod_concern.split(',') if c.strip() != ''])
    overlap = 0
    if len(user_concerns) > 0:
        overlap = len(user_concerns.intersection(prod_concern_tokens)) / float(len(user_concerns))
    score += 0.05 * overlap

    return score


# ---------- Graph Generation Functions ----------

def generate_sensitivity_graph(user_type, user_features_dict, price_range, weights, sample_product_row):
    """
    Generate sensitivity analysis graph showing how score changes with each weight
    Returns base64 encoded image
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('Sensitivity Analysis: Impact of Weight Changes on Product Score', fontsize=14, fontweight='bold')
    
    weight_names = ['skin', 'acne', 'price']
    weight_labels = ['Skin Type Match', 'Acne Match', 'Price Range Match']
    
    # Store the actual current weights
    current_weights = {
        'skin': float(weights.get('skin', 0.5)),
        'acne': float(weights.get('acne', 0.5)),
        'price': float(weights.get('price', 0.5))
    }
    
    for idx, (weight_name, weight_label) in enumerate(zip(weight_names, weight_labels)):
        # Vary this weight from 0 to 1, keep others constant
        weight_range = np.linspace(0, 1, 20)
        scores = []
        
        for w in weight_range:
            # Create a fresh copy of weights for each iteration
            temp_weights = current_weights.copy()
            temp_weights[weight_name] = w
            score = compute_score_for_product(
                sample_product_row, user_type, user_features_dict, temp_weights, price_range
            )
            scores.append(score)
        
        axes[idx].plot(weight_range, scores, linewidth=2, color=['#1f77b4', '#ff7f0e', '#2ca02c'][idx])
        axes[idx].axvline(x=current_weights[weight_name], color='red', linestyle='--', 
                         label=f'Current: {current_weights[weight_name]:.2f}')
        axes[idx].set_xlabel(f'{weight_label} Weight', fontsize=10)
        axes[idx].set_ylabel('Product Score', fontsize=10)
        axes[idx].set_title(f'{weight_label}', fontsize=11, fontweight='bold')
        axes[idx].grid(True, alpha=0.3)
        axes[idx].legend()
        axes[idx].set_xlim(0, 1)
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_base64}"


def generate_utility_graph(user_type, user_features_dict, price_range, weights):
    """
    Generate utility graph showing distribution of scores across all products
    Returns base64 encoded image
    """
    # Compute scores for all products
    all_scores = []
    for _, row in df2.iterrows():
        score = compute_score_for_product(row, user_type, user_features_dict, weights, price_range)
        all_scores.append(score)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle('Utility Analysis: Score Distribution Across Products', fontsize=14, fontweight='bold')
    
    # Histogram
    axes[0].hist(all_scores, bins=30, edgecolor='black', alpha=0.7, color='#1f77b4')
    axes[0].axvline(x=np.mean(all_scores), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(all_scores):.2f}')
    axes[0].axvline(x=np.median(all_scores), color='green', linestyle='--', 
                   label=f'Median: {np.median(all_scores):.2f}')
    axes[0].set_xlabel('Product Score', fontsize=10)
    axes[0].set_ylabel('Number of Products', fontsize=10)
    axes[0].set_title('Score Distribution', fontsize=11, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Box plot with weight contribution
    weight_contributions = {
        'Skin\nMatch': [],
        'Acne\nMatch': [],
        'Price\nMatch': []
    }
    
    for _, row in df2.iterrows():
        # Calculate individual contributions
        prod_skin_type = str(row.get('skin type', '')).strip().lower()
        skin_match = 1.0 if (prod_skin_type == 'all' or prod_skin_type == str(user_type).strip().lower()) else 0.0
        weight_contributions['Skin\nMatch'].append(weights['skin'] * skin_match)
        
        user_has_acne = bool(int(user_features_dict.get('acne', 0)))
        prod_concern = str(row.get('concern', '')).lower()
        acne_match = 1.0 if (user_has_acne and ('acne' in prod_concern)) else 0.0
        weight_contributions['Acne\nMatch'].append(weights['acne'] * acne_match)
        
        prod_bucket = row.get('price_bucket', None)
        price_match = 1.0 if (price_range is not None and prod_bucket == price_range) else 0.0
        weight_contributions['Price\nMatch'].append(weights['price'] * price_match)
    
    axes[1].boxplot(weight_contributions.values(), labels=weight_contributions.keys(),
                   patch_artist=True, boxprops=dict(facecolor='lightblue', alpha=0.7))
    axes[1].set_ylabel('Contribution to Total Score', fontsize=10)
    axes[1].set_title('Weight Contribution Distribution', fontsize=11, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_base64}"


# ---------- main functions ----------

def recs_cs(vector=None, name=None, label=None, count=5, weights=None, price_range=None):
    """
    vector: list/iterable containing feature values (in same order as 'features' list),
            or name: product name to base recommendations on.
    weights: dict with 'skin', 'acne', 'price' float values (0.1 - 1.0)
    price_range: 'low'|'medium'|'high' or None
    """
    products_out = []

    if weights is None:
        weights = {'skin': 0.5, 'acne': 0.5, 'price': 0.5}

    # obtain user feature dict & user skin type
    if name:
        idx = name2index(name)
        if idx is None:
            raise ValueError("product name not found")
        user_vector = None
        user_type = df2.iloc[idx]['skin type']
    elif vector is not None:
        user_vector = list(vector)
        user_type = None
        for i, t in enumerate(features[:4]):
            if i < len(user_vector) and int(user_vector[i]) == 1:
                user_type = t
                break
        if user_type is None:
            user_type = 'all'
    else:
        raise ValueError("Either name or vector must be provided")

    # build dataframe to score (filter by label if provided)
    if label:
        pool = df2[df2['label'] == label].copy()
    else:
        pool = df2.copy()

    # remove name if passed
    if name:
        pool = pool[pool['name'] != name]

    # compute scores
    scored = []
    user_features_dict = {}
    if user_vector is not None:
        for i, f in enumerate(features):
            user_features_dict[f] = int(user_vector[i]) if i < len(user_vector) else 0
    else:
        user_features_dict = {f: 0 for f in features}
        if 'acne' in str(df2.iloc[idx]['concern']).lower():
            user_features_dict['acne'] = 1

    for _, row in pool.iterrows():
        sc = compute_score_for_product(row, user_type, user_features_dict, weights, price_range)
        scored.append((sc, row))

    # sort by score desc
    scored_sorted = sorted(scored, key=lambda x: x[0], reverse=True)[:count]

    for sc, row in scored_sorted:
        products_out.append(wrap(row[['brand', 'name', 'price', 'url', 'img', 'skin type', 'concern']].to_list()))

    return products_out


def recs_essentials(vector=None, name=None, weights=None, price_range=None):
    response = {}
    for label in LABELS:
        r = recs_cs(vector=vector, name=name, label=label, weights=weights, price_range=price_range)
        response[label] = r
    return response


def generate_analysis_graphs(vector, weights=None, price_range=None):
    """
    Generate both sensitivity and utility graphs for the recommendation system
    Returns dict with base64 encoded images
    """
    if weights is None:
        weights = {'skin': 0.5, 'acne': 0.5, 'price': 0.5}
    
    # Derive user type from vector
    user_type = None
    for i, t in enumerate(features[:4]):
        if i < len(vector) and int(vector[i]) == 1:
            user_type = t
            break
    if user_type is None:
        user_type = 'all'
    
    # Build user features dict
    user_features_dict = {}
    for i, f in enumerate(features):
        user_features_dict[f] = int(vector[i]) if i < len(vector) else 0
    
    # Get a sample product (highest scoring one) for sensitivity analysis
    sample_product_row = df2.iloc[0]  # Use first product as sample
    
    # Generate graphs
    sensitivity_graph = generate_sensitivity_graph(
        user_type, user_features_dict, price_range, weights, sample_product_row
    )
    utility_graph = generate_utility_graph(
        user_type, user_features_dict, price_range, weights
    )
    
    return {
        'sensitivity_graph': sensitivity_graph,
        'utility_graph': utility_graph
    }


def makeup_recommendation(skin_tone, skin_type):
    result = []

    foundation = makeup[
        (makeup['skin tone'] == skin_tone) &
        (makeup['skin type'] == skin_type) &
        (makeup['label'] == 'foundation')
    ].head(2)

    concealer = makeup[
        (makeup['skin tone'] == skin_tone) &
        (makeup['skin type'] == skin_type) &
        (makeup['label'] == 'concealer')
    ].head(2)

    primer = makeup[
        (makeup['skin tone'] == skin_tone) &
        (makeup['skin type'] == skin_type) &
        (makeup['label'] == 'primer')
    ].head(2)

    dff = pd.concat([foundation, concealer, primer], ignore_index=True)
    dff = dff.sample(frac=1)

    data = dff[['brand', 'name', 'price', 'url', 'img', 'skin type', 'skin tone']].to_dict('split')['data']
    for element in data:
        result.append(wrap_makeup(element))

    return result