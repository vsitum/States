#Restful interface that has search and update options for navigating a Zip code database on Phpmyadmin.


#https://stackoverflow.com/questions/8211128/multiple-distinct-pages-in-one-html-file
#https://stackoverflow.com/questions/902408/how-to-use-variables-in-sql-statement-in-python
#https://stackoverflow.com/questions/1081750/python-update-multiple-columns-with-python-variables
#https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
#https://github.com/vimalloc/flask-jwt-extended/issues/175


from mysql import connector
from flask import Flask, redirect, url_for, request, render_template
import mysql.connector
app = Flask(__name__, static_url_path='')

#connect to database
conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='zipcodes',
                               buffered = True)
cursor = conn.cursor()

#Search zipcodes database
@app.route('/searchZIPCODE/<searchZip>')
def searchzip(searchZip):
    # Get data from database
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [searchZip])
    test = cursor.rowcount
    if test != 1:
        return searchZip + " was not found"
    else:
        searched = cursor.fetchall()
        return 'Success! Here you go: %s' % searched

#update zipcodes database population for a specified zipcode
@app.route('/updatezippop/<updateZIP> <updatePOP>')
def updatezippop(updateZIP, updatePOP):
    cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s", [updateZIP])
    test = cursor.rowcount
    if test != 1:
        return updateZIP + " was not found"
    else:
        cursor.execute("UPDATE `zipcodes` SET Pop = %s WHERE zip= %s;", [updatePOP,updateZIP])
        cursor.execute("SELECT * FROM `zipcodes` WHERE zip=%s and Pop=%s", [updateZIP,updatePOP])
        test1 = cursor.rowcount
        if test1 != 1:
            return updateZIP + "failed to update"
        else:
            return 'Population has been updated successfully for State: %s' % updateZIP

#update webpage
@app.route('/update',methods = ['POST'])
def update():
       user = request.form['uzipcode']
       user2 = request.form['upop']
       return redirect(url_for('updatezippop', updateZIP=user, updatePOP=user2))

#search page
@app.route('/search', methods=['GET'])
def search():
       user = request.args.get('szipcodes')
       return redirect(url_for('searchzip', searchZip=user))


#root of web server and gots to template (login.html)
@app.route('/')
def root():
   return render_template('login.html')

#main
if __name__ == '__main__':
   app.run(debug = True)