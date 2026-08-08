const express = require("express");
const {
  listMissingSearches,
  createMissingSearch,
} = require("../controllers/missingSearchesController");

const router = express.Router();

router.get("/", listMissingSearches);
router.post("/", createMissingSearch);

module.exports = router;
