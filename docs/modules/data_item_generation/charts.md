# Charts
Charts are generated from Docling Table and are store as annotation to generated pictures.

## ChartFactory
To maintain a consistent interface, a Chart Factory is implemented. This factory serves two main purposes:

- It provides a unified interface for generating chart objects.
- It acts as a wrapper around the chart-generation code developed by Matteo Omenetti, which converts a standardized JSON format into various chart styles.

All chart objects produced by the factory inherit from the ChartAdapter base class, ensuring compatibility and extensibility across different chart types.