const express = require("express");
const { getAllPlants, getPlantById } = require("../controllers/plantsController");

const router = express.Router();

router.get("/", getAllPlants);
router.get("/:id", getPlantById);

module.exports = router;
