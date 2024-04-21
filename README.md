# Song Chords to PDF
#### Video Demo:  <URL HERE>

#### Description:

This project is written as the final assignment of CS50p - Harvard introduction to programming in python and is meant for educational purposes.

This program implements s HTML scraper and a PDF exporter which scrapes and generates a file with Chords and Lyrics for famous songs available in [Internet Chord database](https://www.internetchorddatabase.com/Default.aspx). The program can be run on the terminal, and can output to the standard terminal output or to a PDF.

```sh
python project.py url -o output.pdf
```


#### HTML Song Parser

The `HTMLSongParser` class is responsible for parsing HTML content, specifically tailored for song lyrics websites. It utilizes the HTMLParser module to traverse the HTML structure and extract relevant data such as lyrics and chord notations. Key features include:

    Identification of lyric sections and chord notations within the HTML markup.
    Organization of lyrics into sections and chords with associated lyrics.
    Handling of special cases like section headers and line breaks.

#### Song PDF Exporter

The `SongPdfExporter` class extends the FPDF library to facilitate the creation of PDF documents containing formatted song lyrics. It offers methods for adding chords, lyrics, and section headers to the PDF output. Notable functionalities include:

    Generation of PDF pages with chords, lyrics, and section headers arranged in a readable format.
    Customization options for text formatting and styling within the PDF document.

#### Main Execution:

The main section of the script handles command-line arguments using argparse, allowing users to specify a song URL and optionally an output file for the generated PDF. Key actions performed include:

    Retrieval of the song's HTML content via HTTP request.
    Parsing of the HTML content using the HTMLSongParser.
    Conditional execution based on whether an output file is specified:
        If an output file is provided, the parsed song lyrics are exported to a PDF using SongPdfExporter.
        Otherwise, the parsed lyrics are printed to the console in a formatted manner.

#### Additional Features:

    Utilization of colorama for adding color to console output, enhancing readability.
    Handling of special characters like curly quotes for improved text representation.

#### Usage:

Users can run the program from the command line, providing a song URL as input. Optionally, they can specify an output file for the generated PDF. The program then retrieves, parses, and formats the song lyrics accordingly, either displaying them in the console or saving them to a PDF file.

This Python program offers a convenient solution for musicians and enthusiasts to extract, format, and archive song lyrics from online sources with ease and flexibility.


