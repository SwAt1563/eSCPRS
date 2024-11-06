# eSCPRS: The State Contract and Procurement Registration System Project

This project involves the [Large Purchases by the State of California](https://www.kaggle.com/datasets/sohier/large-purchases-by-the-state-of-ca) dataset and integrates multiple technologies including **FastAPI**, **Docker**, **MongoDB**, **Natural Language Processing (NLP)**, **Ollama**, **Gemme**, **Vite**, **React**, and a **Chatbot**.

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