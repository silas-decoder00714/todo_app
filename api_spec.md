# Vote App API Specification
## HTML pages
> Home page
- Method: `GET`
- Path: `/`
- Response: `home page HTML`
---
> New Topic
- Method: `GET`
- Path: `/new`
- Response: `New Topic HTML`
---
> Vote Topic Page
- Method: `GET`
- Path: `/topic/<topic_id>`
	- variable: `topic_id`
- Response: `Vote topic HTML`

## API
> Add new topic
- Method: `POST`
- Path: `/newTopic`
- Request:
	- body:
```json
{
"name": "string"
}
```
- Response : `home page with updated topic list`
---
> Add choice to the topic
- Path : `/topic/<topic_id>/newChoice`
	- variable: `topic_id`
- Method: `POST`
- Request:
	- Body:
```json
{
"choice": "string"
}
```
- Response: `updated topic page`
---
> Vote for choice in topic
- Path: `/topic/<topic_id>/vote`
- Method: `POST`
- Request:
	- Body:
```json
{
"choice": "string"
}
```
- Response: `updated topic page`