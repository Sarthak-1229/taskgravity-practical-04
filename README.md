# Practical 04: Server-Side NodeJS Application

## TaskGravity — Core HTTP Modules, Server-Side Input Validation, Routing, and REST Endpoints

### 1. Overview
Practical 04 establishes the backend engineering foundation of TaskGravity using core Node.js runtime concepts without external frameworks.

### 2. Core Concepts Implemented
- **Native Modules**: `http`, `fs`, `path`, `url`, `querystring`.
- **Stream Processing**: Request payload buffering with memory flooding protection.
- **Server-Side Validation (`validator.js`)**:
  - `title`: String length bounds (3-80 chars) and non-empty checks.
  - `category`: Whitelist validation (`Frontend`, `Backend`, `Database`, `DevOps`, `Testing`, `UI/UX`).
  - `priority`: Whitelist validation (`Low`, `Medium`, `High`, `Urgent`).
  - `dueDate`: ISO date format validation and past-date rejection.
  - `estimatedHours`: Positive numeric bounds (1-100 hours).
  - `description`: String cap at 300 characters.
- **HTTP Status Codes**:
  - `200 OK`: Successful data retrieval (`GET /api/tasks`, `GET /api/stats`).
  - `201 Created`: Successful server validation and task insertion (`POST /api/tasks`).
  - `400 Bad Request`: Field-specific server validation failure response.
  - `404 Not Found`: Unmatched static paths or missing task IDs.
  - `500 Internal Server Error`: Stream or file I/O errors.

### 3. Execution
```bash
cd Practical4
npm start
```
Server starts on `http://localhost:4000`. Open in browser to test the interactive client and validation responses.
