# BAS Style Kit File Upload Endpoint - Usage

**Note:** This is temporary documentation, it will be replaced with external documentation soon.

This API follows the [JSON API](http://jsonapi.org/format/1.0/) standard.

## Form actions

The methods provided by this API are intended to be used as form actions. 

You must use the `multipart/form-data` encoding type to submit files.

E.g.

```html
<form method="POST" enctype="multipart/form-data" action="https://bas-style-kit-file-upload.herokuapp.com/upload-single">
</form>
```

## Uploaded files

Uploaded files are not stored or read by this API. Nevertheless do not upload files containing sensitive information.

## Upload limit

Requests with a content length greater than `10485760` bytes (*10mb*) will be rejected by this API with a 
[413 Request Entity Too Large](#413-request-entity-too-large) error.

## CORS

This API supports [Cross Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).

### Preflight requests

All methods support preflight requests as per the CORS standard using the `OPTIONS` verb.

### Allowed headers

In addition to the headers allowed in 
[simple requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#Simple_requests):

* `Cache-Control`
* `X-Requested-With`

### Allowed methods/verbs

* `OPTIONS`
* `GET`
* `POST`

**Note:** Only the supported verbs for a method. I.e. for a `GET` method, only `GET, OPTIONS` will be returned.

### Allowed origins

* `http://localhost:9000` (for local versions of the Style Kit and Style Kit documentation)
* `https://style-kit.web.bas.ac.uk`
* `https://style-kit-testing.web.bas.ac.uk`
* `https://style-kit-testbed.web.bas.ac.uk`

The wildcard (`*`) origin is not supported.

**Note:** Only the relevant origin will be listed in the `Access-Control-Allow-Origin` header as not all browsers 
support multiple values. A `Vary` header is set to indicate this value may change on each response and should not be 
cached.

## Errors

Errors reported by this API follow the [JSON API](http://jsonapi.org/format/1.0/#errors) standard.

Many errors are used across the API and are documented centrally in this section.

The `id` property will vary with each error using a UUID version 4, the values shown are examples.

### `400 file field missing in request`

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

### `400 file field value is an empty selection`

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

### `413 - Request Entity Too Large`

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

### `/upload-single`

Upload a single file.

#### Request

Type: [Form data](#form-actions)

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

### `/upload-multiple`

Upload multiple files.

#### Request

Type: [Form data](#form-actions)

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

### `/upload-single-restricted-size`

Upload a singe file with a lower than normal maximum size.

The upload limit for this resource method is restricted to *40kb* to test uploads that are too large. Normally the
regular [Upload limit](#upload-limit) applies.

#### Request

Type: [Form data](#form-actions)

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

### `/upload-single-restricted-mime-types`

Upload a single file restricted to a single file type (`image/jpeg`).

Iploaded files are restricted to a single MIME type (file type), `image/jpeg`, to test uploads that are of the wrong 
type. Normally any type of file can be uploaded.

#### Request

Type: [Form data](#form-actions)

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
      }
      "status": 415,
      "title": "File type uploaded is not allowed"
    }
  ]
}
```
