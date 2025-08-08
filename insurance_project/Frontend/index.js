const mysql = require('mysql2');
const bcrypt = require("bcrypt");
const express = require("express");
const app = express();
const path = require('path');
const methodoverride = require("method-override");
const session = require('express-session');
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

app.use(methodoverride("_method"));
app.use(express.urlencoded({extended: true}));
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "/"));

const connection = mysql.createConnection({
  host: 'localhost',     
  user: 'root',     
  database: 'logindata',   
  password: '@Sayanpaul721632'  
});
const port = 8080;
app.listen(port, () => {
    console.log(`Listening ot port ${port}`);
});

// Serve static files from the homepage directory
app.use(express.static(path.join(__dirname, 'homepage')));

// Route for root URL to serve index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'homepage', 'index.html'));
});

// Show login form
app.get("/login", (req, res) => {
    res.render("login");
});

//Login Route
app.post("/login", (req, res) => {
    const { username, password } = req.body;

    const query = "SELECT * FROM users WHERE username = ?";
    connection.query(query, [username], async (err, results) => {
        if (err) return res.send("Database error.");
        if (results.length === 0) return res.send("User not found");

        const user = results[0];
        const match = await bcrypt.compare(password, user.password);

        if (match) {
            //Redirect to Streamlit app
            // res.redirect("https://ai-medical-soumyadip.onrender.com");
            res.sendFile(path.join(__dirname, 'homepage', 'index.html'));
        } else {
            res.send("Invalid credentials");
        }
    });
});

//Signup Route
// Show signup form
app.get("/signup", (req, res) => {
    res.render("signup");
});

// Handle signup form
app.post("/signup", async (req, res) => {
    const { username, password } = req.body;

    try {
        const hashedPassword = await bcrypt.hash(password, 10); // Hashing
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

// Session middleware
app.use(session({
    secret: 'your_secret_key',
    resave: false,
    saveUninitialized: false
}));

app.use(passport.initialize());
app.use(passport.session());

// Serialize and deserialize user
passport.serializeUser((user, done) => {
    done(null, user);
});
passport.deserializeUser((user, done) => {
    done(null, user);
});

// Google OAuth Strategy
passport.use(new GoogleStrategy({
    clientID: 'YOUR_GOOGLE_CLIENT_ID', // <-- Replace this
    clientSecret: 'YOUR_GOOGLE_CLIENT_SECRET', // <-- Replace this
    callbackURL: '/auth/google/callback'
}, (accessToken, refreshToken, profile, done) => {
    // Here you can save/find the user in your DB if needed
    return done(null, profile);
}));

// Google Auth Routes
app.get('/auth/google',
    passport.authenticate('google', { scope: ['profile', 'email'] })
);

app.get('/auth/google/callback',
    passport.authenticate('google', { failureRedirect: '/login' }),
    (req, res) => {
        // Successful authentication, redirect as needed.
        res.redirect('https://ai-medical-soumyadip.onrender.com');
    }
);
