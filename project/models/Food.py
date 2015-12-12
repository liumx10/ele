from project import db

class Food(db.Model):
    __tablename__ = "food"
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer)
    fid = db.Column(db.Integer)
    name = db.Column(db.String(64))
    count = db.Column(db.Integer)

    def __init__(self, fid, rid, name, count):
        self.rid = rid
        self.fid = fid
        self.name = name
        self.count = count

def get_food(restaurant_id):
    print restaurant_id
    res = Food.query.filter_by(fid=restaurant_id).order_by(Food.count.desc()).all()
    count = 0
    for food in res:
        count = count+food.count
    for food in res:
        food.y = food.count*1.0/count
    return res