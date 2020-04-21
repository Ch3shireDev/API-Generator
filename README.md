# API Generator

Script for generating ASP.NET Core API and (in the future) Angular frontend from given yaml structure.

## Usage

In `ResourceAPI` there is already generated project. To test program:

1. Remove ResourceAPI directory.
2. Generate project using `python main.py` command.
3. Run ResourceAPI project in Visual Studio.
4. Install all required npm components.
5. Refactor all files for reading convenience.

## Yaml file

Yaml is in the OpenAPI standard, with removed all api and only structures left. Any number of models is available.