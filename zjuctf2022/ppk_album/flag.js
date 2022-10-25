const { createCanvas } = require("canvas")
const fs = require('fs')

const FLAG = process.env.FLAG || 'ZJUCTF{TEST}'

const width = FLAG.length * 50 + 10;
const height = 200;
const canvas = createCanvas(width, height);
const context = canvas.getContext("2d");

context.fillStyle = "#ffef62";
context.fillRect(0, 0, width, height);
context.font = "bold 40px Arial";
context.textAlign = "center";
context.fillStyle = "#ab003c";

context.fillText(FLAG, width / 2, height / 2);

const buffer = canvas.toBuffer("image/png");
fs.writeFileSync("flag.png", buffer);