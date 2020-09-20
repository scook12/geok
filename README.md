[![Build Status](https://travis-ci.com/scook12/geok.svg?branch=main)](https://travis-ci.com/scook12/geok)
# geok
pydantic validation for Esri geometries.

## About
geok is a library of schema objects built on pydantic for validating Esri geometry objects. It has the following benefits and use cases:

- Verify your geometries and Esri-related formats are properly formatted at runtime
- Direct interoperability with the ArcGIS API for Python
- Pydantic's integrations are a big plus:
  - Dataclass-compatible and an ORM mode for database development
  - API development and auto-documentation with Starlette/FastAPI
  - graphene-pydantic for developers working on graphQL APIs
  - ...and plenty more!
- Auto-aliasing: Esri schemas use camelCase, but snake_case is idiomatic python so every `geok` model inherits aliasing methods to auto-convert attribute names to their expected camelCase equivalent at runtime (see `aliased_dict` and `aliased_json`)
- Lots of tests! `geok` is largely an exercise in defining operationalized schemas for Esri geometries, but the test cases aim to ensure that the data objects behave as expected beyond pydantic's validation at-construction time

## Status
R&D library in early development, not meant for production. When the version tag is released at 1.0, it will be stable and follow SemVer.

## Contributing
Feel free to open a PR or issue if you spot something!

## License
MIT @ Samuel Cook, 2020