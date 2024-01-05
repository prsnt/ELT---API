# REST API with FASTAPI

## **Swagger API documentation**
[FastAPI - Swagger UI.pdf](https://github.com/prsnt/ELT---API/files/13846982/FastAPI.-.Swagger.UI.pdf)



## **Table of Contents**
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Documentation](#api-documentation)

## **FastAPI Implementation:**
FastAPI offers several advantages for projects:

1. **Performance:** It's built on top of Starlette for high performance and asynchronous capabilities, making it very fast and suitable for handling high loads.
  
2. **Easy to Use:** With its simple and intuitive syntax, FastAPI allows developers to build APIs quickly and efficiently.
  
3. **Automatic Docs Generation:** FastAPI automatically generates interactive API documentation using OpenAPI and Swagger UI, simplifying API understanding and testing.
  
4. **Type Annotations:** Utilizes Python type hints for input validation, improving code reliability and reducing human errors.
  
5. **Async Support:** Provides built-in support for asynchronous programming, allowing for concurrent handling of requests, which can improve application responsiveness and scalability.
  
6. **Compatibility:** Works well with modern Python features and frameworks, enabling easy integration with various Python ecosystems and libraries.

These advantages make FastAPI a compelling choice for building modern and efficient APIs in Python projects.

## Endpoints

### `GET /getFilters`

- **Description**: Retrieves filters/categories for products from the database.
- **Response Model**:
  - `BaseFilterResponse`:
    - `success` (int): Indicates the success status of the request.
    - `message` (str): A message indicating the status of the request.
    - `error` (Optional[ErrorModel]): Details about errors, if any.
    - `category` (List[CategoryModel]): List of product categories.
    - `topics` (List[TopicModel]): List of topics related to products.
    - `countries` (List[CountryModel]): List of countries associated with products.
    - `developers` (List[DeveloperModel]): List of developers involved in products.
    - `typeElts` (List[TypeELTModel]): List of types of ELT (Occupational safety and health e-Learning and Training).
    - `languages` (List[LanguageModel]): List of languages available for products.

### `GET /getProducts`

- **Description**: Retrieves products based on various filters.
- **Query Parameters**:
  - `page_number` (int): Page number for pagination (default: 1).
  - `page_size` (int): Number of items per page (default: 10, max: 100).
  - Other parameters for filtering: `cat_id`, `product_id`, `topic_id`, `type_elt_id`, `developer_id`, `country_id`, `language_id`, `payment_type`.
- **Response Model**:
  - `BaseProductResponse`:
    - `success` (int): Indicates the success status of the request.
    - `message` (str): A message indicating the status of the request.
    - `error` (Optional[ErrorModel]): Details about errors, if any.
    - `data` (List[ProductModel]): List of products fetched based on filters.

### `GET /search_topic_and_name`

- **Description**: Searches for topics and product names based on a provided search text.
- **Query Parameters**:
  - `search_text` (str): Text to search for topics and product names.
- **Response Model**:
  - `BaseSearchTopicResponse`:
    - `success` (int): Indicates the success status of the request.
    - `message` (str): A message indicating the status of the request.
    - `error` (Optional[ErrorModel]): Details about errors, if any.
    - `topics` (List[TopicModel]): List of topics matching the search text.
    - `names` (List[ProductModelResponse]): List of product names matching the search text.

### `GET /getallProducts` (Dummy Response)

- **Description**: Returns a dummy response containing product details.
- **Response**: A list of product details including various attributes such as `product_id`, `Name_of_OSH_related_ELT`, `Website`, `Free_Paid`, `Description_of_technology`, `Duration_min`, and additional information categorized by `Category`, `Key_Topic_Area`, `Developers_Distributor`, `Type_of_ELT`, `Country_Head_Quarters`, `Language`, `Skilled_Trade_Occupation`, `Tasks_Topics`, `OSH_Topics`, and `Hardware_Options_for_ELT`.

## **Installation**

### Pre-requisites:

- **Python**: Ensure you have Python 3.7 or higher installed. You can download it from the [Python official website](https://www.python.org/downloads/).
- **MySQL**: Install MySQL database server on your machine. You can download it from the [MySQL official website](https://dev.mysql.com/downloads/installer/).

### Setting up the environment:

1. **Create a Virtual Environment (optional but recommended)**:
    - Open your terminal or command prompt.
    - Navigate to the directory where you want to create your project.
    - Run the following command to create a virtual environment:
      ```
      python -m venv myenv
      ```
      Replace `myenv` with the name you prefer for your virtual environment.

2. **Activate the Virtual Environment**:
    - Activate the virtual environment:
      - On Windows:
        ```
        myenv\Scripts\activate
        ```
      - On macOS and Linux:
        ```
        source myenv/bin/activate
        ```

3. **Install Required Python Packages**:
    - Once the virtual environment is activated, install the required packages using pip:
      ```
      pip install fastapi uvicorn mysql-connector-python[mysql]
      ```

4. **Database Configuration**:
    - Ensure your MySQL server is up and running.
    - Update the database connection details in your code (`host`, `user`, `password`, `database`) to match your MySQL database settings.

5. **Run the FastAPI application**:
    - Run the FastAPI application using Uvicorn, which is included in the installed packages. Use the following command from the directory where your FastAPI code is located:
      ```
      uvicorn your_script_name:app --reload
      ```
      Replace `your_script_name` with the name of your Python script file.

6. **Access the API**:
    - Once the FastAPI application is running, access it in your browser or using API development tools like Postman or cURL by navigating to `http://localhost:8000/`.

These steps will set up the environment and run your FastAPI application. Adjust the paths and filenames as per your project structure and filenames.
## **Usage**

### Available Endpoints:

1. **Root Endpoint**:
   - Access the root endpoint at `http://localhost:8000/` (or the appropriate host and port where your FastAPI application is running) to get a simple "Hello World" message.

2. **Get Filters**:
   - Endpoint: `http://localhost:8000/getFilters`
   - This endpoint retrieves filter options like categories, topics, countries, developers, etc., from the database.

3. **Get Products**:
   - Endpoint: `http://localhost:8000/getProducts`
   - Parameters: You can pass query parameters like `page_number`, `page_size`, `cat_id`, `product_id`, `topic_id`, etc., to filter and paginate the products.
   - This endpoint fetches products based on the provided filters and pagination options.

4. **Search Topic and Name**:
   - Endpoint: `http://localhost:8000/search_topic_and_name`
   - Parameters: Pass a `search_text` query parameter to search for topics and product names matching the provided text.

### Usage Examples:

- To access these endpoints, you can use tools like:
  - **Web Browser**: Simply enter the appropriate URL in your browser's address bar to access the endpoints and view responses.
  - **API Testing Tools**: Tools like Postman, cURL, or HTTPie can be used to send HTTP requests with specific parameters and headers to these endpoints.

- Examples:

  - **Get Filters**:
    ```
    GET http://localhost:8000/getFilters
    ```
    This will return the available filter options.

  - **Get Products**:
    ```
    GET http://localhost:8000/getProducts?page_number=1&page_size=10&cat_id=1&payment_type=Free
    ```
    Replace the query parameters with the desired values to filter and paginate products.

  - **Search Topic and Name**:
    ```
    GET http://localhost:8000/search_topic_and_name?search_text=fall
    ```
    Replace `search_text` with the text you want to search for in topics and product names.

You can test these endpoints using appropriate HTTP methods (GET in this case) and provide necessary parameters to retrieve specific data or perform actions based on the defined functionality for each endpoint. Adjust the parameters as needed to match your use case.

## **API Documentation**

To generate API documentation for your FastAPI project, you can use the built-in feature called "Automatic Interactive API documentation" powered by Swagger UI and ReDoc. FastAPI automatically generates an interactive API documentation based on your code.

Here's how you can access the API documentation:

1. **Run Your FastAPI Application:**
   Ensure that your FastAPI application is running. Normally, it runs on `http://localhost:8000` by default.

2. **Access Swagger UI Documentation:**
   Open your web browser and navigate to `http://localhost:8000/docs`. This URL will display an interactive documentation using Swagger UI, which presents your API endpoints, request/response models, and allows you to test your API by sending requests directly from the documentation.

3. **Access ReDoc Documentation:**
   Additionally, you can access ReDoc documentation by navigating to `http://localhost:8000/redoc`. ReDoc provides a more polished and structured documentation layout for your API endpoints.

### Using Swagger UI:

- **Explore Endpoints:** Swagger UI provides a user-friendly interface to explore all available endpoints.
- **Test Endpoints:** You can test the endpoints directly from the documentation by entering parameters and sending requests.
- **View Models:** Request and response models are displayed, helping you understand the data structures expected and returned by each endpoint.

### Using ReDoc:

- **Structured Documentation:** ReDoc provides a more structured and visually appealing layout for API documentation.
- **Endpoints Overview:** Lists all endpoints with detailed information, including request methods and expected parameters.
- **Model Schemas:** Clearly displays request and response models for each endpoint.

Both Swagger UI and ReDoc offer great ways to interact with and understand your API. They automatically generate documentation based on your code's OpenAPI specifications, making it easier for developers to comprehend and use your API effectively.
