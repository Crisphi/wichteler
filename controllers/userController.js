
const express = require('express');
const {User} = require('../models/users'); // importing all user routes


const UserController = {
  getAllUsers: async(req, res) =>{
      const users = await User.getUsers();
      res.render("user_overview", {
              users, 

      });
  }, 
  getUserProfile: async (req, res) =>{
    try {
        const user_id = req.params.id;
        const user = await User.getUser(user_id); // Fetch user data
        res.render("profile", {
            user, // Pass user data to template
        });
    } catch (error) {
        console.error("Error fetching user profile:", error);
        res.status(500).send("Error fetching user profile");
    }
  },
  register: async (req, res) =>{
      try {
        const username = req.body.username;
        const pronouns = req.body.pronouns;
        const email_address = req.body.email;
        const given_name = req.body.given_name;                   
        const address = req.body.address;
        const plz = req.body.plz;
        const city = req.body.city;
        
        
        // generate the user id
        const user_id = Math.floor((Math.random()*9000)+1000);
        const newUser = await User.createUser({ user_id, username, pronouns, email_address, given_name, address, plz, city}); 
        //console.log(newUser);
        res.redirect(`/users/${user_id}`);

      } catch (error) {
        console.error("Error creating user", error);
        //res.status(500).send("Error creating user");
      }
    }
}

module.exports = UserController;
