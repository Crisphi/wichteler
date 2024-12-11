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
    verifyUser: async (email) => {
        try {
            const user = await db.select('*').from('participants').where({ email: email }).first();
            console.log("Query ran:", user);
            return user || {};
        } catch (error) {
            console.error("Error verifying user:", error);
            return {};
        }
    }
};
module.exports = {Login};