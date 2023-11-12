# SMHV Website

Welcome to the repository for the website of SMHV! This website is built using HTML, CSS, JavaScript, and Flask to showcase information about our movement, upcoming events, and ways to get involved.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

To run this website locally, you'll need to have Python and Flask installed on your machine.

1. Clone this repository:

    ```bash
    git clone https://github.com/botsarefuture/smhv_website.git
    cd smhv_website
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Add configuration
   
     ```bash
    cp config.example.json config.json && nano config.json
    ```

     and then add configuration to the file... For questions related the config, contact @botsarefuture
     
5. Run the Flask development server:

    ```bash
    python app.py
    ```

4. Open your web browser and go to `http://localhost:5000` to see the website in action.

## Usage

Feel free to modify the content, styles, and functionality of this website to suit your movement's branding and goals. You can update the events, about us information, and contact details in the appropriate HTML files. Additionally, you can customize the styles in the `static/styles.css` file.

If you're new to Flask, you can refer to the Flask documentation for more information: [Flask Documentation](https://flask.palletsprojects.com/)

## Contributing

We welcome contributions to improve and enhance this website. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
