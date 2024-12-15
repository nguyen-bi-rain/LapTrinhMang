import ftplib
import os


def print_menu():
    print("\nMenu:")
    print("1. List directory")
    print("2. Change directory")
    print("3. Create directory")
    print("4. Delete file")
    print("5. Delete directory")
    print("6. Rename file or directory")
    print("7. Get file size")
    print("8. Download file")
    print("9. Upload file")
    print("10. Send custom command")
    print("11. Exit")

def list_dir(server):
    print("----Function List Directory----")
    try:
       print(server.dir())
    except ftplib.all_errors as ex:
        print(ex)


def create_dir(server):
    name = input("Enter name Directory")
    try:
        server.mkd(name)
        print("Created directoty : ",name)
    except ftplib.all_errors as ex:
        print(ex)

def delete_file(server):
    name = input("Enter name file want to delete")
    try:
        server.delete(name)
        print(f"file {name} deleted")
    except ftplib.all_errors as ex:
        print(ex)


def delete_dir(server):
    name = input("Enter name directory want to delete")
    try:
        server.rmd(name)
        print(f"file {name} deleted")
    except ftplib.all_errors as ex:
        print(ex)

def rename_file(server):
    current_name = input("Enter file or directory want to change name")
    rename = input("enter name you want change to")
    try:
        server.rename(current_name,rename)
        print(f"rename {current_name} to {rename}")
    except ftplib.all_errors as ex:
        print(ex)


def file_size(server):
    name = input("Enter file name")
    try:
        size = server.size(name)
        print(f"size of {name} is {size}")
    except ftplib.all_errors as ex:
        print(ex)


def download(server):
    file_origin = input("enter file want to download")
    file_copy = input("Enter local path or file name want to save as ")
    try:
        with open(file_copy, "wb") as fp:
            server.retrbinary("RETR " + file_origin, fp.write())
        print(f"Download of {file_origin} to {file_copy} completed successfull")

    except ftplib.all_errors as e:
        print(f"Error downloading file: {e} ")
        if os.path.isfile(file_copy):
            os.remove(file_copy)

def upload(server):
    file_name = input("Enter file name want to upload: ")

    try:
        with open(file_name, "rb") as fp:
            response = server.storbinary("STOR " + file_name, fp)
        print(f"Server response: {response}")

        if not response.startwith("226"):
            print("Upload failed !")
        else:
            print(f"Upload file {file_name} completed successfully")

    except ftplib.all_errors as e:
        print(f"Error uploading file: {e} ")


def send_custom_cmd(server):
    print("_____Function Send Custom Command_____")
    command  =  input("enter your command")
    try:
        response = server.sendcmd(command)
        print(response)

    except ftplib.all_errors as e:
        print(f"Error sending command: {e} ")

def change_dir(server):
    print("----Function List Directory----")
    dir = input("enter your directory name")
    try:
        server.cwd(dir)
        print(f"Change to directory: {dir} ")
    except ftplib.all_errors as ex:
        print(ex)




if __name__ == '__main__':
    server = ftplib.FTP('127.0.0.1',"user01","123")

    while True:
        print_menu()

        choice = input("choose your option : ")

        if choice == '1':
            list_dir(server)
        elif choice == '2':
            change_dir(server)
        elif choice == '3':
            create_dir(server)
        elif choice == '4':
            delete_file(server)
        elif choice == '5':
            delete_dir(server)
        elif choice == '6':
            rename_file(server)
        elif choice == '7':
            file_size(server)
        elif choice == '8':
            download(server)
        elif choice == '9':
            upload(server)
        elif choice == '10':
            send_custom_cmd(server)
        elif choice == '11':
            break
        else:
            print("invalid choice please choose again")

    server.quit()