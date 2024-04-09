# Shiny Web Server

This Shiny app is designed for DNA sequence alignment using the `bs4Dash` and `shiny` packages in R. It offers a user-friendly interface for inputting DNA sequences and viewing alignment results against a predefined database.

## Features

- **DNA Sequence Input**: Users can input a DNA sequence in the text area provided.
- **Search Button**: Upon clicking the "Search" button, the app performs sequence alignment.
- **Alignment Results Display**: The results of the sequence alignment are displayed in table format, including detailed taxonomic information.

## Installation

To run this app, you need to have R installed on your computer. Additionally, the `shiny` and `bs4Dash` packages must be installed. You can install these packages using the following commands in the R console:

```R
install.packages("shiny")
install.packages("bs4Dash")
```

## Usage

1. **Start the App**: Run the app script in RStudio or in your R console.
2. **Input DNA Sequence**: Enter a DNA sequence in the designated text area within the app's interface.
3. **Initiate Search**: Click the "Search" button to perform the sequence alignment.
4. **View Results**: The alignment results and taxonomic information will be displayed in tables.

## Requirements

- This app requires a local copy of the `usearch` tool and a DNA sequence database file. Ensure the `usearch` command within the server function points to the correct location of your `usearch` binary and database file.
- The provided `anno` dataframe is expected to contain annotation information. Make sure the `./other_uc_dict_human_anno.tsv` file path matches where your annotation file is stored.

## Additional Information

The `tmp_merged_db.fasta` file and the `other_uc_dict_human_anno.tsv` file in the folder serves as sample database files. We have used `usearch` to index this file, creating the `merged_human_all.udb` file for website testing purposes. To utilize the full functionality, please construct an index with a complete database.

## Note

This app is configured to work with a specific environment setup, including the `usearch` tool and a sequence database. Adjustments may be required to adapt the app to your specific setup, such as updating file paths and ensuring compatibility with your sequence database and annotation files.

## Acknowledgments

This app utilizes `usearch` for sequence alignment. Please ensure that you comply with `usearch`'s licensing agreement for your use case.

For more information on `bs4Dash` and `shiny`, please visit their respective CRAN and GitHub pages.