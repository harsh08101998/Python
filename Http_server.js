const http = require("http");

const host = 'localhost';
const port = 8000;

const requestListener = function (req, res) {
    // res.setHeader("Content-Type", "application/json");  //-- for json
    res.setHeader("Content-Type", "text/plain");  // -- text/plain   -- text/csv
    // res.setHeader("Content-Disposition", "attachment;filename=oceanpals.csv");   // -- for sending csv file
    res.writeHead(200);
    console.log(req.url)
    res.end("My first server!");
};

const server = http.createServer(requestListener);
server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});