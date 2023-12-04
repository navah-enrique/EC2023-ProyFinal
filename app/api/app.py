from flask import Flask, request,send_file
import json
import psycopg2
import psycopg2.extras
import os
import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import KMeans


# Estructura del uri:
# "motor://user:password@host:port/database"
database_uri = f'postgresql://{os.environ["PGUSR"]}:{os.environ["PGPASS"]}@{os.environ["PGHOST"]}:5432/{os.environ["PGDB"]}'

app = Flask(__name__)
conn = psycopg2.connect(database_uri)

@app.route('/')
def home():
    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
    cur.execute("select * from users")
    results = cur.fetchall()
    cur.close()
    return json.dumps([x._asdict() for x in results], default=str)

def get_db_connection():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(database_uri)
    return conn

def load_data():
    global neighborhoods_venues_sorted
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tu_tabla")
    rows = cur.fetchall()
    neighborhoods_venues_sorted = pd.DataFrame(rows, columns=[desc[0] for desc in cur.description])
    cur.close()
    conn.close()

@app.route('/users', methods=["POST", "GET", "DELETE", "PATCH"])
def user():
    if request.method == 'GET':
        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        user_id = request.args.get("id")
        cur.execute(f"select * from users where id={user_id}")
        results = cur.fetchone()
        cur.close()
        return json.dumps(results._asdict(), default=str)
    if request.method == "POST":
        user = json.loads(request.data)
        cur = conn.cursor()
        cur.execute(
            "insert into users (name, lastname, age) values (%s, %s, %s)",
            (user[0]["name"], user[0]["lastname"], user[0]["age"]),
        )
        conn.commit()
        cur.execute("SELECT LASTVAL()")
        user_id = cur.fetchone()[0]
        cur.close()
        return json.dumps({"user_id": user_id})
    if request.method == "DELETE":
        cur = conn.cursor()
        user_id = request.args.get("id")
        cur.execute(f"delete from users where id={user_id}")
        conn.commit()
        cur.close()
        return json.dumps({"user_id": user_id})
    if request.method == "PATCH":
        user = json.loads(request.data)
        cur = conn.cursor()
        user_id = request.args.get("id")
        cur.execute(
            "update users set (name, lastname, age) = (%s,%s,%s) where id=%s ",
            (user[0]["name"], user[0]["lastname"], user[0]["age"], user_id),
        )
        conn.commit()
        cur.close()
        return json.dumps({"user_id": user_id})


@app.route('/venues_cdmx_completa', methods=['GET'])
def process_data():
    try:
        # Carga y procesa los datos CSV
        CDMX_venues2 = pd.read_csv('../venues_cdmx_completa.csv')
        CDMX_onehot = pd.get_dummies(CDMX_venues2[['Venue Category']], prefix="", prefix_sep="")

        # add neighborhood column back to dataframe
        CDMX_onehot['Neighborhood'] = CDMX_venues2['Neighborhood'] 

        # move neighborhood column to the first column
        fixed_columns = [CDMX_onehot.columns[-1]] + list(CDMX_onehot.columns[:-1])
        CDMX_onehot = CDMX_onehot[fixed_columns]

        CDMX_grouped = CDMX_onehot.groupby('Neighborhood').mean().reset_index()
        def return_most_common_venues(row, num_top_venues):
            row_categories = row.iloc[1:]
            row_categories_sorted = row_categories.sort_values(ascending=False)
            return row_categories_sorted.index.values[0:num_top_venues]
        #Giving a dataframe with the top 10 with the more kind of venues for each neighborhood

        num_top_venues = 10

        indicators = ['st', 'nd', 'rd']

        # create columns according to number of top venues
        columns = ['Neighborhood']
        for ind in np.arange(num_top_venues):
            try:
                columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
            except:
                columns.append('{}th Most Common Venue'.format(ind+1))

        # create a new dataframe
        neighborhoods_venues_sorted = pd.DataFrame(columns=columns)
        neighborhoods_venues_sorted['Neighborhood'] = CDMX_grouped['Neighborhood']
        CDMX_grouped_clustering = CDMX_grouped.drop('Neighborhood', 1)
        for ind in np.arange(CDMX_grouped.shape[0]):
            neighborhoods_venues_sorted.iloc[ind, 1:] = return_most_common_venues(CDMX_grouped.iloc[ind, :], num_top_venues)
        distortions = []
        K = range(1,10)
        for k in K:
            kmeanModel = KMeans(n_clusters=k, random_state=0)
            kmeanModel.fit(CDMX_grouped_clustering )
            distortions.append(kmeanModel.inertia_)

        # Davies Bouldin score for K means
        def get_kmeans_score(data, center):

            #instantiate kmeans
            kmeans = KMeans(n_clusters=center)
            # Then fit the model to your data using the fit method
            model = kmeans.fit_predict(CDMX_grouped_clustering)
    
            # Calculate Davies Bouldin score
            score = davies_bouldin_score(CDMX_grouped_clustering, model)
    
            return score
        scores = []
        centers = list(range(2,25))
        for center in centers:
            scores.append(get_kmeans_score(CDMX_grouped_clustering, center))
        kclusters = 12
        kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(CDMX_grouped_clustering)

        neighborhoods_venues_sorted.insert(0,'Cluster Labels', kmeans.labels_)
        CDMX_merged = CDMX_venues2.copy()
        nan_rows1 = neighborhoods_venues_sorted[neighborhoods_venues_sorted.isnull().any(1)]
        CDMX_merged = CDMX_merged.join(neighborhoods_venues_sorted.set_index('Neighborhood'), on='Neighborhood')
        nan_rows2 = CDMX_merged[CDMX_merged.isnull().any(1)]
        CDMX_merged.to_csv('venues_kmeans.csv', index=False)
        return send_file('venues_kmeans.csv', as_attachment=True)
    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)


