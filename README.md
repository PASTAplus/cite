# cite
A data citation generator for PASTA data packages

Cite is a web service data citation generator for data packages found in the
Environmental Data Initiative's (EDI) PASTA data repository. Cite provides a simple
to use REST end-point:

```https://cite.edirepository.org/cite/<pid>```

where "pid" is a PASTA package identifier. Cite accepts the following options
 as query parameters on the request URL:
 
```?<env>=[production(default), staging, development]```

```?<style>=[ESIP(default), DRYAD]```

The response body format is controlled by the request "Accept" header value. 
Recognized media-types are: `text/plain`, `text/html`, and `application/json`
(note: media-types with parameters are not considered).

## Examples:

```text
curl -i -H "Accept: text/plain" -X GET https://cite.edirepository.org/cite/edi.460.1
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 28 Jan 2020 19:29:17 GMT
Content-Type: text/plain
Content-Length: 275
Connection: keep-alive

Armitage, A.R., C.A. Weaver, J.S. Kominoski, and S.C. Pennings. 2020. Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019 ver 1. Environmental Data Initiative. https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6. Accessed 2020-01-28.
```

```text
curl -i -H "Accept: text/plain" -X GET https://cite.edirepository.org/cite/edi.460.1?style=DRYAD
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 28 Jan 2020 19:30:48 GMT
Content-Type: text/plain
Content-Length: 238
Connection: keep-alive

Armitage AR, Weaver CA, Kominoski JS, and Pennings SC (2020) Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019. Environmental Data Initiative. https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6
```

```text
curl -i -H "Accept: text/html" -X GET https://cite.edirepository.org/cite/edi.460.1
HTTP/1.1 200 OK
Server: nginx/1.10.3 (Ubuntu)
Date: Tue, 28 Jan 2020 19:31:27 GMT
Content-Type: text/html
Content-Length: 352
Connection: keep-alive

Armitage, A.R., C.A. Weaver, J.S. Kominoski, and S.C. Pennings. 2020. Hurricane Harvey: Coastal wetland plant responses and recovery in Texas: 2014-2019 ver 1. Environmental Data Initiative. <a href='https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6'>https://doi.org/10.6073/pasta/e288ccaf55afceecc29bdf0a341248d6</a>. Accessed 2020-01-28.
```

## A note about how Cite generates a citation

A Cite generated citation may consist of a list of authors, publication date, title, data package version, publisher, digital object identifier, and access date (see below). The order and presence of these components depends on the style requested for the citation (see "style" parameter above).

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

Cite uses content extracted from the science metadata described by an
[Ecological Metadata Language](https://eml.ecoinformatics.org) (EML) document
to generate the author list. Specifically, Cite uses the [*creator*](https://eml.ecoinformatics.org/schema/eml-resource_xsd.html#ResourceGroup_creator) section of EML. The EML *creator* element is divided into three primary secitons: individuals, organizations, and positions (i.e., roles) - see below.

<p align="center"><img src="https://raw.githubusercontent.com/PASTAplus/cite/master/eml-resource_xsd_Element_creator.png"/></p>

- **Authors** - Cite uses indviduals, followed by organizations, as the authors. If neither individuals or organizations are present, it will use a position. Cite also assumes that a creator element contains information pertaining to only a single "creator", although EML allows for multiple identities in a single creator element. This means that if an individual name is present within a *creator* element, Cite will ignore the organization or position names within the same element when creating the author list. Cite also respects the order of *creator* elements as presented in the EML. As such, Cite will order the author list beginning with individuals, and followed by organizations, according to the order in the EML. To remphasize, Cite will only display a position name if there are no individuals or organizations defined in the *creator* section of the EML.

- **Publcation Date** - The *publication date* is defined by the date when the data package was archived into the EDI data repository and only displays the year of publication. This publication date may differ from the publication date entered into the EML, which often marks when it became a public data package, although yet archived into a public repository.

- **Title** - Cite uses the *title* section of EML as the citation title. EML *title* elements are copied verbatim into the citation.

- **Version Number** -The citation *version number* represents the revision step (or increment) of the data package as archived in the EDI data repository. Revision values are whole numbers and have a one-to-one correspondence to the revision of the data package in the repository.

- **Publisher** - By default, the *publisher* field of the citation is always to the Environmental Data Initiative. This value will not change during the tenure of the EDI data repository.

- **DOI** -The *Digital Object Identifier* (DOI) will consist of the EDI DOI value that is registered with DataCite, and is displayed using the fully qualified "doi.org" URL. This DOI URL will resolve to the corresponding "landing page" of the data package as displayed on the EDI Data Portal.

- **Access Date** - Finally, the *access date* displays the date in which the citation was generated, assuming that it serves as a proxy for the date in which the data package was viewed.

