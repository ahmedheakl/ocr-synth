# What to do next
### [] Problem exporting to doctags
A major issue lies in the current handling of inline equations. At the moment, we only apply markers at the beginning and end of the block. However, when multiple provenance (prov) sources are involved, this approach causes significant problems, as the current doctags export logic performs an intersection across all components within the group.

This problem exist in general for each each element (table, text, ...) as the multiple provs are currently not handled by the doctags.

In addition as we are not saving the position of each word, we cannot use the other parameter `char_span`.

This is currently not supported due to visual issues with LaTeX, as it was introducing excessive spacing between words.

### [] Tables
Currently, only full-page tables are handled correctly. When switching to in-column tables, layout issues arise, such as text overflowing beyond the page boundaries.

### [] Efficiency
Make everything faster and more plug and play. The current complete pipeline is too complicated.

### [] Refactoring
The current code is a mess, a mix between my code and the previous intern code. The representation in mind were very different and a complete refactoring tailored to the Docling Document format is needed.
