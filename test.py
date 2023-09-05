import os



with os.open("./tmp",'wb') as file:
    file.write(b"1")
