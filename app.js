const express = require('express');
const app = express();

const port = process.env.PORT; //define our port number, this doesn’t have to be 3000
const path = require("path"); //required to use 'path' module that gets the current directory
//const session = require('express-session'); // check this out later
//const users = require('./routes/UserRoutes'); // importing all user routes
//const posts = require('./routes/PostsRoutes'); // importing all post routes
const login = require('./routes/LoginRoutes');

// set up ejs templates
app.set('view engine', 'ejs');

// Set up the 'views' directory for EJS templates
app.set('views', path.join(__dirname, 'views'));

// setting all paths
app.use(login);

//routing path
app.get('/', (req, res) => {
    res.send('Hello World! jjjj');
  });

  // Start the server
app.listen(port, () => {
    console.log(`Server started on port ${port}`);
  });