# Inventory Management Chatbot
A Flask chatbot application powered by OpenAI's GPT-3.5 Turbo APIs, bridges the gap between complex data analysis and user-friendly interaction. It supports queries on inventory levels, sales forecasts, and more, directly integrating with our database. Integrating linear regression forecasting methods. Additionally, it features a user-friendly chatbot UI written in HTML.
## Forecast.py
The approach integrates two sophisticated linear regression models, trained to predict future sales based on historical data. One model focuses on item-level predictions, while the other specializes in category-level forecasts, allowing for tailored insights depending on the granularity required.

Here's a breakdown of how the system operates:

Model Loading: The LinearRegression algorithm from scikit-learn and use joblib to load our pre-trained models—one for items (linear_regression_model.pkl) and another for categories (linear_regression_model_category.pkl).

Data Handling: Chatbot can predict future sales for both individual items and broader categories. Depending on the user's query, it fetches historical sales data and uses it to make informed predictions.

Dynamic Forecasting: The core function, predict, dynamically adapts to the user's request—whether for a specific item or a category. It processes the input, retrieves relevant historical data, and applies the appropriate model to predict next week's sales.

User-Friendly Outputs: The chatbot rounds up the prediction to the nearest whole number, ensuring the forecast is practical and easily interpretable for inventory planning.

This project not only showcases our capability to integrate AI with practical applications but also represents a significant step towards optimizing inventory management, making operations more efficient, and helping businesses plan their inventory needs with unprecedented accuracy.
