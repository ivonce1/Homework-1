# Homework-1
Homework 1
Project description and requirements specification

Introduction:
	In this assignment, the objective is to design and implement an essential platform for tracking, analyzing, and accessing comprehensive data on Macedonian stocks. This application is specifically designed to support both individual investors and financial professionals by providing a reliable, data-driven resource for understanding the Macedonian stock market. Built on a robust database, Macedonian Stock Database offers users real-time access to detailed stock information, historical performance, and market analytics. Our platform enables users to search and retrieve data across multiple parameters, helping you explore stock trends, compare companies, and analyze performance with precision. With interactive charts, customized filtering options, and downloadable datasets, you have all the tools needed to conduct in-depth market research. This application also provides daily updates on price changes, company news, and economic indicators that impact the Macedonian market. Additionally, the platform includes educational resources and market insights to support informed decision-making. Macedonian Stock Database is built to empower investors at every level with a comprehensive, user-friendly experience tailored to the specific needs of the Macedonian market.
For this assignment, the process will begin with downloading raw daily stock market data for each issuer on the Macedonian Stock Exchange. After obtaining the data, a series of filters will be applied to extract relevant information and ensure the data is uniformly formatted and structured for further analysis. 

Functional and non-functional requirements specification


Functional requirements:

• Data Collection and Downloading
-	The system must automatically download daily historical stock data for all issuers from the Macedonian Stock Exchange covering the past 10 years.
-	Users should be able to manually trigger data downloads if needed.
•	Data Processing and Transformation
-	The system must filter, clean, and format the downloaded stock data using a Pipe and Filter architecture.
-	The application should retain only relevant information (e.g., date, opening and closing prices, volume) and discard unnecessary fields.
-	The processed data should be stored in a structured database that supports analysis.
•	Data Storage
-	The application must store processed stock data in a database, enabling easy retrieval, updates, and analysis.
-	Users should be able to view data summaries for individual stocks, including daily, monthly, and yearly summaries.
•	Data Visualization
-	The application must provide visualizations such as line charts, bar charts, or candlestick charts to illustrate stock performance trends over time.
-	Users should be able to customize the time range of visualized data (e.g., view data for 1 month, 1 year, or 10 years).
•	Export Functionality
-	The application should provide an option to export data in common formats such as CSV or Excel for further offline analysis.

Non-functional requirements:


•	Scalability
-	The system should be scalable to handle an increase in the number of users and data volume as more companies and historical data are added.
•	Maintainability
-	Code should be modular, allowing for easy debugging and future feature integration.

User personas

 For person 1, who is just starting her investment journey, the application will provide a user-friendly interface with intuitive data visualizations and notifications, helping her stay informed on basic stock movements without being overwhelmed. With quick access to recent trends and simplified visuals, she can develop a better understanding of market behavior.
For person 2, the financial analyst, the application will function as a high-performance tool for detailed stock analysis. Advanced search, filtering, and data export capabilities will allow him to delve deeply into the historical data and perform thorough assessments of market trends, supporting his analytical needs. The system’s scalability will ensure that he can work with large datasets without sacrificing speed or data integrity, making the application reliable even during intensive use.
Finally, person 3, a business owner with limited time, will benefit from a system that offers quick, relevant updates with minimal effort. The weekly summaries, tailored notifications, and clear, concise visualizations will provide him with valuable insights, helping him keep an eye on competitors and industry trends without needing to search manually for information.
This application, through its diverse functionality and careful attention to usability and performance, aims to satisfy a broad spectrum of user requirements while ensuring a reliable, accessible, and efficient stock market analysis experience.


Made by: Ivona Eftimovska 221519,  Marko Kajtazi 221542, Marko Josifovski 221515
