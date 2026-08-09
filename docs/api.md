# API Documentation

> REST API endpoints for the AI Talent Router.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints require a Bearer token from Clerk:

```
Authorization: Bearer <clerk_jwt_token>
```

## Endpoints

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/me` | Get current user info |

### Candidates

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/candidates` | Create candidate profile |
| GET | `/candidates` | List candidates (paginated) |
| GET | `/candidates/search` | Search candidates |
| GET | `/candidates/{id}` | Get candidate by ID |
| PATCH | `/candidates/{id}` | Update candidate |
| POST | `/candidates/{id}/projects` | Add project |
| GET | `/candidates/{id}/projects` | List projects |
| POST | `/candidates/{id}/work-history` | Add work history |
| GET | `/candidates/{id}/work-history` | List work history |
| POST | `/candidates/{id}/recommendations` | Add recommendation |
| GET | `/candidates/{id}/skills` | List skills |

### Companies

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/companies` | Create company |
| GET | `/companies` | List companies |
| GET | `/companies/{id}` | Get company |
| PATCH | `/companies/{id}` | Update company |

### Jobs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/jobs` | Create job |
| GET | `/jobs` | List jobs |
| GET | `/jobs/search` | Search jobs |
| GET | `/jobs/{id}` | Get job |
| PATCH | `/jobs/{id}` | Update job |
| POST | `/jobs/{id}/publish` | Publish draft |
| POST | `/jobs/{id}/close` | Close job |

### Resumes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/resumes/upload` | Upload resume |
| GET | `/resumes` | List resumes |
| GET | `/resumes/{id}` | Get resume |

### GitHub

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/github/connect` | Connect GitHub account |
| GET | `/github` | Get GitHub profile |

### Portfolios

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/portfolios` | Add portfolio |
| GET | `/portfolios` | List portfolios |
| GET | `/portfolios/{id}` | Get portfolio |

### Videos

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/videos/upload` | Upload video |
| GET | `/videos` | List videos |
| GET | `/videos/{id}` | Get video |

### Certificates

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/certificates` | Add certificate |
| POST | `/certificates/upload` | Upload certificate file |
| GET | `/certificates` | List certificates |
| GET | `/certificates/{id}` | Get certificate |

### Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search/candidates` | Keyword search candidates |
| POST | `/search/jobs` | Keyword search jobs |

### Matching

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/matching/run` | Run matching pipeline |
| GET | `/matching/jobs/{id}` | Get job matches |
| PATCH | `/matching/matches/{id}` | Update match status |

### Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/stats` | Platform statistics |
| GET | `/admin/users` | List all users |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| GET | `/health/ready` | Readiness probe |

## Pagination

List endpoints accept `page` (default: 1) and `size` (default: 20, max: 100).

Response format:
```json
{
  "items": [],
  "total": 100,
  "page": 1,
  "size": 20,
  "pages": 5
}
```

## Error Responses

```json
{
  "error": "Not found",
  "request_id": "uuid"
}
```
