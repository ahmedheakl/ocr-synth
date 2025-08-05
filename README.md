# Synthetic Data Generation

This project consists of the main application, the Synthetic Data Generator (SDG), which is used to generate synthetic datasets from provided source data, and a visualization tool that allows manual visual inspection of the generated LaTeX PDF documents along with their annotated ground truth (GT) values. In short, the two applications can be summarized as follows:

- **Synthetic Data Generator**: An application for generating synthetic documents in a variety of styles. Run this application by executing the following Python scripts from the root directory: ```poetry run python3 synthetic_data_generator.py -e <production or dev>``` (to generate the synthetic data; if *dev* is provided as environment, the code stops if an error is encountered, if production is used, the code catches the error and logs it to a text file, and procedes with the next document in the synthesis sequence) 
For large dataset generation operations, ```poetry run python3 synthetic_data_generator_parallel.py -e <production or dev> ``` can be used.
- **Reading Order Visualizer**: An application used to visualize the created GT data directly on the PDF pages of the generated LaTeX documents. Its sole purpose is to provide a tool that allows users to visually inspect the quality of the GT values for the generated documents. Run this application by executing the following Python script from the root directory:  ```poetry run python3 reading_order_visualizer.py```.
- **Creating the HF dataset**: for the creation of the HF dataset, run ```poetry run python3 save_HF_format.py --input_path 'path_generated_data' --cutoff_date 'date_from_when_to_take_the_document```. The code will create two folders, one that will act as the tmp dataset, storing the pages images and a checkpoint file called metadata.csv, the second will contain the actual parquets file. In addition, if for some reason the metadata.csv already exist together with the pages images, ```poetry run python3 save_HF_format_from_csv.py``` can be used.

### How the file must be insert into the seed dataset:
The dataset expect a docling document with name ``` filename.json``` and the images referenced in that file as ```file_name_pictures_[picture number]```.
An example is 3246478299440331.json and 3246478299440331_pictures_0.png. A suggestion is to use the hash number as the file name.

### IF YOU ONLY HAVE 5 MINUTES 
- Install all the requirements (and if you are on a RedHat Machine, also all the latex packages) and activate the poetry env.
- Put the seed documents (docling json file + the images of the different picture expected in the json (see previous section)).
- ```poetry run python3 synthetic_data_generator.py -e <production or dev>```
- the file will be generated under synthetic_data_generation/generated_latex/internal
- run save_HF_format.py with the args ```--input_path 'path_generated_data' --cutoff_date 'date_from_when_to_take_the_document``` to generate the data.
- enjoy your ready to use parquets file
- ADDITIONAL: if you want to generate the charts, you need to go under ``` synthetic_data_generator/synthetic_data_generation/templates/template_settings/layout_settings/base_layout_style.json ``` and activate the charts generation flag.


#### Origin Data

In order to start syntesizing documents, origin data must first be stored to a particular directory. The path to this directory can be configured as described below in the section *Dataset Path*. This origin data forms the basis upon which the synthetic documents are generated. For now, each origin document that forms the basis for synthetic documents must be stored to this directory as .pdf and .json file. This pair of files is used by the SDG for synthesis. Future work can extend on this idea. 

## 📚 Requirements

