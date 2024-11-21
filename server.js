// server.js (Node.js with Express.js)
const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const app = express();
const PORT = 3000;

const COMPLAINTS_FILE = 'complaints.json';

// Middleware for parsing form data
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// File upload setup with multer
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/');
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});
const upload = multer({ storage: storage });

// Route to handle complaint submission
app.post('/submit-complaint', upload.single('image'), async (req, res) => {
    const { description } = req.body;
    const imagePath = req.file ? req.file.path : '';

    // Create a new complaint object
    const newComplaint = {
        description,
        image: imagePath,
        status: 'Pending'
    };

    // Read existing complaints from file
    let complaints = [];
    if (fs.existsSync(COMPLAINTS_FILE)) {
        const data = fs.readFileSync(COMPLAINTS_FILE, 'utf8');
        complaints = JSON.parse(data);
    }

    // Add the new complaint
    complaints.push(newComplaint);

    // Write the updated complaints back to the file
    fs.writeFileSync(COMPLAINTS_FILE, JSON.stringify(complaints, null, 2));

    res.json({ message: 'Complaint submitted successfully', complaints });
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
