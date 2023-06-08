const express = require("express");
const bodyParser = require("body-parser");
var MongoClient = require('mongodb').MongoClient;
const mongoMod = require('./test');
const { spawn } = require('child_process');

const client = new MongoClient("mongodb://localhost:27017");

const app = express();

app.use(express.static('/public'));

app.set('view engine', 'ejs');

// urlencoded parses html stuff
app.use(bodyParser.urlencoded({extended: true}))

app.get("/", function (req,res){
    //res.sendFile(__dirname + "/index.html")
    res.render('search');
})


app.post("/", function (req,res){
    const query = String(req.body.queryString);
    const n = req.body.slider;
    res.redirect('/result?input='+ query + '&n=' + n);

})

// app.get("/result", function (req, res) {
//   const query = req.query.input;
//     var result = mongoMod.run(query).catch(console.dir);
//     result.then(function(result) {
//         res.render('results',{result,query});
//     })
// })

// Undo the comment on top to revert back to previous version

app.get("/result", function (req, res) {
    const query = req.query.input;
    const n = req.query.n;
    // var result = mongoMod.run(query).catch(console.dir);
    const pythonProcess = spawn('python', ['indexingEngine.py', query, n]);
    let output = '';
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });
    pythonProcess.on('close', (code) => {
        if (code === 0) {
          console.log('Python program executed successfully.');
          console.log('Output:', output);
          const result = JSON.parse(output);
          res.render('results',{result,query,n});
        } else {
          console.error('Python program exited with error code:', code);
        }
    });
    // result.then(function(result) {
    //     res.render('results',{result,query});
    // })
})


app.get("/libraries", function (req,res){
    //res.sendFile(__dirname + "/index.html")
    res.render('searchLibraries');
})


app.post("/libraries", function (req,res){
    const query = String(req.body.queryString);
    const n = req.body.slider;
    res.redirect('/librariesResult?input='+ query + '&n=' + n);
})



app.get("/librariesResult", function (req, res) {
    const query = req.query.input;
    const n = req.query.n;
    // var result = mongoMod.run(query).catch(console.dir);
    const pythonProcess = spawn('python', ['indexingEnginePyPi.py', query, n]);
    let output = '';
    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });
    pythonProcess.on('close', (code) => {
        if (code === 0) {
          console.log('Python program executed successfully.');
          console.log('Output:', output);
          const result = JSON.parse(output);
          res.render('resultsLibraries',{result,query});
        } else {
          console.error('Python program exited with error code:', code);
        }
    });
    // result.then(function(result) {
    //     res.render('results',{result,query});
    // })
})


app.listen(process.env.PORT || 3000, function (){
    console.log ('\nServer set up on port 3000')
});
