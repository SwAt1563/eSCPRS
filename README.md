# [eSCPRS](https://drive.google.com/file/d/1-rdujgzhyd3REjeLH5ACr6AjoQR-oFDC/view?usp=sharing): The State Contract and Procurement Registration System Project

The **eSCPRS** (State Contract and Procurement Registration System) project is a comprehensive solution designed for processing large-scale procurement data from the State of California. The project leverages a variety of technologies, including **FastAPI**, **ReactJS**, **MongoDB**, **Docker**, **Ollama** (to run Gemma2 LLM), and **Power BI**, to build a scalable, efficient, and user-friendly system. This README provides an overview of the project's setup, features, and my contributions.

The project utilizes the [Large Purchases by the State of California](https://www.kaggle.com/datasets/sohier/large-purchases-by-the-state-of-ca) dataset to manage and query data for procurement analysis.

## My Contributions and Features

In this project, I took on several key roles to ensure the successful development and deployment of the eSCPRS system. Here’s a summary of what I accomplished:

### 1. **Data Cleaning and Preparation**
   - I performed **data cleaning** on the dataset, which included handling missing values, correcting inconsistencies, and formatting the data for use in MongoDB.
   - The data cleaning code is available in a Jupyter notebook (`.ipynb` file), where I applied various preprocessing techniques to ensure the dataset was ready for analysis and querying.

### 2. **Data Analysis and Visualization**
   - After cleaning the data, I used **Power BI** for **visualization** to gain insights and perform deeper analysis on the procurement data.
   - The visualizations helped to identify trends and patterns in large procurement transactions, which were valuable for generating insights to support decision-making.

### 3. **Storing Data in MongoDB**
   - I saved the cleaned data in a **JSON** format and used it as **seed data** for populating the **MongoDB** database.
   - I created collections in MongoDB with **indexes and caching** to optimize query performance and ensure efficient data retrieval.

### 4. **Backend Development with FastAPI**
   - I developed a **FastAPI** backend to manage data queries. This backend serves as the core of the system, providing an API to interact with the MongoDB database.
   - The backend supports **11 different queries** that return data based on user input. These queries allow the frontend to extract specific insights from the database.

### 5. **Frontend Development with ReactJS**
   - On the frontend, I used **ReactJS** to build the user interface for interacting with the system.
   - The interface integrates with the FastAPI backend to send user queries and display results in a chatbot-style interface.
   - I ensured that responses are structured in a professional **README** format, making them easily readable and accessible for users.

### 6. **Integrating Gemma2 LLM with Ollama**
   - To provide natural language processing (NLP) capabilities, I integrated **Ollama** with **Gemma2 LLM**. This allowed the system to interpret and respond to user queries intelligently.
   - The integration ensures that user questions about procurement data are processed and responded to in a clear and informative manner.

### 7. **Containerization with Docker and Docker Compose**
   - I containerized the entire project using **Docker** to ensure portability and consistency across different environments.
   - Using **Docker Compose**, I orchestrated multiple services, including the FastAPI backend, MongoDB, and the ReactJS frontend, to run seamlessly in a local development environment.

---

## Getting Started

Follow the instructions below to set up and run the eSCPRS project on your local machine.

### 1. Clone the Repository

Begin by cloning the repository with the following command:

```bash
git clone https://github.com/SwAt1563/Large-Purchases-by-the-State-of-CA.git
```

### 2. Navigate to the Project Directory

After cloning the repository, change into the project directory:

```bash
cd Large-Purchases-by-the-State-of-CA
```

### 3. Configure Git Line Ending Behavior

To prevent automatic line ending conversion by Git, configure Git with the following command:

```bash
make config
```

### 4. Switch to the Development Branch

Switch to the development branch with the following command:

```bash
make checkout-development
```

### 5. Install Prerequisites

Ensure you have the following tools installed on your system:

- **Docker**: Required for containerization.
- **Docker Compose**: For orchestrating multi-container Docker applications.
- **Makefile**: For automating project setup and management tasks.

### 6. Network Setup

To set up the required network, run the appropriate script based on your operating system:

- **Windows**:
  ```bash
  .\create_network.ps1
  ```

- **Ubuntu or macOS**:
  ```bash
  ./create_network.sh
  ```

### 7. Running the Project

Once the network is set up, you can start the project by running:

```bash
make run
```

This command will initiate the services and run the application.

### 8. Pushing Changes to the Current Branch

To push your changes to the current branch, use the following command:

```bash
make push
```

This will ensure your changes are committed and pushed to the appropriate branch.

---

## Features

- **FastAPI Backend**: API to handle user queries, execute MongoDB queries, and return responses in a professional README format.
- **MongoDB Database**: Stores cleaned and indexed procurement data for fast querying.
- **ReactJS Frontend**: User-friendly interface for interacting with the system and receiving chatbot-style responses.
- **Ollama and Gemma2 LLM**: Leverages NLP for interpreting user queries and generating informative responses.
- **Docker and Docker Compose**: Containerized the application for consistency across environments and easy deployment.

With these technologies, the eSCPRS project provides an efficient and scalable system for managing large procurement datasets, enabling users to query and analyze data in a professional and intuitive manner.
