const { Login } = require('../models/loginmodel');

const session = require('express-session');


const LoginController = {
  checkLogin: async(req, res) => {
    
    try {
      const username = req.body.username;
      const userEmail = req.body.user_email;
      const user = await Login.verifyUser(username, userEmail);
      //console.log(user);
      if (user) { // if user is verified, set session details for them 
        console.log("found user", user.user_id);
       // req.session.user_id = user.user_id;
        //req.session.user_name = user.username;
        //req.session.user_email = user.user_email;

        return res.redirect(`/users/${user.user_id}`);
      } else {
        console.log("no user found", user.length);
        res.redirect("/404");
      }
    } catch (error) {
      console.log("checkLogin error", error);
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
      if (err) console.log("session end error", err);
    });

    console.log("session destroyed", req.session);
    return res.redirect(302, "/login");
  }
};

module.exports = LoginController;


