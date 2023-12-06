import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64

import random as rand
import datetime

def database_connection_url():
    dotenv.load_dotenv()

    return os.environ.get("POSTGRES_URI")

engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

with engine.begin() as conn:
    conn.execute(sqlalchemy.text("""
    DROP TABLE IF EXISTS shoes CASCADE; --5%                             
    DROP TABLE IF EXISTS brands CASCADE; --very small
    DROP TABLE IF EXISTS users CASCADE; --10%   
    DROP TABLE IF EXISTS raffles CASCADE; --1% 
    DROP TABLE IF EXISTS prize_carts CASCADE; --2.5%                                                      
    DROP TABLE IF EXISTS orders; -- 1%
    DROP TABLE IF EXISTS point_ledger; --20%
    DROP TABLE IF EXISTS prize_cart_items; --2.5%
    DROP TABLE IF EXISTS prize_ledger; --5%
    DROP TABLE IF EXISTS raffle_entries; --10%
    DROP TABLE IF EXISTS reviews; --20%
    DROP TABLE IF EXISTS shoes_to_users; --20%
    
                                 

    create table
    public.users (
    user_id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    name text not null,
    username text not null,
    email text not null,
    password bytea null,
    salt bytea null,
    is_logged_in boolean null default false,
    address text null,
    constraint Users_pkey primary key (user_id),
    constraint users_email_key unique (email),
    constraint users_user_id_key unique (user_id),
    constraint users_username_key unique (username)
    ) tablespace pg_default;
                                 
    create table
    public.brands (
    brand_id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    brand_name text not null,
    email text not null,
    password bytea null,
    salt bytea null,
    is_logged_in boolean not null default false,
    constraint brands_pkey primary key (brand_id),
    constraint brands_brand_name_key unique (brand_name),
    constraint brands_email_key unique (email)
    ) tablespace pg_default;
                                 
    create table
    public.shoes (
    shoe_id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    name text not null,
    brand text not null,
    price double precision not null,
    color text not null,
    material text not null,
    tags text[] null,
    type text not null,
    constraint shoes_pkey primary key (shoe_id)
    ) tablespace pg_default;
                                    
                                 
    create table
    public.raffles (
    raffle_id bigint generated by default as identity,
    start_time timestamp with time zone not null default now(),
    shoe_id bigint null,
    active boolean not null default true,
    constraint raffle_catalog_pkey primary key (raffle_id),
    constraint raffles_shoe_id_fkey foreign key (shoe_id) references shoes (shoe_id) on update cascade on delete cascade
    ) tablespace pg_default;

    create table
    public.orders (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    user_id bigint not null,
    shoe_id bigint not null,
    quantity integer not null default 1,
    constraint orders_pkey primary key (id),
    constraint orders_shoe_id_fkey foreign key (shoe_id) references shoes (shoe_id) on update cascade on delete cascade,
    constraint orders_user_id_fkey foreign key (user_id) references users (user_id) on update cascade on delete cascade
    ) tablespace pg_default;
                                    
    create table
    public.point_ledger (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    user_id bigint not null,
    point_change bigint not null,
    constraint point_ledger_pkey primary key (id),
    constraint point_ledger_user_id_fkey foreign key (user_id) references users (user_id) on update cascade on delete cascade
    ) tablespace pg_default;


    create table
    public.prize_carts (
    cart_id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    user_id bigint not null,
    active boolean not null default true,
    constraint prize_carts_pkey primary key (cart_id),
    constraint prize_carts_user_id_fkey foreign key (user_id) references users (user_id) on update cascade on delete cascade
    ) tablespace pg_default;                             

    create table
    public.prize_cart_items (
    created_at timestamp with time zone not null default now(),
    cart_id bigint not null,
    shoe_id bigint not null,
    quantity integer not null,
    constraint prize_cart_items_pkey primary key (cart_id, shoe_id),
    constraint prize_cart_items_cart_id_fkey foreign key (cart_id) references prize_carts (cart_id) on update cascade on delete cascade,
    constraint prize_cart_items_shoe_id_fkey foreign key (shoe_id) references shoes (shoe_id) on update cascade on delete cascade
    ) tablespace pg_default;
                                    
                          
    create table
    public.prize_ledger (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    shoe_id bigint not null,
    change integer not null default 1,
    constraint prize_ledger_pkey primary key (id),
    constraint prize_ledger_shoe_id_fkey foreign key (shoe_id) references shoes (shoe_id) on update cascade on delete cascade
    ) tablespace pg_default;
                                    
    create table
    public.raffle_entries (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    user_id bigint not null,
    raffle_id bigint not null,
    constraint raffle_entries_pkey primary key (id),
    constraint raffle_entries_raffle_id_fkey foreign key (raffle_id) references raffles (raffle_id) on update cascade on delete cascade,
    constraint raffle_entries_user_id_fkey foreign key (user_id) references users (user_id) on update cascade on delete cascade
    ) tablespace pg_default;
                                    
                                    
    create table
    public.reviews (
    rating_id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    shoe_id bigint not null,
    user_id bigint not null,
    rating integer not null,
    comment text null,
    constraint reviews_pkey primary key (rating_id),
    constraint reviews_shoe_id_fkey foreign key (shoe_id) references shoes (shoe_id) on update cascade on delete cascade,
    constraint reviews_user_id_fkey foreign key (user_id) references users (user_id) on update cascade on delete cascade,
    constraint ratings_comment_check check (
        (
        length(
            comment
        ) < 500
        )
    ),
    constraint ratings_rating_check check (
        (
        (rating >= 1)
        and (rating <= 5)
        )
    )
    ) tablespace pg_default;    

    create table
    public.shoes_to_users (
    shoe_id bigint not null,
    user_id bigint not null,
    constraint shoes_to_users_shoe_id_fkey foreign key (shoe_id) references shoes (shoe_id) on update cascade on delete cascade
    ) tablespace pg_default;

    """))

