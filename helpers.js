const fs = require('fs');
const path = require('path');

const checkIfDirExists = dir =>  fs.existsSync(dir);

const resolvePath = rawPath => path.resolve(rawPath);

const ensureDirectoryExists = (filePath) => {
    const dir = path.dirname(filePath);
    if (!checkIfDirExists(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.info(`Carpeta creada: ${dir}`);
    }
};


module.exports = {
  checkIfDirExists,
  resolvePath,
  ensureDirectoryExists
}