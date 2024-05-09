# OpenCF: The File Conversion Scripts

The `opencf` package provides a collection of Python scripts for file conversion tasks, built on top of the [opencf-core](https://test.pypi.org/project/opencf-core/) framework. These scripts offer functionalities to convert various file formats, including text, CSV, JSON, XML, Excel, and image files, making it easy to handle different types of data transformations efficiently.

## Features

- **Extensive Conversion Support**: The package includes scripts for converting between various file formats, including text, XML, JSON, CSV, and Excel.
- **Integration with `opencf-core`**: Utilizes classes from the `opencf-core` package for file I/O operations, MIME type detection, and exception handling.
- **Modular Converter Classes**: Each conversion script is backed by a custom converter class tailored to handle specific file format conversions, extending the base converter class provided by `opencf-core`.
- **Flexible Input/Output Handling**: Supports reading from and writing to different file formats seamlessly, leveraging the capabilities of `opencf-core`.
- **Custom File Handlers**: Implements custom file reader and writer classes for Excel and image files, demonstrating extensibility and versatility.
- **Command-Line Interface**: Offers a command-line interface for executing file conversion tasks, allowing users to specify input and output file paths and types conveniently.
- **Extensibility**: Other input/output pairs converters can be easily added to augment the existing functionality, providing flexibility for handling a wider range of file formats.
- **Direct Integration**: For specific projects, each converter script can directly leverage the separated package `opencf-core` to build custom converters tailored to project requirements.

## Conversion Handlers

This module provides classes for converting between different file formats. It includes [concrete implementations of conversion classes](./opencf/converters.py) for various file types.

- `TextToTextConverter`: Marge text based files (txt, md, xml, json, ...).
- `XMLToJSONConverter`: Converts XML files to JSON format. (Reader: XmlToStrReader, Writer: DictToJsonWriter)
- `JSONToCSVConverter`: Converts JSON files to CSV format. (Reader: JsonToDictReader, Writer: ListToCsvWriter)
- `CSVToXMLConverter`: Converts CSV files to XML format. (Reader: CsvToListReader, Writer: StrToXmlWriter)
- `XLSXToCSVConverter`: Converts Excel files to CSV format. (Reader: SpreadsheetToPandasReader, Writer: ListToCsvWriter)
- `ImageToPDFConverter`: Converts image files to PDF format. (Reader: ImageToPillowReader)
- `ImageToPDFConverterWithPyPdf2`: Converts image files to PDF format using PyPDF2. (Reader: ImageToPillowReader, Writer: PyPdfToPdfWriter)
- `PDFToImageConverter`: Converts PDF files to image format. (Reader: PdfToPyPdfReader)
- `PDFToImageExtractor`: Extracts images from PDF files. (Reader: PdfToPyPdfReader)
- `ImageToVideoConverterWithPillow`: Converts image files to video format using Pillow. (Reader: ImageToPillowReader, Writer: VideoArrayWriter)
- `ImageToVideoConverterWithOpenCV`: Converts image files to video format using OpenCV. (Reader: ImageToOpenCVReader, Writer: VideoArrayWriter)
- ...

## Getting Started

To use the `opencf` package, follow these steps:

1. Install the package along with its dependencies using your preferred package manager.
2. Import the required classes into your Python scripts or applications, ensuring that the `opencf-core` package is accessible.
3. Utilize the provided converter classes to perform file format conversions as needed, specifying input and output file paths and types.
4. Execute the scripts either programmatically or via the command-line interface, providing necessary arguments for file conversion tasks.

## Example Usage

Here's an example demonstrating how to use the `opencf` package for converting an PNG file to PDF:

```bash
# Install the package along with its dependencies (if not already installed)
pip install -i https://test.pypi.org/simple/ opencf

# Run the converter script
opencf examples/input/example.png -o examples/output/example.pdf
# or
opencf examples/input/example.png -ot pdf
```

This command executes the `ConverterApp` class, initiating the conversion process from an PNG file to a PDF file using the appropriate converter classes.

## Other examples

- pdf to png

You can set, the output argument as a folder. So, the png files would be in that folder. Using a filepath instead of a folder may yield an error.

```bash
opencf examples/input/example.pdf -o examples/output -ot png
```

This command will write png files into the `examples/output` as mentioned

## Contribution

Contributions to the `opencf` package are welcome! Feel free to submit bug reports, feature requests, or pull requests via the GitHub repository. Additionally, consider extending the functionality by adding support for additional file formats or improving existing converter classes.
