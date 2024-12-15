const knex = require('knex');
const dotenv = require("dotenv");
const bcrypt = require('bcrypt'); // pw encryption
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
    verifyUser: async (email, password) => {
        try {
            const user = await db.select('*').from('participants').where({ email: email }).first();
            let hashedPW = user.password;
            if (encryptPassword(password, hashedPW)){
                return user || {};
            }
            
        } catch (error) {
            console.error("Error verifying user:", error);
            return {};
        }
    }
};

// checking pw function
async function encryptPassword(password, hash) {
return await bcrypt.compare(password, hash);
}
module.exports = {Login};