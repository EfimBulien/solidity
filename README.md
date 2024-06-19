# Blockchain Real Estate Platform

This is a Flask-based web application for managing real estate transactions on a blockchain. It includes functionalities for user registration, login, account management, balance checking, and creating, updating, and viewing real estate and advertisement information. The application leverages the Web3 library to interact with a smart contract deployed on an Ethereum blockchain.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Routes](#routes)
- [License](#license)

## Features
- User registration and login.
- Account management and balance checking.
- Creating and updating real estate listings.
- Creating and updating advertisements.
- Purchasing real estate.
- Viewing all real estate and advertisements.

## Requirements
- Python 3.7+
- Flask
- Flask-Caching
- Web3.py
- Geth (Go Ethereum client)

## Installation
1. **Clone the repository:**
    ```sh
    git clone https://github.com/EfimBulien/solidity.git
    cd solidity || cd solidity-main
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt || pip install -r commands.txt
    ```

4. **Set up and run your Ethereum node (Geth):**
    Follow the instructions on the [Geth documentation](https://geth.ethereum.org/docs/) to set up and run your local Ethereum node.

## Configuration
1. **Smart Contract:**
   - Deploy your smart contract on your local Ethereum node.
   - Copy the contract ABI to `contract_info/abi_contract.py`.
   - Copy the contract address to `contract_info/address_contract.py`.

2. **App Configuration:**
   - Create a `config.py` file with the necessary configuration details.
   - Example configuration:
    ```python
    config = {
        'DEBUG': True,
        'CACHE_TYPE': 'simple'
    }
    ```

## Usage
1. **Run the Flask application:**
    ```sh
    flask -m run
    ```

2. **Access the application:**
    Open your browser and navigate to `http://localhost:5000`.

## Routes
- **`GET /`** or **`GET /home`** or **`GET /index`**: Home page.
- **`GET /register`**: Registration page.
- **`POST /register`**: Handle user registration.
- **`GET /login`**: Login page.
- **`POST /login`**: Handle user login.
- **`GET /dashboard/<account>`**: User dashboard.
- **`GET /balance/<account>`**: Check account balance.
- **`POST /withdraw`**: Withdraw funds.
- **`POST /create_estate`**: Create a new estate.
- **`POST /create_ad`**: Create a new advertisement.
- **`POST /purchase_estate`**: Purchase an estate.
- **`POST /update_estate`**: Update estate status.
- **`POST /update_ad`**: Update advertisement status.
- **`GET /get_all_ads`**: Get all advertisements.
- **`GET /get_ad`**: Get a specific advertisement by ID.
- **`GET /get_all_estates`**: Get all estates.
- **`GET /get_estate`**: Get a specific estate by ID.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
