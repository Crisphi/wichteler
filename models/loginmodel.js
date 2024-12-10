const knex = require('knex');
const dotenv = require("dotenv");
dotenv.config();

const db = knex({
    client: "mysql2",
    connection: {
      host: process.env.DB_HOST,
      user: process.env.DB_USERNAME,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_DATABASE,
    },
  });

const Login = {
    verifyUser: async (name, email) => {
        try {
            console.log(name, email);
            const user = await db.select('*').from('users').where({ username: name, email_address: email }).first();
            console.log("Query Ran:", user);
            return user || {};
        } catch (error) {
            console.error("Error verifying user:", error);
            return {};
        }
    }
};
module.exports = {Login};