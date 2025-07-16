# Zomato-EDA
About Dataset
The dataset provides a comprehensive view of the restaurant scene in the 13 metropolitan areas of India( 900 restaurants). Researchers, analysts, and food enthusiasts can use this dataset to gain insights into various aspects such as dining and delivery ratings, customer reviews and preferences, popular cuisines, best-selling items, and pricing information across different cities. It enables the exploration of dining patterns, the comparison of restaurants and cuisines between cities, and the identification of trends in the food industry. This dataset serves as a valuable resource for understanding the culinary landscape and making data-driven decisions related to the restaurant business, customer satisfaction, and food choices in these metropolitan areas of India. In this dataset, we have more than 123000 rows and 12 columns, a fairly large dataset. We will be able to get hands-on experience while performing the following tasks and will be able to understand how real-world problem statement analysis is done.

**Link**:- [Kaggle](https://www.kaggle.com/datasets/narsingraogoud/zomato-restaurants-dataset-for-metropolitan-areas)

Dataset
The analysis is based on the zomato_dataset.csv file, which contains detailed information about restaurants and their menu items.

Columns:

Restaurant_Name: Name of the restaurant.

Dining_Rating: Customer rating for dining experience.

Delivery_Rating: Customer rating for delivery service.

Dining_Votes: Number of votes for dining.

Delivery_Votes: Number of votes for delivery.

Cuisine: Type of cuisine served.

Place_Name: Specific locality of the restaurant.

City: City where the restaurant is located.

Item_Name: Name of the food item.

Best_Seller: Special tags like 'BESTSELLER' or 'MUST TRY'.

Votes: Number of votes for the specific item.

Prices: Price of the food item in INR.

🛠️ Tools & Libraries
This analysis utilizes the following Python libraries:

pandas: For data manipulation and analysis.

numpy: For numerical operations.

matplotlib & seaborn: For data visualization.

folium: For creating interactive geospatial maps.

🚀 Analysis Overview
The project follows a structured approach to analyze the data, from cleaning to drawing conclusions.

1. Data Cleaning & Preprocessing
Handling Missing Values: Null values in Dining_Rating, Delivery_Rating, and Best_Seller columns were identified and imputed. For instance, NaN in Best_Seller was replaced with "NA".

Data Standardization: Inconsistencies in the City column were resolved. For example, localities like 'Banaswadi' and 'Ulsoor' were correctly mapped to 'Bangalore'.

2. Feature Engineering
New features were created to facilitate deeper analysis:

total_votes: The sum of Dining_Votes and Delivery_Votes to measure overall engagement.

Total_rating: The sum of Dining_Rating and Delivery_Rating to create a combined performance score.

3. Exploratory Data Analysis (EDA)
The core of the project involved answering key business questions through visualization:

Restaurant Distribution: Visualized the number of restaurants in each city to identify market size and saturation.

Popularity Analysis: Identified the top-rated and most frequently listed restaurants in each city.

Price Analysis: Compared average item prices across cities and identified the most and least expensive cuisines.

Geospatial Analysis: Plotted restaurant density on an interactive map of India using Folium to visualize regional hotspots.

Customer Engagement: Analyzed total delivery votes per city to gauge user activity.

Menu Insights: Examined the distribution of menu item categories like 'BESTSELLER' and 'MUST TRY'.

📈 Key Insights & Conclusion
City Distribution: Hyderabad, Jaipur, and Mumbai have the highest concentration of listed restaurants, indicating strong market demand and competition.

Brand Presence: National chains like Domino's Pizza and McDonald's have a significant number of outlets across multiple cities, highlighting their strong brand recognition.

Customer Engagement: Cities like Mumbai and Bangalore show very high vote counts, suggesting an active and engaged user base that provides frequent feedback.

Pricing Trends: Mumbai has the highest average item price, while cities like Kolkata and Lucknow feature some of the most expensive individual dishes, often specialty or large-format items.

Delivery Performance: Pune, Hyderabad, and Jaipur lead with the highest average delivery ratings, indicating efficient and high-quality delivery services in these locations.

Market Opportunity: Mumbai's high customer engagement (votes) relative to its restaurant count suggests a highly active market, making it an ideal city for launching a new restaurant venture.
