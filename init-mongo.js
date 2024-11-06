// Read database name from environment variable
const dbName = process.env.MONGO_INITDB_DATABASE || 'default_database';
db = db.getSiblingDB(dbName);  // Switch to the specified database

// Create the 'purchases' collection
db.createCollection('purchases');
