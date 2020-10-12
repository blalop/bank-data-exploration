
DROP TABLE IF EXISTS MOVEMENTS;

.mode csv
.separator "|"
.import movements.csv MOVEMENTS
