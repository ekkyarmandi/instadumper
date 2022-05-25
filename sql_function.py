import sqlite3

def create_table(table_name: str, field: dict) -> None:
    field_str = ",\n".join({k+" "+v for k,v in field.items()}).strip()
    with sqlite3.connect("data/instagram.db") as con:
        cur = con.cursor()
        cur.execute(f"CREATE TABLE {table_name} ({field_str});")
        con.commit()

def clear(table_name:str) -> None:
    with sqlite3.connect("data/instagram.db") as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM {table_name};")
        con.commit()

def insert(table_name: str, entry: dict) -> None:
    n = len(entry)
    columns = ",".join(list(entry.keys()))
    values = list(entry.values())
    with sqlite3.connect("data/instagram.db") as con:
        cmd = f"""
            INSERT or IGNORE into {table_name} ({columns}) VALUES ({str('?,'*n).strip(",")});
        """
        cur = con.cursor()
        cur.execute(cmd,(*values,))
        con.commit()


if __name__ == "__main__":

    # create_table(
    #     "followers",
    #     dict(
    #         id="TEXT UNIQUE",
    #         username="TEXT",
    #         fullname="TEXT",
    #         followers="INT",
    #         followings="INT",
    #         posts="INT",
    #         last_post_url="TEXT",
    #         last_post_date="TEXT",
    #         biography="TEXT",
    #         is_bussiness="BOOL",
    #         business_category="TEXT",
    #         links="TEXT"
    #     )
    # )

    # entry = dict( 
    #     id="1234",
    #     username="ekkyarmandi",
    #     fullname="Ekky Armandi",
    #     followers=100,
    #     followings=10,
    #     posts=5,
    #     last_post_url="last.com",
    #     last_post_date="2 Feb 2022",
    #     biography="Python Developer",
    #     is_bussiness=0,
    #     business_category=None,
    #     links="link.com"
    # )
    # insert("followers", entry)

    clear("followers")