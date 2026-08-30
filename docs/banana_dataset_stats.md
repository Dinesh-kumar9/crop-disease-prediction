# Banana Dataset Analysis
Generated on: 2026-02-09

## 1. Dataset Overview
- **Source:** BananaLSD (OriginalSet)
- **Total Images:** 937
- **Collection Method:** Field-collected (Natural environment, variable lighting)
- **Validation Strategy:** Automatic Split (20% of training data during runtime)

## 2. Class Distribution
| Class | Count | Percentage | Description |
| :--- | :--- | :--- | :--- |
| **Sigatoka** | 473 | 50.5% | Fungal leaf spot disease |
| **Pestalotiopsis** | 173 | 18.5% | Fungal infection causing grey spots |
| **Cordana** | 162 | 17.3% | Leaf spot disease (Cordana musae) |
| **Healthy** | 129 | 13.7% | No visible disease symptoms |

## 3. Field vs. Lab Ratio
**Result:** **~100% Field Conditions**

**Evidence:**
- The dataset structure and file counts (e.g., `sigatoka: 473`) match the **Banana Leaf Spot Dataset (BananaLSD)**.
- BananaLSD is specifically designed for real-world field conditions, featuring complex backgrounds and natural lighting variations. It is not a lab-controlled dataset.
- Files are named sequentially (e.g., `0.jpeg`, `100.jpeg`), consistent with the processed version of this public dataset.

## 4. Relevance to Research Paper
This dataset supports the paper's claim of "Real-World applicability" better than lab datasets because models trained on it generalize better to actual farm conditions.
