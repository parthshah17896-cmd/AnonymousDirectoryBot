from database import get_connection

profiles = [

    (1, "Riya", 19, "Unmarried", "India",
     "Hi! I'm Riya. I love chatting, movies, music and making new friends.",
     "images/riya.jpg",
     "https://t.me/ChatWithRiyaaBot"),

    (2, "Sofia", 26, "Unmarried", "Spain",
     "Love travelling, photography, hiking and photography.",
     "images/sofia.jpg",
     "https://t.me/ChatWithSofiaaBot"),

    (3, "Payal", 25, "Unmarried", "India",
     "Foodie, traveller and always up for a good conversation.",
     "images/payal.jpg",
     "https://t.me/ChatWithPayalBot"),

    (4, "Preeti", 32, "Married", "India",
     "Love books, family, travelling and meeting new people.",
     "images/preeti.jpg",
     "https://t.me/ChatWithPreetiBot"),

    (5, "Thoibi", 20, "Unmarried", "India",
     "Hi! I'm Thoibi. I love reading novels, cycling & gardening.",
     "images/Thoibi.jpeg",
     "https://t.me/ChatWithThoibiBot")

]

conn = get_connection()
cur = conn.cursor()

for p in profiles:
    cur.execute("""
        INSERT INTO profiles
        (id, name, age, marital_status, country, about, image, bot_link)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id)
        DO NOTHING;
    """, p)

conn.commit()

cur.close()
conn.close()

print("Profiles imported successfully.")
