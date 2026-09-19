# API client

`client.js` contains the Axios contract for the backend `/api/v1` endpoints.

Set `VITE_API_BASE_URL` when the backend is not available at
`http://localhost:8000/api/v1`.

The PDF helper requests a binary `blob` response. Business-plan generation and
PDF export can return backend errors such as `422`, `503`, or `500`; callers
must handle rejected Axios promises explicitly.
