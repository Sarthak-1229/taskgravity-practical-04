/**
 * Practical 04: Server-Side NodeJS Application (Core HTTP Modules)
 * Handles GET & POST requests, server-side input validation, static file serving, and REST endpoints.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { validateTaskPayload } = require('./validator');

const PORT = process.env.PORT || 4000;
const PUBLIC_DIR = path.join(__dirname, 'public');

// In-Memory Data Store (Preloaded with realistic seed tasks)
let tasks = [
  {
    id: 'tg-node-101',
    title: 'Core HTTP Request Router Implementation',
    category: 'Backend',
    priority: 'Urgent',
    dueDate: '2026-11-20',
    estimatedHours: 4,
    description: 'Implement stream chunk parsing and URL query string routing in native Node.js.',
    status: 'completed',
    createdAt: new Date().toISOString()
  },
  {
    id: 'tg-node-102',
    title: 'Server-Side Input Sanitization Pipeline',
    category: 'Backend',
    priority: 'High',
    dueDate: '2026-11-23',
    estimatedHours: 5,
    description: 'Enforce boundary checks on date formats, string lengths, and numeric parameters.',
    status: 'in-progress',
    createdAt: new Date().toISOString()
  },
  {
    id: 'tg-node-103',
    title: 'HTTP Status Code & Error Standardization',
    category: 'Testing',
    priority: 'Medium',
    dueDate: '2026-11-25',
    estimatedHours: 3,
    description: 'Format standard JSON error envelopes for 400 Bad Request and 404 Not Found responses.',
    status: 'pending',
    createdAt: new Date().toISOString()
  }
];

// Helper: Send JSON Response
function sendJSON(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  });
  res.end(JSON.stringify(data));
}

// Helper: Serve Static File
function serveStatic(req, res, filePath, contentType) {
  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
      } else {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('500 Internal Server Error');
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
}

// Helper: Parse Request Body (Buffer stream)
function parseRequestBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
      // Guard against payload flooding (max 1MB)
      if (body.length > 1e6) {
        req.connection.destroy();
        reject(new Error('Payload Too Large'));
      }
    });
    req.on('end', () => {
      if (!body) return resolve({});
      try {
        // Try parsing JSON first
        resolve(JSON.parse(body));
      } catch (e) {
        // Fallback to URL-encoded form data
        const querystring = require('querystring');
        resolve(querystring.parse(body));
      }
    });
    req.on('error', err => reject(err));
  });
}

// Main HTTP Server
const server = http.createServer(async (req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;
  const method = req.method;

  // Handle CORS Preflight
  if (method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    });
    return res.end();
  }

  // -------------------------------------------------------------
  // API ROUTING: GET Requests
  // -------------------------------------------------------------
  if (method === 'GET' && pathname === '/api/tasks') {
    const { status, category } = parsedUrl.query;
    let result = [...tasks];

    if (status && status !== 'all') {
      result = result.filter(t => t.status === status);
    }
    if (category && category !== 'all') {
      result = result.filter(t => t.category === category);
    }

    return sendJSON(res, 200, {
      success: true,
      count: result.length,
      data: result
    });
  }

  if (method === 'GET' && pathname === '/api/stats') {
    const total = tasks.length;
    const completed = tasks.filter(t => t.status === 'completed').length;
    const inProgress = tasks.filter(t => t.status === 'in-progress').length;
    const pending = tasks.filter(t => t.status === 'pending').length;

    return sendJSON(res, 200, {
      success: true,
      stats: {
        total,
        completed,
        inProgress,
        pending,
        velocity: total > 0 ? Math.round((completed / total) * 100) : 0
      }
    });
  }

  if (method === 'GET' && pathname.startsWith('/api/tasks/')) {
    const id = pathname.split('/')[3];
    const task = tasks.find(t => t.id === id);
    if (!task) {
      return sendJSON(res, 404, {
        success: false,
        error: `Task with id '${id}' was not found.`
      });
    }
    return sendJSON(res, 200, { success: true, data: task });
  }

  // -------------------------------------------------------------
  // API ROUTING: POST Requests (with Server-Side Validation)
  // -------------------------------------------------------------
  if (method === 'POST' && pathname === '/api/tasks') {
    try {
      const payload = await parseRequestBody(req);

      // Execute Server-Side Validation Module
      const validation = validateTaskPayload(payload);

      if (!validation.isValid) {
        return sendJSON(res, 400, {
          success: false,
          message: 'Server-side validation failed. Please correct input errors.',
          errors: validation.errors
        });
      }

      // Payload is validated; construct task record
      const newTask = {
        id: 'tg-node-' + Date.now().toString().slice(-4),
        title: payload.title.trim(),
        category: payload.category,
        priority: payload.priority,
        dueDate: payload.dueDate,
        estimatedHours: Number(payload.estimatedHours),
        description: (payload.description || '').trim(),
        status: 'pending',
        createdAt: new Date().toISOString()
      };

      tasks.unshift(newTask);

      return sendJSON(res, 201, {
        success: true,
        message: 'Task successfully created and validated on server.',
        data: newTask
      });
    } catch (err) {
      return sendJSON(res, 500, {
        success: false,
        error: 'Failed to process request: ' + err.message
      });
    }
  }

  // -------------------------------------------------------------
  // STATIC ASSETS ROUTING
  // -------------------------------------------------------------
  if (method === 'GET') {
    if (pathname === '/' || pathname === '/index.html') {
      return serveStatic(req, res, path.join(PUBLIC_DIR, 'index.html'), 'text/html');
    }
    if (pathname === '/styles.css') {
      return serveStatic(req, res, path.join(PUBLIC_DIR, 'styles.css'), 'text/css');
    }
    if (pathname === '/app.js') {
      return serveStatic(req, res, path.join(PUBLIC_DIR, 'app.js'), 'application/javascript');
    }
  }

  // Fallback 404
  return sendJSON(res, 404, {
    success: false,
    error: `Route '${method} ${pathname}' does not exist on this server.`
  });
});

if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`[TaskGravity Core Node Server] Running on http://localhost:${PORT}`);
  });
}

module.exports = server;