fake = Faker()
with engine.begin() as conn:

    #all possible brand names
    brandnames = ['Nike', 'Skechers', 'Asics', 'Puma', 'Fila', 'Vans', 'New Balance', 'Converse', 'Reebok', 'Adidas','Under Armour','Balenciaga','Timberland']
    brands = []

    #get key for encryption
    dotenv.load_dotenv()
    crypto_key = bytes(os.environ.get("CRYPTO_KEY"),'utf-8')

    #create and encrypt password
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(crypto_key))
    f = Fernet(key)

    password = f.encrypt(bytes(fake.pystr(8,12),'utf-8'))

    for name in brandnames:
        #create fake brand data
        brands.append({
            "created_at": fake.date_time_between(start_date='-3y', end_date='-1y', tzinfo=None),
            "brand_name": name,
            "email": name + "@gmail.com",
            "password": password,
            "salt": salt,
            "is_logged_in": fake.pybool(),
        })

    #populate brands table
    conn.execute(sqlalchemy.text("""
                                        INSERT INTO brands (created_at,brand_name, email, password,salt,is_logged_in) 
                                        VALUES (:created_at,:brand_name, :email, :password,:salt,:is_logged_in)
                                        """),
                                        brands)
    
    #create fake shoe info
    num_shoes = 10000
    tag_list = ("true_to_size","eye-catcher","non-slip","closed-toe","sustainable","professional","designer","form-fitting","high-top","low-top")
    material_list = ("Leather","Mesh","Felt","Textile","Knit","Suede","Primeknit","Flyknit","Canvas","Flexweave","Nylon","Synthetic","Leather/Mesh","Leather/Suede","Synthetic/Leather","Canvas/Leather","Leather/Synthetic","Suede/Canvas")
    color_list = ("Navy","Multi-Color","Red","Gray","Ivory","Pink","Purple","Cinder","Zebra","Yellow","Beige","Cream","Sunflower","Egret","Khaki","Black","Orange","Green","Silver","White","Charcoal","Burgundy","Brown")
    type_list = ("Fashion","Running","Basketball","Hiking","CrossFit","Walking","Training","Trail","Lifestyle","Daily","Slides","Skate","Casual")
    name_list = ("Air","Max","Ultra","Boost","Force","Classic","Elite","React","Infinity","Foam","Runner","Zoom","Flex","Go","Star","Sport","Nano","Pegasus","October","Red","Night","Blaze")
    shoes = []


    for i in range(num_shoes):
        shoes.append({
            "created_at": fake.date_time_between(start_date='-3y', end_date='now', tzinfo=None),
            "name": fake.random_element(elements=name_list) + " " + fake.random_element(elements=name_list) + " "+ str(rand.randint(1,50)),
            "brand": fake.random_element(elements=brandnames),
            "price": rand.randrange(50,250+1,5),
            "color": fake.random_element(elements=color_list),
            "material": fake.random_element(elements=material_list),
            "tags": fake.random_elements(elements=tag_list,unique=True),
            "type": fake.random_element(elements=type_list)
        })
        
    #populate shoes table with fake data
    conn.execute(sqlalchemy.text("""
            INSERT INTO shoes (created_at,name, brand, price, color, material, tags, type)
            VALUES (:created_at,:name, :brand, :price, :color, :material, :tags, :type)
        """), shoes)

    #new engine connection to ensure that shoes table exists

    num_users = 85000
    total_shoes = 0
    total_reviews = 0
    shoes_to_users = []

    review_list = ["fit","comfy","expensive","ergonomic","cheap","high quality","poor quality", "quality", "uncomfy","true-to-size","too big","too small", "good value","stylish","ugly","for","buy","dont buy", "scam","worth","wow","bad","good","and","not","very","too","the","but","or","so"]
    reviews = []
    points= []

    shoe_sample_distribution = np.random.default_rng().negative_binomial(0.5, 0.11, num_users)
    
    for i in range(num_users):
        #create profile
        profile = fake.simple_profile()
        creation_date = fake.date_time_between(start_date='-3y', end_date='now', tzinfo=None)

        id = conn.execute(sqlalchemy.text("""
        INSERT INTO users (created_at,name, username, email, password,salt,address,is_logged_in) VALUES (:created_at, :name, :username, :email,:password,:salt,:address,:is_logged_in) RETURNING user_id;
        """), {
            "created_at":creation_date , 
            "name": profile['name'], 
            "username": fake.first_name()[0].lower() + fake.last_name().lower() + str(i) , 
            "email": str(i) + fake.unique.ascii_free_email(),
            "password":password,"salt":salt,
            "address":profile['address'],
            "is_logged_in":fake.pybool()
        }).scalar_one()

        
        shoe_amount = shoe_sample_distribution[i]
        total_shoes += shoe_amount

        for j in range(shoe_amount):
            shoe_id = fake.unique.random_int(min=1,max=num_shoes)

            shoes_to_users.append({
                "shoe_id": shoe_id ,
                "user_id":id
            })

            comment = fake.text(max_nb_chars = rand.randint(100,500),ext_word_list = review_list)
            comment_date = fake.date_time_between(start_date=creation_date, end_date='now', tzinfo=None)

            if fake.pybool(75) is True:
                total_reviews += 1
                sample_rating = np.random.choice([1, 2, 3, 4, 5],
                                                 1,
                                                p=[0.1, 0.15,0.15,0.35,0.25]).item()
                
                reviews.append({
                    "created_at":comment_date, 
                    "shoe_id":shoe_id,
                    "user_id": id,
                    "rating": sample_rating,
                    "comment":comment
                })

                points.append({
                    "created_at":comment_date,
                    "user_id": id,
                    "point_change": len(comment)//10
                })
        fake.unique.clear()
        
  
    #calculate number of raffles
    num_raffles = 52 * 3
    
    orders = []
    raffle_entries = []

    participants = np.random.default_rng().negative_binomial(0.75, 0.003, num_raffles)


    for i in range(num_raffles):
        start_time = fake.date_time_between(start_date='-3y', end_date='now', tzinfo=None)
        endtime = start_time + datetime.timedelta(days=7)
        raffle_shoe = fake.unique.random_int(min=1,max=num_shoes)
        days = (datetime.datetime.now() - start_time).days
        

        if days >= 7:
            active = False
        else:
            active = True

        raffle_id = conn.execute(sqlalchemy.text("""
            INSERT INTO raffles (start_time,shoe_id,active) VALUES (:start_time, :shoe_id,:active) RETURNING raffle_id;
            """), [{"start_time":start_time,"shoe_id":raffle_shoe,"active":active}]).scalar_one()
        
        ticket_cost = conn.execute(sqlalchemy.text("""
            SELECT price FROM shoes WHERE shoe_id = :shoe_id
            """), [{"shoe_id":raffle_shoe}]).scalar_one()
        
        #insert entries for winners
        if active is False:

            winner_id = fake.random_int(min=1,max=num_users)

            entries = fake.random_int(1,5)

            orders.append({"created_at":endtime,
                           "user_id":winner_id,
                           "shoe_id":raffle_shoe})
            
            entry_time = fake.date_time_between(start_date=start_time, end_date=endtime, tzinfo=None)

            for _ in range(entries):
                raffle_entries.append({"created_at":entry_time,
                                       "user_id":winner_id,
                                       "raffle_id":raffle_id})
                
            points.append(
                {
                "created_at":entry_time,
                "user_id":winner_id,
                "point_change":entries * ticket_cost * -1
                }
            )
            points.append(
                 {
                "created_at":entry_time - datetime.timedelta(days=10),
                "user_id":winner_id,
                "point_change":entries * ticket_cost 
                }
            )

        #insert all other entries
        enterers = []
    
        for _ in range(max(participants[i].item(),1)):

            other_entries = max(np.random.default_rng().negative_binomial(1, 0.5, 1).item(),1)

            if other_entries > 0:
                enterers.append({
                    "user_id":fake.random_int(1,num_users),
                    "entries": other_entries
                    })
            

        for user in enterers:
            entry_time = fake.date_time_between(start_date=start_time, end_date=endtime, tzinfo=None)
            for _ in range(user['entries']):
                raffle_entries.append({"created_at":entry_time,
                                        "user_id":user['user_id'],
                                        "raffle_id":raffle_id})
            
            points.append(
                {
                "created_at":entry_time,
                "user_id":user['user_id'],
                "point_change":user['entries'] * ticket_cost * -1
                }
            )



    fake.unique.clear()

    #fill prize ledger and prize related tables
    cart_items = []

    for j in range(num_raffles):
        prize_shoe = fake.random_int(min=1,max=num_shoes)
        created_at = fake.date_time_between(start_date='-3y', end_date='now', tzinfo=None)

        prize_id = conn.execute(sqlalchemy.text("""
            INSERT INTO prize_ledger (created_at,shoe_id,change) VALUES (:created_at, :shoe_id,1) RETURNING id;
            """), [{"created_at":created_at,"shoe_id":prize_shoe}]).scalar_one()
        
        if fake.pybool(60):
            prize_user = fake.unique.random_int(min=1,max=num_users)
            prize_date = created_at + datetime.timedelta(days=rand.randint(1,60))

            conn.execute(sqlalchemy.text("""
            INSERT INTO prize_ledger (created_at,shoe_id,change) VALUES (:created_at, :shoe_id,-1);
            """), [{"created_at":prize_date,"shoe_id":prize_shoe}])

            cart_id = conn.execute(sqlalchemy.text("""
            INSERT INTO prize_carts (created_at,user_id,active) VALUES (:created_at, :user_id,False) RETURNING cart_id;
            """), [{"created_at":prize_date,"user_id":prize_user}]).scalar_one()

            cart_items.append({
                "created_at":prize_date,
                "cart_id":cart_id,
                "shoe_id":prize_shoe,
                "quantity":1
            })

            prize_cost = conn.execute(sqlalchemy.text("""
            SELECT price FROM shoes WHERE shoe_id = :shoe_id
            """), [{"shoe_id":prize_shoe}]).scalar_one()

            points.append(
                {
                "created_at":prize_date,
                "user_id":prize_user,
                "point_change":  prize_cost * -1
                }
            )

            orders.append({"created_at":prize_date,
                           "user_id":prize_user,
                           "shoe_id":prize_shoe})
    fake.unique.clear()


            
    if shoes_to_users:
        conn.execute(sqlalchemy.text("""
            INSERT INTO shoes_to_users (shoe_id,user_id) VALUES (:shoe_id, :user_id);
            """), shoes_to_users)
        
    if reviews:
        conn.execute(sqlalchemy.text("""
            INSERT INTO reviews (created_at,shoe_id,user_id,rating,comment) VALUES (:created_at,:shoe_id, :user_id,:rating,:comment);
            """), reviews)
        
    if points:
         conn.execute(sqlalchemy.text("""
            INSERT INTO point_ledger (created_at,user_id,point_change) VALUES (:created_at, :user_id,:point_change);
            """), points)
         
    if orders:
        conn.execute(sqlalchemy.text("""
            INSERT INTO orders (created_at,user_id,shoe_id,quantity) VALUES (:created_at,:user_id, :shoe_id,1);
            """), orders)
        
    if raffle_entries:
        conn.execute(sqlalchemy.text("""
                INSERT INTO raffle_entries (created_at,user_id,raffle_id) VALUES (:created_at,:user_id, :raffle_id);
                """), raffle_entries)
        
    if cart_items:
        conn.execute(sqlalchemy.text("""
                INSERT INTO prize_cart_items (created_at,cart_id,shoe_id,quantity) VALUES (:created_at,:cart_id, :shoe_id,:quantity);
                """), cart_items)

    
    print("brands:" + str(len(brandnames)))
    print("shoes: " + str(num_shoes))
    print("users: "  + str(num_users))
    print("user_shoes: " + str(len(shoes_to_users)))
    print("reviews: " + str(len(reviews)))
    print("points: " + str(len(points)))
    print("orders: " + str(len(orders)))
    print("raffle_entries: " + str(len(raffle_entries)))
    print("raffles: " + str(num_raffles))
    print("prizes: " + str(num_raffles))
    print("cart_items: " + str(len(cart_items)))
    print("carts: " + str(len(cart_items)) )

    total_rows = len(brandnames) + num_shoes + num_users + len(shoes_to_users) + len(reviews) + len(points) + len(orders) + len(raffle_entries) + num_raffles + num_raffles + len(cart_items) + len(cart_items)
    print("\ntotal rows: " + str(total_rows))


    