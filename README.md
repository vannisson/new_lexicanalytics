# Lexicanalytics Web 🔎📄

**Lexicanalytics** is a web platform tailored for linguists and education professionals, enabling them to extract valuable lexical insights from textual content.

## Technologies Used ⚙️

In this latest iteration, Lexicanalytics harnesses the power of a **Flask** backend server and a responsive **ReactJS** frontend.

## Key Features 📝

Lexicanalytics offers a suite of robust features for text analysis:

* **Data Extraction**: Calculate essential metrics like lexical density, diversity, and word/line counts.

* **Morphological Analysis**: Dive into the morphology of words within the text.

* **Data Visualization**: Make your insights come to life with dynamic graphs and charts.

## Getting Started 🧑🏼‍💻

To start using Lexicanalytics, follow these simple steps:

1. **Clone the Repository**: Begin by cloning the project repository to run the application locally.

    ```shell
    $ git clone https://github.com/vannisson/new_lexicanalytics.git
    ```

2. **Set Up a Virtual Environment**: Create an isolated virtual environment for the project to manage dependencies.

    ```shell
    $ python -m venv venv
    ```

3. **Activate the Virtual Environment**: Depending on your operating system, activate the virtual environment:

   - On Windows:

    ```shell
    $ .\venv\Scripts\activate
    ```

   - On Linux:

    ```shell
    $ source venv/bin/activate
    ```

4. **Install Dependencies**: With the virtual environment active, install project dependencies using pip.

    ```shell
    $ pip install -r requirements.txt
    ```

5. **Database Setup**: You'll need to create the required database tables. Ensure you configure your database URL parameters in an `.env` file.

    ```shell
    $ python create_tables.py
    ```

6. **Start the Server**: Launch the server to begin using Lexicanalytics.

    ```shell
    $ python app.py
    ```

This guide provides a straightforward path to get started with Lexicanalytics on your local machine. For any questions or assistance, please feel free to reach out. Enjoy utilizing Lexicanalytics for your linguistic and educational research needs!
