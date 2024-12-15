
const express = require('express');

const UserController = require('../controllers/userController.js'); // importing user controller

const LoginController = require('../controllers/logincontroller.js'); // importing login controller

const users = express.Router();


// Define a route for the root URL ("/")
users.get('/', async (req, res) => {
    res.redirect('/feed');
});




// page that lists all users
users.get("/users", UserController.getAllUsers);  // use this for the admin role later

// page that displays user details
users.get("/users/:id", LoginController.requireAuth, UserController.getUserProfile);

// register the user
users.post("/register", UserController.register);




module.exports = users;

