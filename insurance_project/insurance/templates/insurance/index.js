const mysql = require('mysql2');
const bcrypt = require("bcrypt");
const express = require("express");
const app = express();
const path = require('path');
const methodoverride = require("method-override");

app.use(methodoverride("_method"));
app.use(express.urlencoded({ extended: true }));
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "/views"));

// Serve static files from the homepage directory
app.use(express.static(path.join(__dirname, 'homepage')));

// MySQL database connection
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  database: 'logindata',
  password: '@Sayanpaul721632'
});

// Home route (serves homepage/index.html)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'homepage', 'index.html'));
});

// Login form
app.get("/login", (req, res) => {
  res.sendFile(path.join(__dirname, "views", "login.html"));
});

app.post("/login", (req, res) => {
  const { username, password } = req.body;
  console.log("Login attempt for:", username);

  const query = "SELECT * FROM users WHERE username = ?";
  connection.query(query, [username], async (err, results) => {
    if (err) {
      console.error("Database error:", err);
      return res.send("Database error.");
    }

    if (results.length === 0) {
      console.log("User not found");
      return res.send("User not found");
    }

    const user = results[0];
    const match = await bcrypt.compare(password, user.password);

    if (match) {
      console.log("Login successful, redirecting...");
      res.redirect("https://ai-medical-soumyadip.onrender.com");
    } else {
      console.log("Password mismatch");
      res.send("Invalid credentials");
    }
  });
});

// Signup form
app.get("/signup", (req, res) => {
  res.sendFile(path.join(__dirname, "views", "signup.html"));
});

// Handle signup
app.post("/signup", async (req, res) => {
  const { username, password } = req.body;

  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    const query = "INSERT INTO users (username, password) VALUES (?, ?)";

    connection.query(query, [username, hashedPassword], (err, results) => {
      if (err) {
        console.error("Error inserting user:", err);
        return res.send("User already exists or error occurred.");
      }
      res.send("Signup successful");
    });
  } catch (err) {
    res.send("Internal Server Error");
  }
});

// Start server
const port = 8080;
app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
