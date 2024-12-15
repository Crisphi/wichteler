const { Login } = require('../models/loginmodel');

const session = require('express-session');


const LoginController = {
  checkLogin: async(req, res) => {  // initially checking if login details are correct
    
    try {
      const user_email = req.body.user_email
      const user_password = req.body.user_password;

      console.log(user_email, user_password);
      const user = await Login.verifyUser(user_email, user_password);
      //console.log(user);
      if (user) { // if user is verified, set session details for them 
        console.log("found user");
        req.session.user_id = user.user_id;
        req.session.isLoggedIn = true;
        req.session.user_name = user.username;
      
        return res.redirect(`/users/${user.id}`);
       
      } else {
        console.log("no user found", user.length);
        res.redirect("/404");
      }
    } catch (error) {
      console.log("checkLogin error", error);
    }
  },
  requireAuth: async(req, res, next) => {   // continually checking if user is still logged in 
    if (req.session.userId) {
        next(); // User is authenticated, continue to next middleware
    } else {
        res.redirect('/login'); // User is not authenticated, redirect to login page
    }
},

  showLogin: async (req, res) => {
    try {
        res.render("login");
    } catch (error) {
        console.error("Error showing login:", error);
        res.status(500).send("Error showing login");
    } 
  },
  logout: async (req, res) => {
    req.session.destroy(function (err) {
      if (err) {
        console.log("session end error", err);
      } else {
        console.log("session destroyed", req.session);
    return res.redirect(302, "/login");
      }
    });    
  }
};

module.exports = LoginController;


