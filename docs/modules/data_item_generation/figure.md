## Figure

Figure items represent visual elements such as images or charts. Each figure is characterized by the following attributes:

* **Original path**: A unique path indicating where the figure is stored.
* **Caption** *(optional)*: A textual description of the figure.
* **Annotation** *(optional)*
* **Chart flag**: A boolean value indicating whether the figure is a chart.

> **Note:** Currently, the presence of an annotation is treated as equivalent to the figure being a chart.

### Chart Generation from Tables

The class method `from_table()` acts as an alternative constructor, enabling the generation of a chart directly from a Docling table. This method is triggered when the chart generation flag is set to `True`.