- Python >= 3.11
- [Poetry](https://python-poetry.org/docs/#installation) (for dependency management)
- Latest version of docling (check for charts represented as tabular data in the picture annotation)

### Install the dependencies using Poetry
```bash
poetry install
poetry env activate
C:\Users\mirpa\AppData\Roaming\Python\Scripts\poetry env activate
```

#### Install a LaTeX Compiler

Before you run the SDG, you must install a LaTeX compiler. On a Mac you can install MacTeX (the full version is required). MacTeX can be found here: ```https://www.tug.org/mactex/```.


## Synthetic Data Generator

### Configuration

The configuration file can be found in ```synthetic_data_generation/config/config.json```. This file controls the ins and outs of the SDG. In the following, its key/value pairs are described and outlined with brief examples.

In addition some filtering on the input data can be activated based on the data altready generated. For example I can decide to not use seed data recently used (cutoff date) and to only take seed documents with tables.

#### Dataset Path

By default, the SDG looks for the source data in the directory ```/synthetic_data_generation/dataset/```. If you store your data in this directory, you do not need to provide a data path. Otherwise, the path to the source data must be specified using the following key/value pair.

```
"dataset-path": ""
```

#### Document Indexes

You can select the documents that are picked for the synthetic data generation process. The directory you point the SDG to with the value provided for the key *dataset-path* entails the origin data based on which the synthetic data is gnerated. By providing values to the keys *document-start-index* and *document-end-index*, you can select the range of origin documents picked for the synthesis. This comes in handy, if multiple SDG processes are started (e.g. on a cluster), as the first job could take indexes 1 ... 999, the second job could take indexes 1000 ... 1999, etc. If the start index is not provided, it is set to zero by default. In case the finish index is not provided, it is set equal to the number of documents stored in the dataset directory, i.e. all documents from start to the end are used for synthesis.

##### Example

```
...
"document-start-index: 0,
"document-finish-index: 999,
...
```

##### Documents with tables
Set only_documents_with_tables to take only seed documents with tables inside (usefull when you want to generate synthetic document with charts, as the charts are created from tables).

##### cutoff_date
If you want to filter all the documents processed before the cutoff date. For example, if I stop the generation and I want to start again after some days, I can filter the seed documents for which I generated a syn document before the cutoff date.

#### Stored Files

Several temporary files are created during the process of generating the synthetic dataset. Some of these temporary files are necessary to generate the synthesized PDF document, others are just log files containing information about the PDF generation steps. The *stored-files* option allows you to decide which files to save. The generation of particular output files can be truned on/off by providing the according boolean flag *true/false* as value.

- **pdf**: The compiled LaTeX code in PDF format.
- **tex**: The tex code.
- **aux**: Created by default by LaTeX during the PDF generation process; entails metadata about the compilation.
- **log**: Created by default by LaTeX during the PDF generation process; entails detailed information about all steps-taken during the compilation step alongside info, warning, and error messages.
- **pos**: An array of temporary files containing position logs of specific items rendered in the PDF document. The data stored in these file is ultimately used by the SDG to compute GT data. Setting this value to true keeps all position log files.
- **vis**: This flag ensures that all files that are required for the visualiation through the ```reading_order_visualizer.py``` are generated. This flag currently generates the docling document used as a GT.

*Tip: If you intend to generate large datasets, it is recommended to set all values adside pdf and vis to 'false'. The generation of all such files consumes a considerable amount of memory!*

###### Example

```
"stored-files": {
  "pdf": false, // (bool)
  "tex": true // (bool)
  "aux": false, // (bool)
  "log": false, // (bool)
  "pos": true, // (bool)
  "vis": true, // (bool)
}
```

#### Document Selection

The SDG provides three different ways to select documents that serve as source data for synthesizing new documents. These new documents are variants of the source document that differ in style and content based on the templates used for synthesis. Only one option can be selected. If multiple options are provided, any one of them could be used by the SDG (undefined behavior). If no options or only non-existent options are provided, the SDG uses *all* by default. The available options are described below.

- **all**: Synthethic data is generated for every document of the source dataset.
```
"document-selection": {
  "all": {} // The value for this key is ignored.
}
```
- **custom**: Synthetic data is generated only for documents whose file names are explicitly provided. This option allows you to synthesize data only from a custom subset of documents in your source dataset.
```
"document-selection": {
  "custom": {
    "document-file-names": [
      "<file_name_0>.<file_extension_0>",
      "<file_name_1>.<file_extension_1>",
      ...,
      "<file_name_n>.<file_extension_n>"
    ]
  }
}
```
- **random**: Synthetic documents are only generated for a random sample of documents selected from the source dataset. No document is sampled more than once. The sample size can be configured as shown below.
```
"document-selection": {
  "random": {
    "num-to-select": <num_to_select> // (int) A number >= 0
  }
}
```

#### Template Selection

Once the source documents for synthetization are selected, the templates to create synthesized variants of the source document must be selected. The source document provides the data for the synthesis, whereas the template provides the styling of the synthetic document. Think of styling as the configuration of font styles, font sizes, page margins, elements to be displayed (e.g. switch on/off figures, captions, tables, etc.). Therefore, each template is a unique way of determining the style of the synthesized document.

Templates can be selected from three different categories: *official*, *internal*, and *personal* (see the *Template Storage System* section for differences). You can provide templates from all three categories for the same synthesizing process, as you might want to synthesize documents from official sources (e.g. Overleaf), templates provided by the SDG, and your personal (custom) ones. The base layout of the *template-selection* ought to look as the following example:

```
"template-selection": {
  "official": {
  },
  "internal": {
  },
  "personal": {
  }
}
```

---

As a next step, the templates to use for synthesis must be specified for each of the three categories explained above. You can choose between three different options: *all*, *custom*, and *random*. If no option is specified, *all* is selected by default.

Each template can be used multiple times to synthesize data from the same source document. This can be useful if a template uses a randomized selection for multiple style options, resulting in a different document style on every run. This behaviour can be configured by specifying a value for the *num-instances* key. For instance, setting *num_instances = 2* creates two synthesized version of the origin document using the specified template.

Another option to randomize the template selection can be specified via the *num-to-shuffle* value. This value defines how many templates of the selected templates are actually used for data synthesis. Think of this setting as follows: Each of *all*, *custom*, and *random* allows you to select templates from a respective category. *num-to-shuffle* is then used to select a subset of these templates. Why is this useful? E.g. if you want to specify a pool of several templates used for data synthesis, but you only want to generate one synthesized document for each origin document, then setting *num-to-shuffle = 1* provides you exactly with this functionality. Only one template from your selected pool of templates is sampled randomly and used for synthesizing the document. The value provided for *num-to-shuffle* must be greater than zero; otherwise, it is ignored and all selected templates are used for synthesis. Setting a value greater than the selected number of templates, simply results in picking all the selected templates.

- **all**: All templates of the category this option belongs to are selected for data synthesis, i.e. each template will be used at least once to generate a new variant of each selected source document.
```
"<template_type>": {
  "all": {
    "num-instances": <num_instances>, // (int)
    "num-to-shuffle": <num_to_shuffle> // (int)
  }
}
```
- **custom**: Allows to select a subset of templates used for data synthesis.
```
"<template_type>": {
  "custom": {
    "template-names": [
      "<template_name_1>.json",
      "<template_name_2>.json",
      ...,
      "<template_name_n>.json",
    ],
    "num-instances": <num_instances>, // (int)
    "num-to-shuffle": <num_to_shuffle> // (int)
  }
}
```
- **random**: Allows a random selection of templates used for data synthesis. No template is selected more than once.
```
"<template_type>": {
  "random": {
    "num-to-select": <num_to_select>, // (int)
    "num-instances": <num_instance>, // (int)
    "num-to-shuffle": <num_to_shuffle> // (int)
  }
}
```

###### Complete examples

###### Example 1

```
{
  "dataset-path": "/path/to/my/source/dataset/",
  "document-start-index: 0,
  "document-finish-index: 999,
  "stored-files": {
    "log": true,
    "pdf": true
  },
  "document-selection": {
    "all": {}
  },
  "template-selection": {
    "internal": {
      "custom": [
        {
          "template-name": "my_template.json",
          "num-instances": 1
        },
        {
          "template-name": "my_other_template.json",
          "num-instances": 2
        }
      ]
    },
    "personal": {
      "all": {
        "num-instances": 1
      }
    }
  }
}
```

###### Example 2

```
{
  "document-start-index: 10,
  "document-selection": {
    "random": {
      "num-to-select": 12
    }
  },
  "template-selection": {
    "official": {
        "all": {}
    }
  }
}
```
<br>

---

### Template Storage System

There exist three different template categories:

- **Official**: Official templates are a representation of publicly available LaTeX templates and have standardized styles. For example, the LaTeX templates available on Overleaf are part of this category.
- **Internal**: Internal templates are a collection of templates written by the SDG developers and  cover a wide range of template styles. Several such templates are already provided to you out of the box.
- **Personal**: Personal templates are templates created by users of the SDG. I.e. if you create a new template, it belongs to this category. You may want to create your own personal templates if you cannot find the layout styles you want for your synthetic data among the *official* and *internal* templates.

If you want to know more about *official* and *internal* templates available in the SDG, go to the *official* and *internal* directories in ```/synthetic_data_generation/templates/templates/```. These are all templates ready to use out of the box to generate synthetic datasets.

### Template Settings

This section explains how to write a template. In the following, all template options that are available for configuration are described.

#### Template Name

The template name should clearly indicate the layout purpose of the template. If you need some ideas for template names, take a look at the *internal* template directory. It contains several templates with different layouts. The template name is part of the file name generated for the synthetic data files, and thus acts as an identifier for synthetically generated documents.

The template name is restricted to lower case letters (a-z) and underscores (_). Any other character is replaced by the empty string character.

If you do not specify a template name, a default template name is generated. This is strongly discouraged, however, as it obscures the information about which templates were used for which synthetic documents.

###### Example

The following template name is a good example for a template that is in portrait format, has a two column layout, does not feature tables, and is written in blue.

```
"template-name": "portrait_two_col_no_tables_blue_font_template"
```

#### Inactive Items

The *Inactive Items* setting allows you to exclude items of particular types from the generated documents. Items of types that should not be part of the generated document must be specified as a string in the list of inactive items.

Below is a list of all available item types. Any of these can be passed to the inactive items list as a string so that it does not form part of the generated document.

- caption
- figure
- footnote
- list-item
- page-footer
- page-header
- subtitle-level-1
- subtitle-level-2
- subtitle-level-3
- paragraph
- table
- title

###### Example

The following setting would generate a document without captions and tables.

```
"inactive-items": [
    "caption",
    "table"
]
```

#### Excluded Reading Order Items

Templates allow you to exclude items of particular types from the reading order. Unlike the *Inactive Items* setting, where the item does not appear in the document at all, item types provided as part of this setting will appear in the document, but will not be part of the stored GT reading order data. Therefore, this setting enables you to teach a model which item types to consider when reading the document.

###### Example

The following setting excludes all page headers and page footers from the stored GT reading order data. However, if they are not included in *"inactive-items"*, they will be rendered as part of the generated document.

```
"excluded-reading-order-items": [
  "page-header",
  "page-footer"
]
```

#### Layout Style

The *Layout Style* setting determines the appearance of generated documents. The basic layout settings are provided by the SDG and work out of the box. To customize the layout settings to your needs, you can easily override the default settings by specifying the key/value pair of a particular setting in your template.

Below is the basic layout configuration as provided by the SDG. Any key/value pair can be customized by simply specifying it in the newly created template. The SDG imposes restrictions on some of these values (see later in this section).

All distance values of the page layout must be specified in the unit pt (approximately 1 pt = 0.3515 mm).

```
{
  "packages": ["geometry"],
  "page-format": "portrait", // (str) Can be "portrait" or "landscape"
  "page-height": 794.97, // (float) [pt] A4 page height
  "page-width": 614.295, // (float) [pt] A4 page width
  "num-columns": 1, // (int)
  "column-separation": 0.0, // (float) [pt]
  "has-line-numbers": false, // (bool)
  "text-height": 556.47656, // (float) [pt]
  "text-width": 430.00462, // (float) [pt]
  "baseline-skip": 12.0, // (float) [pt]
  "text-parindent": 15.0, // (float) [pt]
  "hoffset": 0.0, // (float) [pt]
  "voffset": 0.0, // (float) [pt]
  "odd-side-margin": 19.8752, // (float) [pt]
  "top-margin": -13.87262, // (float) [pt]
  "head-height": 12.0, // (float) [pt]
  "head-sep": 25.0, // (float) [pt]
  "foot-height": 9.0, // (float) [pt]
  "foot-skip": 30.0, // (float) [pt]
  "font-color": "", // (str) See list of available colors below or "random"
  "font-size": 5, // (int) A value in [1, 10] or zero (random)
  "font-style": "" // (str) See list of availabe font styles below or "random"
}
```

##### Available Font Colors

Some font colors available in LaTeX that are not listed below have been intentionally omitted for readability reasons. These colors have a very light appearance, making it difficult to distinguish individual characters.

- black
- blue
- brown
- cyan
- darkgray
- gray
- green
- magenta
- olive
- orange
- purple
- red
- teal
- violet

##### Available Font Styles

Some LaTeX font styles are not included in the following list as they caused problems when used in a multi-col layout. Specifically, the lines were not broken up correctly.

The appearance of all font styles below can be checked out [here](https://www.overleaf.com/learn/latex/Font_typefaces).

- bookman
- charter
- computer-modern-roman
- computer-modern-sans-serif
- computer-modern-typewriter
- helvetica
- latin-modern-dunhill
- latin-modern-roman
- latin-modern-sans-serif
- latin-modern-sans-typewriter
- palatino
- tex-gyre-adventor
- tex-gyre-bonum
- tex-gyre-cursor
- tex-gyre-heros
- tex-gyre pagella
- tex-gyre-schola
- tex-gyre-termes
- times
- utopia

#### Line Numbers

The *Line Numbers* setting allows line numbers to be displayed to the left of each line in the generated document. Line numbers can also be included in the GT reading order data.

Line numbers are only displayed on single-column and two-column multi-column layouts if they are enabled. If line numbers are enabled for multi-column layouts with more than two columns, these settings are ignored and line numbers are not displayed. There is simply not enough space to display line numbers on page layouts with more than two columns.

If line numbers are configured to be part of the reading order, they appear before the item to which they correspond in the reading order. That is, the line numbers are read first, and then the actual content is read. Line numbers must be displayed to be included in the reading order.

###### Example

```
"line-numbers": {
  "are-displayed": true // (bool)
  "are-included-in-reading-order": false // (bool)
}
```

#### Watermarks

Watermarks can be displayed as text in the background of any document page. It is possible to change the displayed text, font color, font color intensity (for gray color only), the text angle, and the text size.

###### Example

```
"watermarks-style": {
  "text": "confidential", // (str) The watermark text or "random"
  "font-color": "green", // (str) Any color of the xcolor package or "random"
  "color-intensity": 1.0, // (float) A value in [0.1, 0.9] or zero (random)
  "angle-degrees": 30, // (int) A value in [1, 360] or zero (random)
  "size": 1 // (int) A value in [1, 10] or zero (random)
}
```

#### Item Position

Template files provide the functionality to adjust the position of *figure* and *table* elements on document pages. The positioning options available for figures and tables are identical. There are three positioning options:

- **spans-all-column**: The item occupies the entire page width, regardless of the number of columns in the selected layout. Even if the page layout used has two columns, for example, the item will still be positioned as if it were part of a page with a single-column layout.
- **spans-one-column**: The item is contained within a single page column. The item cannot span multiple columns when this option is selected.
- **wrap**: Text may wrap around the element. The item is positioned either to the left or to the right of the column to which it belongs. Positioning the item in the center of the column and allowing text to wrap to the left and right of it is not supported because it causes layout issues. Also, the wrapping position is only available for single-column layouts. Testing with multi-column layouts revealed inconsistent behavior of LaTeX that made it impossible to create reliable GT bboxes.

It is further possible to let the SDG **randomly select** the position of elements (see the example below for more information).

On single-column pages, setting either *spans-all-column* or *spans-one-column* to true results in the same behavior; the item can use the text width. If more than one option is set to true, the code defaults to random positioning. If no option is given, the code defaults to positioning items within one column, i.e. its behavior emulates the setting ```"spans-one-column": true```.

For tables, the code chooses the ideal table position based on the number of columns and rows in the table. For tables with a large number of columns and/or rows, this behavior avoids unwanted layout distortions.

###### Example

```
"item-position": {
  "figure-item": {
    "spans-all-column": false, // (bool)
    "spans-one-column": true, // (bool)
    "wrap": false, // (bool)
    "random": false // (bool)
  },
  "table-item": {
    "spans-all-column": false, // (bool)
    "spans-one-column": false, // (bool)
    "wrap": false, // (bool)
    "random": true // (bool)
  }
}
```

#### Item Style

While the *layout-style* option can be used to specify the base style of the document, the *item-style* option provides a more fine-grained choice for styling individual items. This means that a document has a particular base layout style, but that items of specific types can have a style that differs from this base layout style. The style of such items can also be selected for each position option. For instance, tables that span the entire page can be styled differently than tables that are contained within a single column of text (see the example below for a better understanding). If the item style options are not provided for a particular item type, the layout style options are used by default.

The styles for all items must be provided as part of the value of the *item-style* key. As of now, the code provides individual styling for figures and tables (see the example below).

###### Example for figure item

```
"item-style": {
  "figure-item": {
    "spans-one-column": {
      "font-color": "red",
      "font-size": 5,
      "font-style": "helvetica",
      "position": "l", // Move to the left
      "size": 5
    },
    "spans-all-column": {
      "font-color": "blue",
      "font-size": 2,
      "font-style": "courier",
      "position": "r", // Move to the right
      "size": 2
    },
    "wrap": {
      "font-color": "random",
      "font-size": 0, // Random selection
      "font-style": "random",
      "position": "", // Position to the left or right (random)
      "size": 0 // Random selection
    }
  }
}
```

###### Example for table item

Tables have no support for the *position* and *size* options.

```
"item-style": {
  "table-item": {
    "spans-one-column": {
      "font-color": "random",
      "font-size": 0,
      "font-style": "random"
    },
    "spans-all-column": {
      "font-color": "random",
      "font-size": 0,
      "font-style": "random"
    },
    "wrap": {
      "font-color": "olive",
      "font-size": 0,
      "font-style": "random"
    }
  }
}
```

#### List Items

The selection of the list item type, i.e. itemize, enumerate, or description, can be defined in a template. If no list item type setting is provided in a template, the SDG chooses a list item type randomly. Furthermore, it is possible to provide the symbol type. This allows users to provide a preferred symbol type like "a)", "a.", "a.)", etc. The symbol is ignored if "item" is used as type, the standard bullet point is used in this case.

```
"list-items": {
  "type": ..., // (str) One of "item", "enumerate", or "random"
  "symbol": ... // (str) E.g. "alph*.", "alph*)", etc.
}
```

##### Example Configuration

```
{
    "test-split-size": 0.2,
    "storage-dir-path": "/path/to/store/generated/hf-data/to",
    "datasets": [
        {
            "name": "name-of-first-dataset",
            "path": "/path/to/synthetic-hf-basis-data/of/first-dataset",
            "num-pages-to-load": 1
        },
        {
            "name": "name-of-second-dataset",
            "path": "/path/to/synthetic-hf-basis-data/of/second/dataset",
            "num-pages-to-load": 1
        }
    ]
}
```

The above example entails all the information needed, that is, no key/value pairs are missing in this example. The key/value pairs can be explained as follows:

- **test-split-size (float):** Determines the percentage of the generated HF dataset that should be used as test split (value in [0, 1])
- **storage-dir-path (str):** The path the generated HF dataset is stored to
- **datasets (list):** This list of dictionaries allows to configure from which synthetically generated datasets you want to take data from. For instance, you might have created synthetic docs from the Wikipedia and arXiv dataset; now you desire to pack some document pages from both datasets into the HF dataset, this options enables you to do so. Each dictionary provided as list item configures the data taken from one synthetic dataset. The key/value pairs of each list item is described below:
  - **name (str):** The name of the dataset that is used internally, it has no effect to the outside world. This pair can be used in future extensions to make use of the name (for instance, for logging, etc.)
  - **path (str):** The path where the synthetic data is stored. The application loads the synthetic data form this path for the HF dataset generation.
  - **num-pages-to-load (int):** The number of document pages loaded from the dataset specified by this dictionary. This key/value pair allows to configure the composition of a generated HF dataset. The documents are always retrieved in alphabetical order w.r.t. their document hash, starting at index zero.

<br>

## Reading Order Visualizer

The Reading Order Visualizer (ROV) was created to allow easy manual visual inspection of synthetically generated LaTeX PDF files with their created GT values.

Each item on a latex PDF page is annotated with its GT bbox and further labeled with its reading order index. In addition, each item is connected to its predecessor and successor items in the reading order with a straight line. This facilitates the mental task of visually following the reading order of a document. If an item does not have a predecessor on the same page, it is linked to the center of the top margin. This behavior can occur for a number of reasons. For example, when text flows from one page to another, or when floating images and/or floating tables are moved to other pages to make the page layout more appealing.

The visualizer code loads the generated LaTeX PDFs and their corresponding GT data and uses the GT values to annotate each page of each synthesized document. The annotated PDF files are stored in ```reading_order_visualization/generated_annotations/<template_type>/```. If the visualization fails for a specific document, the terminal logs show a short information about the error. The details about the errors are logged in a text file stored in ```reading_order_visualization/logging/logs/vis_file_generation_error_logs.txt```. Errors in the reading order visualization are not per se an indicator of incorrect GT data.

Run this application by executing the following Python script from the root directory.<br>

```
python3 reading_order_visualizer.py
```

## Charts Generation
Working on top of the repo https://github.ibm.com/DeepSearch/chart-rendering/tree/main, a chart from table generation can be added. 
The flag ``` "chart-flag"  ``` must set to True inside ``` synthetic_data_generator/synthetic_data_generation/templates/template_settings/layout_settings/base_layout_style.json ```.
By default the charts available are Pie, Bar, StackedBar and are choosen randomly. (As Stacked bar requires more parameters, if the generation fails, the other two are tried instead).

The style of the charts can be modified in the original repo.

---
<br>

## Demo

Clone the repo to your machine and install the virtual environment:
```
python3 -m venv venv
pip install -r requirements.txt
```

Configure the synthetic document generation config file in ```synthetic_data_generation/config/config.jons``` by copying the following content to it:
```
{
  "dataset-path": "./synthetic_data_generation/dataset/demo/wikipedia/",
  "document-start-index": 0,
  "document-finish-index": 4,
  "stored-files": {
    "pdf": true,
    "tex": false,
    "aux": false,
    "log": false,
    "pos": false,
    "vis": true
  },
  "document-selection": {
    "all": {}
  },
  "template-selection": {
    "official": {
    },
    "internal": {
      "all": {
        "num-instances": 1,
        "num-to-shuffle": 1
      }
    },
    "personal": {
    }
  },
  "export-data": {
    "domain": "wikipedia",
    "dataset": "synthetic docs",
    "url": null,
    "title": null,
    "extra.category": null,
    "extra.dpi": 120,
    "extra.hap_confidence": null,
    "extra.language": "EN"
  }
}
```

Now, you can run the document synthesis via the command:
```
python3 synthetic_data_generator.py -e production
```
The results can be found in the directories ```synthetic_data_generation/generated_latex/internal/``` and ```synthetic_data_generation/generated_hf/```.

The synthesized documents and their ground truth data can be visualized using:
```
python3 reading_order_visualizer.py
```
The visualized results are stored to ```reading_order_visualization/generated_annotations/```.

To generate the HF dataset, you must create a directory somewhere on your machine where you want to store the data to. The configuration can be done in file ```synthetic_data_generation/config/config.json```. Change the value of key ```storage-dir-path``` to the storage directory you have just created. Make sure you have only one dict entry in the list corresponding to key ```datasets```. Set the value of key ```path``` to ```synthetic_data_generation/generated_hf_dataset/<directory_name_of_the_only_dir_here>```. Set ```num-pages-to-load``` to some desired number, e.g. 100 to make sure all pages are loaded. Run:
```
python3 run_synthetic_data_to_hf_ds.py
```

---
<br>

## Extensions

This section is a compilation of ideas for future extensions to this application.

#### Line Numbers

- Different font styles (maybe the model cannot generalize well enough using only the standard LaTeX package)

#### List Items

- Create separate bboxes for the symbol and the text (similar to the line numbers implementation)
- Nested list items (list-item-level-1, list-item-level-2, list-item-level-3, etc.)

#### Watermarks

- Watermark images instead of plain text

#### Official templates

- Templates from overleaf
- Power point templates (https://www.overleaf.com/learn/latex/Beamer)

#### Source dataset format

- Provide functionality that a CCS-like json file with images stored in some other directory can be used as source data. The images are then not cropped from a pdf document, but loaded directly from that directory.
- Allow data of all items to be part of the main text, i.e. there is no need for using the "__ref" key to look up information anymore. This could make it easier for users to provide their data.

## Installing on the redhat machine:

sudo mktexlsr /usr/share/texlive/texmf-dist/
