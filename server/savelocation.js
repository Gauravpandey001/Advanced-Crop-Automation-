const fs = require('fs');
const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  if (pathname === '/saveLocation' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      const locationData = JSON.parse(body);
      saveToFile(locationData);
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end('Location saved successfully!');
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found');
  }
});

function saveToFile(locationData) {
  const fileName = 'locations.json';
  const data = JSON.stringify(locationData);
  fs.writeFileSync(fileName, data);
}

const port = 3000;
server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
