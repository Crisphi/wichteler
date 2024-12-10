
const express = require('express');
const LoginController = require('../controllers/logincontroller.js');

const login =  express.Router();

login.get("/login", LoginController.showLogin)
login.post("/login", LoginController.checkLogin);

 


module.exports = login;
