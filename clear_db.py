from db.database import Database

tsodb = "tsoenv.db"
database = Database(tsodb)

print("Deleting entire data from "+tsodb)

database.delete_all()
