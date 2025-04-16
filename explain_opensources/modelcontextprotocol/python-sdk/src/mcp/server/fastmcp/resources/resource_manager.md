# ResourceManager
- manage resources and templates in the FastMCP system. It provides functionality for adding, retrieving, and listing resources and templates
## init
- Initializes the internal data structures for managing resources and templates.
- Provides flexibility to enable or disable warnings for duplicate resources.
## add_resource
- Ensures that resources are uniquely identified by their URIs.
- Prevents accidental overwriting of existing resources.
## add_template
- Allows dynamic creation of templates from functions.
- Provides a structured way to manage templates for generating resources dynamically.
## get_resource
- Provides a unified interface for retrieving resources, whether they are pre-registered or dynamically generated from templates.
- Ensures robust error handling during resource creation.
## list_resources
- Allows inspection of all currently registered resources.
## list_templates
- Allows inspection of all currently registered templates.
