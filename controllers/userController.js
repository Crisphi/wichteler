
const express = require('express');
const {User} = require('../models/users'); // importing all user routes
const bcrypt = require('bcrypt'); // pw encryption


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
  register: async (req, res) => {
    try {
      // load data from the form 
        const {username, pronouns, email, password, given_name, streetandnr, plz, city } = req.body;

        // Hash the password
        const hashedPassword = await hashPassword(password);

        // generate id
        const id = Math.floor((Math.random()*9000)+1000);

        // Create the user
        const newUser = await User.createUser({
            id: id,
            name: username,
            pronouns,
            email,
            password: hashedPassword, 
            shippingname: given_name,
            streetandnr,
            plz,
            city,
        });

        // Resdirect to user page 
        
        res.redirect(`/users/${id}`);
    } catch (error) {
        console.error("Error registering user:", error);
        res.status(500).json({ error: "Failed to register user" });
    }
}
};

// Password hashing utility
async function hashPassword(password) {
const saltRounds = 10;
return await bcrypt.hash(password, saltRounds);
}
module.exports = UserController;
