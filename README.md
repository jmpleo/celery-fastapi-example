```bash
docker compose up -d
```

### GET: /start

```bash
curl -X GET "http://localhost:8000/start?n=10"
```
```json
{
  "error": "",
  "data": {
    "task_id": "043bd852-8d13-4540-b67a-0143000fba13"
  }
}
```

### POST: /start
```bash
curl -X POST "http://localhost:8000/start" -H "Content-Type: application/json" -d '{"ns": [10, 15, 20]}'
```
```json
{
  "error": "",
  "data": {
    "group_id": "30f02097-b50b-4af0-8fd2-76325ae3d71b"
  }
}
```

### GET: /task
```bash
curl -X GET "http://localhost:8000/task/043bd852-8d13-4540-b67a-0143000fba13"
```
```json
{
  "error": "",
  "data": {
    "ready": true,
    "result": [7,6,1,9,4,8,6,8,10,10]
  }
}
```

### GET: /task
```bash
curl -X GET "http://localhost:8000/task"
```
```json
{
  "error": "",
  "data": {
    "043bd852-8d13-4540-b67a-0143000fba13": {
      "ready": true,
      "result": null
    },
    "b551108b-02bc-432c-ba21-430526e56464": {
      "ready": true,
      "result": null
    }
  }
}
```

### GET: /groups
```bash
curl -X GET "http://localhost:8000/group/30f02097-b50b-4af0-8fd2-76325ae3d71b"
```
```json
{
  "error": "",
  "data": {
    "ready": true,
    "progress": 3,
    "results": {
      "6cbd2d15-d9b2-42c6-a882-731ab116dbce": [
        10,9,5,0,7,8,6,4,2,8
      ],
      "8c266347-58e2-4130-a435-d32cab0eadb1": [
        2,7,6,14,8,6,14,0,4,2,8,5,1,2,9
      ],
      "a6eeb23e-fe79-4c7d-a579-d9036285a0a4": [
        6,2,12,12,13,0,16,10,4,14,19,4,3,14,4,1,10,10,7,15
      ]
    }
  }
}

```

### GET: /group
```bash
curl -X GET "http://localhost:8000/group"
```
```json
{
  "error": "",
  "data": {
    "1231bbbf-e7e5-487f-9713-abc4c176937f": {
      "ready": true,
      "progress": 3
    },
    "61e4b8e3-ff7b-4d0c-a124-da0ebb492333": {
      "ready": true,
      "progress": 3
    },
    "f4a89450-9d3f-4195-ab92-953db429c7f2": {
      "ready": true,
      "progress": 3
    }
  }
}
```
