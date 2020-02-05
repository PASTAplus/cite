# cite
A data citation generator for PASTA+ data packages

## About

The Cite web service is a managed service of the Environmental Data
 Initiative (EDI). Cite generates formatted citations for scientific data packages archived in the PASTA+ data repository. Cite provides a simple to use REST end-point:

```https://cite.edirepository.org/cite/<pid>```

where "pid" is a PASTA package identifier.

Cite accepts the following options as query parameters with the request URL:
 
```?<env>=[production(default), staging, development]```

```?<style>=[ESIP(default), DRYAD, BIBTEX, RAW]```

The response body format is controlled by the request "Accept" header value. 
Recognized media-types are: `text/plain`, `text/html`, and `application/json`
(note: media-types with parameters are not considered).

## Examples:
1 - Retrieve "ESIP" stylized citation (default) in plain text format:
```text
curl -s -H "Accept: text/plain" -X GET https://cite.edirepository.org/cite/edi.460.1

Armitage, A.R., C.A. Weaver, J.S. Kominoski, and S.C. Pennings. 2020. Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019 ver 1. Environmental Data Initiative. https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6. Accessed 2020-01-28.
```
2 -  Retrieve "DRYAD" stylized citation in plain text format:
```text
curl -s -H "Accept: text/plain" -X GET https://cite.edirepository.org/cite/edi.460.1?style=DRYAD

Armitage AR, Weaver CA, Kominoski JS, and Pennings SC (2020) Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019. Environmental Data Initiative. https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6
```
3 - Retrieve "ESIP" stylized citation (default) in HTML format:
```text
curl -s -H "Accept: text/html" -X GET https://cite.edirepository.org/cite/edi.460.1

Armitage, A.R., C.A. Weaver, J.S. Kominoski, and S.C. Pennings. 2020. Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019 ver 1. Environmental Data Initiative. <a href='https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6'>https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6</a>. Accessed 2020-01-28.
```
4 - Retrieve "BIBTEX" stylized citation in plain text format:
```text
curl -H "Accept: text/plain" -s -X GET "https://cite.edirepository.org/cite/edi.460.1?style=BIBTEX"

@misc{edi.460.1,
    author={Anna R Armitage and Carolyn A Weaver and John S Kominoski and Steven C Pennings},
    title={{Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019. ver 1}},
    year={2020},
    howpublished={{Environmental Data Initiative}},
    note={Online: https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6 (2020-02-05)}
}
```

5 - Retrieve "RAW" citation in JSON format:
```text
curl -s -H "Accept: application/json" -X GET https://cite.edirepository.org/cite/edi.460.1?style=RAW

{
  "citation": {
    "title": "Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019",
    "pubdate": "2020-01-21",
    "version": "1",
    "doi": "doi:10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6",
    "authors": [
      {
        "individual_names": [
          {
            "sur_name": "Armitage",
            "given_names": [
              "Anna",
              "R"
            ]
          }
        ],
        "organization_names": [
          "Texas A&M University at Galveston"
        ],
        "position_names": []
      },
      {
        "individual_names": [
          {
            "sur_name": "Weaver",
            "given_names": [
              "Carolyn",
              "A"
            ]
          }
        ],
        "organization_names": [
          "Texas A&M University - Corpus Christi"
        ],
        "position_names": []
      },
      {
        "individual_names": [
          {
            "sur_name": "Kominoski",
            "given_names": [
              "John",
              "S"
            ]
          }
        ],
        "organization_names": [
          "Florida International University"
        ],
        "position_names": []
      },
      {
        "individual_names": [
          {
            "sur_name": "Pennings",
            "given_names": [
              "Steven",
              "C"
            ]
          }
        ],
        "organization_names": [
          "University of Houston"
        ],
        "position_names": []
      }
    ],
    "publisher": "Environmental Data Initiative"
  }
}


```


## A note about how Cite generates a citation

A Cite generated citation may consist of a list of authors, publication year, title, data package version, publisher, digital object identifier, and access date. The order and presence of these components depends on the style requested for the citation (see "style" parameter above).

The JSON content of an ESIP style citation, and a brief discussion of the fields, follows:

```
{
    "authors": "Armitage, A.R., C.A. Weaver, J.S. Kominoski, and S.C. Pennings.",
    "pub_year": "2020.",
    "title": "Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019",
    "version": "ver 1.",
    "publisher": "Environmental Data Initiative.",
    "doi": "https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6.",
    "accessed": "Accessed 2020-01-29."
}
```

- **Authors** - Cite uses content extracted from the science metadata described by an
[Ecological Metadata Language](https://eml.ecoinformatics.org) (EML) document
to generate the *author list*. Specifically, Cite uses the [*creator*](https://eml.ecoinformatics.org/schema/eml-resource_xsd.html#ResourceGroup_creator) section of EML. The EML *creator* element is divided into three primary secitons: individuals, organizations, and positions (i.e., roles) - see below.

    Cite uses indviduals, followed by organizations, as the authors. If neither individuals or organizations are present, it will use a position. Cite also assumes that a creator element contains information pertaining to only a single "creator", although EML allows for multiple identities in a single creator element. This means that if an individual name is present within a *creator* element, Cite will ignore the organization or position names within the same element when creating the author list. Cite also respects the order of *creator* elements as presented in the EML. As such, Cite will order the author list beginning with individuals, and followed by organizations, according to the order in the EML. To remphasize, Cite will only display a position name if there are no individuals or organizations defined in the *creator* section of the EML.

<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/cite/master/eml-resource_xsd_Element_creator.png"/></p>

- **Publication Year** - The *publication year* is defined by the date when
 the data package was archived into the EDI data repository and only displays the year of publication. This publication date may differ from the publication date entered into the EML, which often marks when it became a public data package, although yet archived into a public repository.

- **Title** - Cite uses the *title* section of EML as the citation title. EML *title* elements are copied verbatim into the citation.

- **Version Number** -The citation *version number* represents the revision step (or increment) of the data package as archived in the EDI data repository. Revision values are whole numbers and have a one-to-one correspondence to the revision of the data package in the repository.

- **Publisher** - By default, the *publisher* field of the citation is always to the Environmental Data Initiative. This value will not change during the tenure of the EDI data repository.

- **DOI** -The *Digital Object Identifier* (DOI) will consist of the EDI DOI value that is registered with DataCite, and is displayed using the fully qualified "doi.org" URL. This DOI URL will resolve to the corresponding "landing page" of the data package as displayed on the EDI Data Portal.

- **Access Date** - Finally, the *access date* displays the date in which the citation was generated, assuming that it serves as a proxy for the date in which the data package was viewed.

