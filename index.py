from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)

def query_folder():
    folder = subprocess.check_output('ls folder/ -p | grep /',shell=True).decode().replace('/', '').split('\n')
    folder_list =  list(folder)[:-1]
    files = subprocess.check_output('ls folder/ -p | grep -v /',shell=True).decode().replace('/', '').split('\n')
    files_list = list(files)[:-1]
    return folder_list, files_list

@app.route("/")
def practice():
    folder_list, files_list = query_folder()
    return render_template("index_page.html", folders=folder_list, files=files_list)


@app.route('/parser_data', methods=['POST'])
def parser_data():
    flow = 0
    print(request.form)
    cmd = ''
    if request.form.get('foldername'):
        cmd = 'mkdir folder/{}'.format(request.form['foldername'])

    elif request.form.get('filename'):
        cmd = 'touch folder/{}'.format(request.form['filename'])

    elif request.form.get('change_name'):
        cmd = 'mv folder/{} folder/{}'.format(request.form['name_id'], request.form['new_name'])

    elif request.form.get('permission'):
        permission = request.form['permission']
        print(permission)
        type_permission = ''
        if permission == 'rwx':
            type_permission = '777'
        elif permission == 'rw':
            type_permission = '666'
        elif permission == 'wx':
            type_permission = '333'
        elif permission == 'r':
            type_permission = '444'
        elif permission == 'w':
            type_permission = '222'
        elif permission == 'x':
            type_permission = '111'

        cmd = 'chmod {} folder/{}'.format(type_permission, request.form['name_id'])

    elif request.form.get('cambiar_propietario'):
        cmd = 'folder/{}'.format(request.form['name_id'])

    elif request.form.get('eliminar'):
        cmd = 'rm -rf folder/{}'.format(request.form['name_id'])

    elif request.form.get('info_permisos'):
        flow = 1
        folder_list, files_list = query_folder()
        cmd = 'ls -ld folder/{}'.format(request.form['name_id'])
        cmd_shell = subprocess.check_output(cmd,shell=True).decode().split('-')
        permissions = list(filter(None, cmd_shell))
        permissions_split =  [i.split(' ')[0] for i in permissions]
        users = ['Propietario: ', 'Grupo: ', 'Todos los usuarios: ']
        permissions_list = []
        pos = 0
        if len(permissions_split) > 2:
            while pos < 3:
                permission = users[pos]
                if 'r' in permissions_split[pos]:
                    permission += 'lectura '
                if 'w' in permissions_split[pos]:
                    permission += 'escritura '
                if 'x' in permissions_split[pos]:
                    permission += 'ejecución '
                permissions_list.append(permission)
                pos +=1
        else:
            while pos < 3:
                permission = users[pos] + 'lectura, escritura, ejecución'
                permissions_list.append(permission)
                pos +=1

        return render_template("index_page.html", folders=folder_list, files=files_list, permissions=permissions_list)

    elif request.form.get('copiar_pegar'):
        flow = 1
        folder_list, files_list = query_folder()
        def copy_paste_function(value):
            new_name = request.form['name_id'] + 'copy' + str(value)
            cmd = 'cp -r folder/{} folder/{}'.format(request.form['name_id'], new_name)
            cmd_shell = subprocess.check_output(cmd,shell=True).decode()
        i = 1
        try:
            copy_paste_function(1)
        except Exception as e:
            if 'are the same file' in str(e):
                i+=1
                copy_paste_function(i)
            else:
                print("an exception has ocurred!")
                
    if flow == 0:
        try:
            cmd_shell = subprocess.check_output(cmd,shell=True).decode()
            print(cmd_shell)
        except:
            print("an exception has ocurred!")

    folder_list, files_list = query_folder()
    return render_template("index_page.html", folders=folder_list, files=files_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")