BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "solutions" (
	"Solution_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Distance"	REAL,
	"Node_order"	TEXT,
	"Problem_name"	TEXT,
	FOREIGN KEY("Problem_name") REFERENCES "problems"("Name")
);
CREATE TABLE IF NOT EXISTS "problems" (
	"Name"	TEXT,
	"Dimension"	INTEGER,
	"Nodes"	TEXT,
	"X"	REAL,
	"Y"	REAL,
	PRIMARY KEY("Name")
);
COMMIT;
