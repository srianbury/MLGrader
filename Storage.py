from flask_restful import Resource


class Storage(Resource):
    def __init__(self):
        import mysql.connector
        self.db = mysql.connector.connect(
            user='notadmin',
            password='notpassword',
            host='localhost',
            database='image_dataset'
        )

    def get(self):
        return self.read(), 200

    def post(self):
        return 'post not implemented', 200

    def insert(self, answers, images):
        cursor = self.db.cursor()

        sql = "INSERT INTO images (letter, pixels) VALUES (%s, %s)"
        val = []
        for index in range(0, len(answers)):
            temp_tuple = ("{}".format(answers[index]), "{}".format(images[index]))
            val.append(temp_tuple)

        cursor.executemany(sql, val)
        self.db.commit()
        #print(cursor.rowcount, "was inserted.")
        cursor.close()

    def read(self):
        cursor = self.db.cursor()
        sql = "SELECT * FROM images LIMIT 10"
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        return res


if __name__ == '__main__':
    store = Storage()
    data = store.read()
    for datum in data:
        print(datum)
