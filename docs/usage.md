# BAS Style Kit File Upload Endpoint - Usage

**Note:** This is temporary documentation, it will be replaced with external documentation soon.

This API follows the [JSON API](http://jsonapi.org/format/1.0/) standard, unless stated otherwise.

## General information

### Support

Limited, best effort, support is offered for those using this API to test file upload components within the BAS Style 
Kit.

This API is designed for testing and provided without any availability, reliability or performance guarantees.

Contact the [BAS Service Desk](mailto:servicedesk@bas.ac.uk) if this applies to you.

### Information handling

This API processes files upload to it in order to complete its function. During processing the type and size of uploaded
files is used and may be returned in an error response to assist the user to use this API.

This API does not store uploaded files, or access their contents. Once processed, files cannot be accessed.

Information transmitted to and from this API is protected using HTTPS. We ensure any third party services, such as 
hosting platforms or monitoring and analytics tools, have measures in place to protect information they host or we 
provide to them, and we ensure such services are used appropriately for a necessary task.

Applicable services used by this API are:

* [Heroku](https://heroku.com) - for hosting the API
* [Sentry](https://sentry.io/) - for reporting API errors

**Note:** Despite these safeguards, this API is meant for testing any so sensitive information should not be uploaded.

This API is provided by the [British Antarctic Survey](https://www.bas.ac.uk), part of 
[UK Research and Innovation](https://www.ukri.org).

If you have any questions about how information is used by this API please contact the 
[BAS Service Desk](mailto:servicedesk@bas.ac.uk) in the first instance. If you do not receive a reply within a few days
please contact the [BAS Freedom of Information Officer](foi@bas.ac.uk).

### Security disclosures

Please report any security disclosures with this API to the [BAS Service Desk](mailto:servicedesk@bas.ac.uk).

Contact us for instructions if you need to report any sensitive information.

### Versioning policy

This API does not currently use versioning.

As this API is designed for testing, it may change significantly over time. Where possible backwards compatibility will
be preserved but this is not guaranteed.

## Technical information

### Base URL

The base URL is `https://bas-style-kit-file-upload.herokuapp.com/`. 
**Note:** This API is only available over `HTTPS`.


### Content Types

This API supports the `application/json` content type only, unless stated otherwise.

This API supports `UTF-8` character encoding only, unless stated otherwise.

### Request IDs

All requests will include a `X-Request-ID` header to aid in debugging requests through different components.

If desired, a custom request ID can be specified by the client which will be used instead of, or in addition to a API
generated value.

**Note:** In some cases a client specified value will be ignored, ensure you do not rely on this value being returned.

**Note:** This header may include multiple values (multiple Request IDs) separated by a `,` with possible whitespace. 

### CORS

This API supports [Cross Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).

#### Preflight requests

All methods support preflight requests as per the CORS standard using the `OPTIONS` verb.

#### Allowed headers

In addition to the headers allowed in 
[simple requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#Simple_requests):

* `Cache-Control`
* `X-Requested-With`

#### Allowed methods/verbs

* `OPTIONS`
* `GET`
* `POST`

**Note:** Only the supported verbs for a method. I.e. for a `GET` method, only `GET, OPTIONS` will be returned.

#### Allowed origins

* `http://localhost:9000` (for local versions of the Style Kit and Style Kit documentation)
* `https://style-kit.web.bas.ac.uk`
* `https://style-kit-testing.web.bas.ac.uk`
* `https://style-kit-testbed.web.bas.ac.uk`

The wildcard (`*`) origin is not supported.

**Note:** Only the relevant origin will be listed in the `Access-Control-Allow-Origin` header as not all browsers 
support multiple values. A `Vary` header is set to indicate this value may change on each response and should not be 
cached.

### Upload limit

Requests with a content length greater than `10485760` bytes (*10mb*) will be rejected by this API with a 
[413 Request Entity Too Large](#413-request-entity-too-large) error.

## Errors

Errors reported by this API follow the [JSON API](http://jsonapi.org/format/1.0/#errors) standard.

Many errors are used across the API and are documented centrally in this section.

The `id` property will vary with each error using a UUID version 4, the values shown are examples.

**Note:** Errors are captured by an error tracking service, you don't need to report them unless you wish to provide 
any additional information about an error.

### `400` - File field missing in request`

```json
{
  "errors": [
    {
      "detail": "Check the name of the field and that the request uses multipart/form-data encoding",
      "id": "a611b89f-f1bb-43c5-8efa-913c83c9109e",
      "status": 400,
      "title": "[file] field missing in request"
    }
  ]
}
```

### `400` - File field value is an empty selection`

```json
{
  "errors": [
    {
      "detail": "Check the file selected is specified correctly and is a valid file",
      "id": "a611b89f-f1bb-43c5-8efa-913c83c9109e",
      "status": 400,
      "title": "[file] field value is an empty selection"
    }
  ]
}
```

### `413` - Request Entity Too Large`

The `meta.request_content_length` property will vary on each error, the value below is an example.

```json
{
  "errors": [
    {
      "detail": "Check the content length of the request is less than the maximum allowed",
      "id": "a611b89f-f1bb-43c5-8efa-913c83c9109e",
      "meta": {
        "maximum_content_length_allowed": 10485760,
        "request_content_length": 10896534
      },
      "status": 413,
      "title": "Request content length is too great"
    }
  ]
}
```

## Resources

This API has no resources.

## Standalone methods

### HTML form actions

The upload methods provided by this API are intended to be used as form actions. 

You must use the `multipart/form-data` encoding/content type to upload files.

**Note:** Do not use the default `application/json` content type for form actions.

E.g.

```html
<form method="POST" enctype="multipart/form-data" action="https://bas-style-kit-file-upload.herokuapp.com/upload-single">
</form>
```

### [GET] `/`

Gives a high level summary of this API.

#### Request

Type: Empty

#### Response

##### `200 - OK`

Summary returned successfully.

```
{
  "meta": {
    "summary": "A minimal API implementing a simple form action for testing file upload components in the BAS Style Kit."
  }
}
```

### [POST] `/upload-single`

Upload a single file.

#### Request

Content type: [Form data](#form-actions)

##### Body form fields

| Form Field | Occurrence | Type        | Description   |
| ---------- | ---------- | ----------- | ------------- |
| `file`     | 1          | Binary/File | Uploaded file |

#### Response

##### `204 - No Content`

Submitted file received successfully.

##### `400 - Bad Request`

See Common errors for:

* [Missing file field](#400-file-field-missing-in-request)
* [Empty file selection](#400-file-field-value-is-an-empty-selection)

##### `413 - Request Entity Too Large`

See [Common error](#413-request-entity-too-large)

### [POST] `/upload-multiple`

Upload multiple files.

#### Request

Content type: [Form data](#form-actions)

##### Body form fields

| Form Field | Occurrence | Type        | Description    |
| ---------- | ---------- | ----------- | -------------- |
| `files`    | 1-n        | Binary/File | Uploaded files |

**Note:** The total of all files must be under the request [Upload limit](#upload-limit) (i.e. not per-file).

#### Response

##### `204 - No Content`

Submitted file received successfully.

##### `400 - Bad Request`

See Common errors for:

* [Missing file field](#400-file-field-missing-in-request) (references to `file` should be read as `files`)
* [Empty file selection](#400-file-field-value-is-an-empty-selection) (applies to one of the uploaded files)

##### `413 - Request Entity Too Large`

See [Common error](#413-request-entity-too-large)

### [POST] `/upload-single-restricted-size`

Upload a singe file with a lower than normal maximum size.

The upload limit for this resource method is restricted to *40kb* to test uploads that are too large. Normally the
regular [Upload limit](#upload-limit) applies.

#### Request

Content type: [Form data](#form-actions)

##### Body form fields

| Form Field | Occurrence | Type        | Description   |
| ---------- | ---------- | ----------- | ------------- |
| `file`     | 1          | Binary/File | Uploaded file |

#### Response

##### `204 - No Content`

Submitted file received successfully.

##### `400 - Bad Request`

See Common errors for:

* [Missing file field](#400-file-field-missing-in-request)
* [Empty file selection](#400-file-field-value-is-an-empty-selection)

##### `413 - Request Entity Too Large`

See [Common error](#413-request-entity-too-large) (references to the `maximum_content_length_allowed` should be `40960`)

### [POST] `/upload-single-restricted-mime-types`

Upload a single file restricted to a single file type (`image/jpeg`).

Iploaded files are restricted to a single MIME type (file type), `image/jpeg`, to test uploads that are of the wrong 
type. Normally any type of file can be uploaded.

#### Request

Content type: [Form data](#form-actions)

##### Body form fields

| Form Field | Occurrence | Type        | Description   |
| ---------- | ---------- | ----------- | ------------- |
| `file`     | 1          | Binary/File | Uploaded file |

#### Response

##### `204 - No Content`

Submitted file received successfully.

##### `400 - Bad Request`

See Common errors for:

* [Missing file field](#400-file-field-missing-in-request)
* [Empty file selection](#400-file-field-value-is-an-empty-selection)

##### `413 - Request Entity Too Large`

See [Common error](#413-request-entity-too-large)

##### `415 - Unsupported Media Type`

The `meta.instance_mime_type` property will vary on each error, the value below is an example.

```json
{
  "errors": [
    {
      "detail": "Check the file mime_type is in the list of allowed types",
      "id": "a611b89f-f1bb-43c5-8efa-913c83c9109e",
      "meta": {
        "allowed_mime_types": [
          "image/jpeg"
        ],
        "instance_mime_type": "image/png"
      },
      "status": 415,
      "title": "File type uploaded is not allowed"
    }
  ]
}
```
