# Styling
All code should follow pep8 when it comes to spacing (4 spaces for tabs)

# Naming
Functions that are native Objective C should be in `camelCase`
Classes that are ObjC will follow `PascalCase`
Helper functions that are not directly related to an ObjC function follow `snake_case`

# Classes
Classes will have `@property` methods to ensure proper handling of ObjC functions.
This is so that if the root ObjC object changes the class reflects it

# Enums
Enums will be in `camelCase` (this way items with a name of `none` don't interfere with python's `None`)
Enums should be located at the top of the file
