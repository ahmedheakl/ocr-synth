# Data Item Generation

Each element extracted from the **Docling Document** is converted into a corresponding class instance within this module. These classes are designed to closely align with the original DoclingDocument classes. However, due to differences in data format and structure, some compromises were necessary.

There are four main data item types:

* [**Figure Item**](figure.md): Represents pictures or charts.
* [**Groups Item**](groups.md): Represents inline groups.
* [**Table Item**](table.md): Represents tabular data.
* [**Text Item**](text.md): Represents textual content.

All item classes inherit from a common base class, `MainTextItem`. This base class includes essential metadata such as:

* **New index**: The updated index assigned in the transformed structure.
* **Label**: A fine-grained indicator specifying the content type (e.g., standard text vs. formula).
* **Original index and type**: References to the original position (specific for group) and general type (e.g., Table, Picture, Text, Group) in the seed Docling document.

The `label` provides a detailed classification, while the `type` offers a broader categorization.

The use of a common index in the representation it's a burden coming from the initial implementation.

