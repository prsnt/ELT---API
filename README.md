# REST API with FASTAPI

# **Table of Contents**
Introduction
Features
Installation
Usage
API Documentation
Contributing
License
Features

# **FastAPI Implementation:**
Highlight the advantages of using FastAPI in your project.

# **Endpoints:**
Certainly! Below is a README template focused on documenting the provided endpoints and their response details:

---

# Project Title - FastAPI REST API

## Introduction

This project involves developing a FastAPI-based RESTful API to manage and retrieve information about various products related to occupational safety and health (OSH). The API connects to a MySQL database (`elt_db`) to fetch and deliver relevant data.

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

# **Installation**
Provide step-by-step instructions on how to install and set up the API locally.
Include details about dependencies, virtual environments, and any specific configurations required.

# **Usage**
Explain how to run the API locally.
Include information on environment variables, configuration settings, and running tests if applicable.

# **API Documentation**
Provide a link or instructions on how to access the API documentation.
Include details on how users can interact with the API, request/response formats, authentication methods, etc.

# **Contributing**
Guidelines for contributing to the API project.
Instructions for submitting bug reports, suggesting enhancements, or making pull requests.

# **License**
Specify the project's license and provide a link to the full license file.

# **Authors**
L  ist the contributors or authors involved in developing the API.
