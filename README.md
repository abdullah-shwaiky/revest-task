# Data Warehouse and Recommendation System Project

<img src="https://revest.sa/wp-content/uploads/2023/06/revest-logo.svg" alt="Project Image" width="100%" height="auto">

## Task 1: Data Warehouse Solution

In this task, I designed and implemented a data warehouse solution using **PostgreSQL** as the data warehouse. I created an **ETL (Extract, Transform, Load)** pipeline using Python to extract data from CSV files, transform it as needed, and load it into the PostgreSQL database. Afterwards, the database is stored to **parquet** files. To store the data, I created the following database tables:

1. **Orders Table**: Contains order, shipping, and sales data.
2. **Customers Table**: Contains customer information including id, name, and address.
3. **Products Table**: Contains product information including id, name, and category.

Additionally, I developed a **Streamlit interface** that interacts with the data warehouse and showcases the data. The interface allows users to:

- Visualize the data stored in PostgreSQL.
- Interact with an **API** built in **Task 2**.
- Display real-time log information.

## Task 2: Recommendation System Deployment

In this task, I focused on building and deploying a recommendation system. The implementation steps were as follows:

1. **API Development**: I developed an **API** using **Django REST Framework** to handle requests and provide recommendations.
2. **Caching**: Integrated **Redis caching** to improve the performance of the recommendation system.
3. **Logging**: Used **MongoDB** to log the API's input and output for monitoring purposes.
4. **Containerization**: Both the **Streamlit interface** and the **Django API** were containerized separately using **Docker**.
5. **Docker Compose**: Created a **docker-compose** file to manage and run all the services (Streamlit, Django API, Redis, and MongoDB) in a single cluster.

## Instructions to Run the Solution

To run the solution locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/abdullah-shwaiky/revest-task.git
   cd revest-task
   ```
2. Make sure Docker and Docker Compose are installed and functional.
3. Run the command:

   ```bash
   docker-compose up --build -d
   ```

4. Access the interface on your browser through the url: http://0.0.0.0:8500