#from flask import Flask, request
#import json
#import psycopg2
#import psycopg2.extras
#import os
# Estructura del uri:
# "motor://user:password@host:port/database"
#database_uri = f'postgresql://{os.environ["PGUSR"]}:{os.environ["PGPASS"]}@{os.environ["PGHOST"]}:5432/{os.environ["PGDB"]}'

#app = Flask(__name__)
#conn = psycopg2.connect(database_uri)

#@app.route('/')
#def home():
#    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
#    cur.execute("select * from users")
#    results = cur.fetchall()
#    cur.close()
#    return json.dumps([x._asdict() for x in results], default=str)


#@app.route('/users', methods=["POST", "GET", "DELETE", "PATCH"])
#def user():
#    if request.method == 'GET':
#        cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
#        user_id = request.args.get("id")
#        cur.execute(f"select * from users where id={user_id}")
#        results = cur.fetchone()
#        cur.close()
#        return json.dumps(results._asdict(), default=str)
#    if request.method == "POST":
#        user = json.loads(request.data)
#        cur = conn.cursor()
#        cur.execute(
#            "insert into users (name, lastname, age) values (%s, %s, %s)",
#            (user[0]["name"], user[0]["lastname"], user[0]["age"]),
#        )
#        conn.commit()
#        cur.execute("SELECT LASTVAL()")
#        user_id = cur.fetchone()[0]
#        cur.close()
#        return json.dumps({"user_id": user_id})
#    if request.method == "DELETE":
#        cur = conn.cursor()
#        user_id = request.args.get("id")
#        cur.execute(f"delete from users where id={user_id}")
#        conn.commit()
#        cur.close()
#        return json.dumps({"user_id": user_id})
#    if request.method == "PATCH":
#        user = json.loads(request.data)
#        cur = conn.cursor()
#        user_id = request.args.get("id")
#        cur.execute(
#            "update users set (name, lastname, age) = (%s,%s,%s) where id=%s ",
#            (user[0]["name"], user[0]["lastname"], user[0]["age"], user_id),
#        )
#        conn.commit()
#        cur.close()
#        return json.dumps({"user_id": user_id})


#@app.route('/flights', methods=['GET'])
#def flights():
#    cur = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
#    user_id = request.args.get("id")
#    cur.execute(f"select * from flights limit 100")
#    results = cur.fetchall()
#    cur.close()
#    return json.dumps([x._asdict() for x in results], default=str)


#if __name__ == "__main__":
#    app.run(host="0.0.0.0", debug=True, port=8080)
