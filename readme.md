# Truth or Dare Card Generator

## Overview

The **Truth or Dare Card Generator** is a Python script that allows you to generate a printable set of truth and dare cards. This can be particularly useful for organizing party games, social events, or simply having fun with friends.

## Features

- **Customizable Number of Cards**: Specify the total number of cards (must be an even number).
- **Flexible Paper Size Options**: Choose from standard paper sizes such as Letter, A4, and Legal.
- **Adjustable Card Dimensions**: Customize the width and height of each card to fit your needs or preferences.
- **Questions Loading**: Automatically reads truth and dare questions from provided text files (`truth_questions.txt` and `dare_questions.txt`).
- **PDF Generation**: Generates a PDF file containing all the cards, ready for printing.

## Requirements

To run the script, you need to have Python installed on your system. Additionally, you will need the following libraries:

- `reportlab`: For generating PDF files.
- `os`: For handling file paths.

You can install the required library using pip:

```bash
pip install reportlab
```

## Usage

1. **Prepare Your Questions**:
   - Create two text files named `truth_questions.txt` and `dare_questions.txt`.
   - Each line in these files should contain a single question.

2. **Run the Script**:
   - Open your terminal or command prompt.
   - Navigate to the directory containing the script and the questions files.
   - Run the script by executing:

     ```bash
     python playing_card.py
     ```

3. **Follow the Prompts**:
   - The script will guide you through entering various parameters such as the number of cards, paper size, card dimensions, and the output PDF filename.
   - After completing all the steps, a PDF file containing your generated truth and dare cards will be created.

4. **Print and Play**:
   - Print the generated PDF on cardstock or regular paper.
   - Cut along the outlines to separate individual cards.
   - Shuffle and play!

## Troubleshooting

- **File Not Found Errors**: Ensure that the `truth_questions.txt` and `dare_questions.txt` files are in the same directory as the script.
- **Encoding Issues**: If you encounter encoding errors, make sure your text files are saved with UTF-8 encoding.
- **Paper Size Adjustments**: If the chosen paper size is too small for the specified card dimensions, the script will automatically adjust the card size to fit at least one card per page.

## Contributing

Contributions are welcome! If you have any ideas or improvements, please feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the terms of the license.