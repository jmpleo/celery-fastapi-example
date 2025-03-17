## Async celery worker example


### GET: /start
```bash
curl -X GET "http://localhost:8000/start?q=query"
```
```json
{"task_id":"a22c1d86-b928-4c3e-bbf4-a1d6d9edc196"}
```

### GET: /task
```bash
curl -X GET "http://localhost:8000/task/a22c1d86-b928-4c3e-bbf4-a1d6d9edc196"
```
```json
{"status":"PENDING"}
```

### POST: /start
```bash
curl -X POST "http://localhost:8000/start" -H "Content-Type: application/json" -d '{"qs": ["query1", "query2", "query3"]}'
```
```json
{"status":"PENDING"}
```

### GET: /groups
```bash
curl -X GET "http://localhost:8000/groups"
```
```json
{
  "2ceb12ec-0a05-4adf-bdbb-42ac39dae539": {
    "c918732d-0fe6-4c19-b927-28182d9e46e3": {
      "status": "SUCCESS"
    },
    "e07bd4c7-a8d1-4b45-aff8-4aeb3d4b75d5": {
      "status": "SUCCESS"
    },
    "9772f439-d035-4890-8b9e-387a6e078485": {
      "status": "SUCCESS"
    }
  }
}
```

### GET: /group
```bash
curl -X GET "http://localhost:8000/group/2ceb12ec-0a05-4adf-bdbb-42ac39dae539?expand=0"
```
```json
{"progress":3}
```

```bash
curl -X GET "http://localhost:8000/group/2ceb12ec-0a05-4adf-bdbb-42ac39dae539?expand=1"
```
```json
{
    "progress":3, "results": {
        "c918732d-0fe6-4c19-b927-28182d9e46e3": {
            // result here
        }
    }
}
```

### GET: /tasks
```bash
curl -X GET "http://localhost:8000/tasks"
```
```json
{
  "c918732d-0fe6-4c19-b927-28182d9e46e3": {
    "status": "SUCCESS"
  },
  "e07bd4c7-a8d1-4b45-aff8-4aeb3d4b75d5": {
    "status": "SUCCESS"
  },
  "9772f439-d035-4890-8b9e-387a6e078485": {
    "status": "SUCCESS"
  }
}
```