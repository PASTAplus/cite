# cite
A data citation generator for PASTA+ data packages

## About

The Cite web service is a managed service of the Environmental Data Initiative (EDI). Cite generates formatted citations for scientific data packages archived in the PASTA+ data repository. Cite provides a simple to use REST end-point:

```https://cite.edirepository.org/cite/<pid>```

where "pid" is a PASTA package identifier.

## Query parameters

Cite accepts the following options as query parameters with the request URL:

- __*access*__ - Return a datestamp in the citation of the current UTC date (see below). This is recommended by the ESIP citation style guide.

    ```text
    ?<access>
    ```
 
- __*env*__ - Set the PASTA archive environment in which the citation request is to be processed (the default environment is *production*).

    ```text
    ?<env>=[production(default), staging, development]
    ```

- __*style*__ - Set the style for which to format the citation (the default style is *ESIP*).

    ```text
    ?<style>=[ESIP(default), DRYAD, BIBTEX, RAW]
    ```
  
- __*ignore*__ - Ignore INDIVIDUALS, ORGANIZATIONS, or POSITIONS in author list.

    ```text
    ?<ignore>=[INDIVIDUALS, ORGANIZATIONS, POSITIONS]
    ```

## Response body formatting

The response body format is controlled by the request "Accept" header value. Recognized media-types are: `text/plain`, `text/html`, and `application/json` (note: media-types with parameters are not considered).

## Examples:
1 - Retrieve "ESIP" stylized citation (default) in plain text format:
```text
curl -s -H "Accept: text/plain" -X GET https://cite.edirepository.org/cite/edi.460.1?access

Armitage, A.R., C.A. Weaver, J.S. Kominoski, and S.C. Pennings. 2020. Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019 ver 1. Environmental Data Initiative. https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6. Accessed 2020-01-28.
```
2 -  Retrieve "DRYAD" stylized citation in plain text format:
```text
curl -s -H "Accept: text/plain" -X GET https://cite.edirepository.org/cite/edi.460.1?style=DRYAD

Armitage AR, Weaver CA, Kominoski JS, and Pennings SC (2020) Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019. Environmental Data Initiative. https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6
```
3 - Retrieve "ESIP" stylized citation (default) in HTML format:
```text
curl -s -H "Accept: text/html" -X GET https://cite.edirepository.org/cite/edi.460.1?access

Armitage, A.R., C.A. Weaver, J.S. Kominoski, and S.C. Pennings. 2020. Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019 ver 1. Environmental Data Initiative. <a href='https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6'>https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6</a>. Accessed 2020-01-28.
```
4 - Retrieve "BIBTEX" stylized citation in plain text format:
```text
curl -H "Accept: text/plain" -s -X GET "https://cite.edirepository.org/cite/edi.460.1?style=BIBTEX&access"

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
```

6 - Using PHP to retrieve the default ESIP style with the access date (sans the response):

```
$url_get_citation = "https://cite.edirepository.org/cite/knb-lter-ntl.".$datasetID.".".$revision."?access";
$headers = array(
               'Accept: text/html'
               );
$curl_cit = curl_init();
curl_setopt_array($curl_cit, [
               CURLOPT_RETURNTRANSFER => 1,
               CURLOPT_URL => $url_get_citation,
               CURLOPT_HTTPHEADER => $headers
               ]);
$result = curl_exec($curl_cit);
curl_close($curl_cit);
```

## A note about how Cite generates a citation

A Cite generated citation may consist of a list of authors, publication year, title, data package version, publisher, digital object identifier, and access date. The order and presence of these components depends on the style requested for the citation (see query parameters above).

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
to generate the *author list*. Specifically, Cite uses the [*creator*](https://eml.ecoinformatics.org/schema/eml-resource_xsd.html#ResourceGroup_creator) section of EML to generate the list of authors, including *individuals*, *organizations*, and *positions*.

    Cite preserves the order of the *creator* list as defined within the EML document. As such, if you would like the citation to begin with an organization name, you should position the *creator* element that describes the organization at the beginning of the *creator* list in the EML document.

    Cite also assumes that a creator element contains information pertaining to only a single "creator", although EML allows for multiple identities in a single creator element. Cite will do its best to accommodate multi-named subjects within a *creator* element, but mileage will vary. 
        
    Cite is opinionated in how it determines an author: individuals, take precedence over organizations and positions, and organizations take precedence over positions. What this means is if an *individual* and *organization* and *position* are all defined in a single *creator* element, Cite sets the author to the named information within the *individual* element; and, if only an *organization* and *position* exist within a single *creator* element, Cite will set the author to the named information within the *organization* element. Finally, if only a *position* is defined within a single *creator* element, Cite will set the author to the named information within the *position* element. It is important to note that Cite respects the *creator* content as defined in the EML document and will set a *position* name to an author if it is present and meets the above hierarchy. If you believe that a *position* should not be displayed as data package author, then you should not include it as a data package creator.

    Finally, Cite does not collect or use tertiary information (e.g., phone number, addresses, emails) from within the *creator* element since this type of information is not used as part of a data package citation.

    
<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/cite/master/images/eml-resource_xsd_Element_creator.png"/></p>

- **Publication Year** - The *publication year* is defined by the calendar year when the data package was archived into the EDI data repository. The publication year may differ from the year of the publication date entered into the EML, which is often set to the date when the data package became publicly available, although not yet archived into the EDI data repository.

- **Title** - Cite uses the *title* section of EML as the citation title. EML *title* elements are copied verbatim into the citation.

- **Version Number** -The citation *version number* represents the revision step (or increment) of the data package as archived in the EDI data repository. Revision values are whole numbers and have a one-to-one correspondence to the revision of the data package in the repository.

- **Publisher** - By default, the *publisher* field of the citation is permanently set to "Environmental Data Initiative". This value will not change during the tenure of the EDI data repository.

- **DOI** -The *Digital Object Identifier* (DOI) is the EDI generated DOI value that is registered with DataCite, and is displayed using the fully qualified "doi.org" URL. This DOI URL will resolve to the corresponding "landing page" of the data package as displayed on the EDI Data Portal.
 
- **Access Date** - The *access date* is the UTC date in which the citation was requested.

## References

ESIP Data Preservation and Stewardship Committee (2019): Data Citation Guidelines for Earth Science Data, Version 2. ESIP. Online resource. https://doi.org/10.6084/m9.figshare.8441816.v1 
