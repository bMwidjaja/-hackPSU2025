const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

let ratings = [];

app.post('/ratings', (req, res) => {
  const rating = {
    id: Date.now().toString(),
    ...req.body
  };
  ratings.push(rating);
  res.json({ success: true, rating });
});

app.get('/ratings', (req, res) => {
  res.json({ ratings });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
}); 