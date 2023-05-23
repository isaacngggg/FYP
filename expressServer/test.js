

var MongoClient = require('mongodb').MongoClient;
// Replace the uri string with your MongoDB deployment's connection string.

var client = new MongoClient("mongodb://localhost:27017");

async function run(userInput) {
  try {
    const client = new MongoClient("mongodb://localhost:27017");
    var resultArray = [];
    var input = userInput
    const database = client.db("scrapped-function");
    const collection = database.collection("all");
    // query for movies that have a runtime less than 15 minutes
    const query = {"title": new RegExp('.*' + input + '.*','i')};
    const options = {
      // sort returned documents in ascending order by title (A->Z)
      sort: { title: 1 },
      // Include only the `title` and `imdb` fields in each returned document
      projection: { _id: 0, title: 1, description: 1, url: 1  },
    };

    const cursor = collection.find(query, options);
    // print a message if no documents were found
    if ((await collection.countDocuments(query)) === 0) {
      console.log("No documents found!");
      const resultItem = {
          title: "No documents found",
          description: "search again",
        };
      resultArray.push(resultItem);
    }
    // replace console.dir with your callback to access individual elements
    await cursor.forEach((doc) => {
        //console.log(doc.title);
        //console.log(doc.description);
        const resultItem = {
            title: doc.title,
            description: doc.description,
            url: doc.url
        };
        resultArray.push(resultItem);
    });
  } finally {
    await client.close();
  }
  return resultArray;
}

// var result = run("max").catch(console.dir);

// result.then(function(result) {
//     console.log("The results are : " + result);
//  })

module.exports = { run };