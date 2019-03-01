import os
from flask import Flask, request, render_template, g, redirect, Response, session, abort,flash
import pandas as pd
import io
import requests
import pandasql as ps

# flask... magic
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# width and height of svg
width = 800 
height = 757

# the altitude and latitude of the SVG
ymax = 40.92
ymin= 40.49
xmin = -74.27
xmax = -73.68

# read data from URL
url = "https://onedrive.live.com/download?cid=1ABF8B3A88607926&resid=1ABF8B3A88607926%2116840&authkey=AFQr6OPqQXwEK6U"
s = requests.get(url).content
data = pd.read_csv(io.StringIO(s.decode('utf-8')))

# re-formate the data
data['INSPECTION_DATE'] = pd.to_datetime(data['INSPECTION_DATE'])
data['YEAR'] = data['INSPECTION_DATE'].dt.year
data['MONTH'] = data['INSPECTION_DATE'].dt.month
data.drop(columns=['ID', 'INSPECTION_DATE'])

def getTable(year, month, boro):
	query = "SELECT LATITUDE,LONGITUDE FROM data WHERE YEAR = %s AND MONTH = %s AND BORO_CODE = %s;" %(year, month, boro)
	result = ps.sqldf(query, locals())
	return result

@app.before_request
def before_request():
	return

@app.teardown_request
def teardown_request(exception):
	return

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/plot', methods = ['GET','POST'])
def plot():
	if request.method != 'POST':
		return render_template("indexPlot.html")

	# request the month
	months = []
	if request.form.get('jan'):
		months.append(int(request.form.get('jan')))
	if request.form.get('feb'):
		months.append(int(request.form.get('feb')))
	if request.form.get('mar'):
		months.append(int(request.form.get('mar')))
	if request.form.get('apr'):
		months.append(int(request.form.get('apr')))
	if request.form.get('may'):
		months.append(int(request.form.get('may')))
	if request.form.get('jue'):
		months.append(int(request.form.get('jue')))
	if request.form.get('jul'):
		months.append(int(request.form.get('jul')))
	if request.form.get('aug'):
		months.append(int(request.form.get('aug')))
	if request.form.get('sep'):
		months.append(int(request.form.get('sep')))
	if request.form.get('oct'):
		months.append(int(request.form.get('oct')))
	if request.form.get('nov'):
		months.append(int(request.form.get('nov')))
	if request.form.get('dec'):
		months.append(int(request.form.get('dec')))
	
	# request the year
	years = []
	if request.form.get('y09'):
		years.append(int(request.form.get('y09')))
	if request.form.get('y10'):
		years.append(int(request.form.get('y10')))
	if request.form.get('y11'):
		years.append(int(request.form.get('y11')))
	if request.form.get('y12'):
		years.append(int(request.form.get('y12')))
	if request.form.get('y13'):
		years.append(int(request.form.get('y13')))
	if request.form.get('y14'):
		years.append(int(request.form.get('y14')))
	if request.form.get('y15'):
		years.append(int(request.form.get('y15')))
	if request.form.get('y16'):
		years.append(int(request.form.get('y16')))
	if request.form.get('y17'):
		years.append(int(request.form.get('y17')))
	if request.form.get('y18'):
		years.append(int(request.form.get('y18')))

	# request the boro
	boros = []
	if request.form.get('b1'):
		boros.append(int(request.form.get('b1')))
	if request.form.get('b2'):
		boros.append(int(request.form.get('b2')))
	if request.form.get('b3'):
		boros.append(int(request.form.get('b3')))
	if request.form.get('b4'):
		boros.append(int(request.form.get('b4')))
	if request.form.get('b5'):
		boros.append(int(request.form.get('b5')))

	
	# subset the data

	# start with month
	subset_m = data[data['YEAR'] == -1] # empty set
	if len(months) != 0:
		for i in months:
			subset_m = pd.concat([subset_m, data[data['MONTH'] == i]])
	else:
		subset_m = data # if select nothing, it means select all

	# handling the year
	subset_my = subset_m[subset_m['YEAR'] == -1] # empty set
	if len(years) != 0:
		for i in years:
			subset_my = pd.concat([subset_my, subset_m[subset_m['YEAR'] == i]])
	else:
		subset_my = subset_m

	# handling the boros
	subset = subset_my[subset_my['YEAR'] == -1] # empty set
	if len(boros) != 0:
		for i in boros:
			subset = pd.concat([subset, subset_my[subset_my['BORO_CODE'] == i]])
	else:
		subset = subset_my
	
	num_point = len(subset)
	latitude = subset['LATITUDE'].tolist()
	longitude = subset['LONGITUDE'].tolist()
	location = longitude + latitude


	# get the number of different inspection type
	ini_num = len(subset[subset["INSPECTION_TYPE"] == "INITIAL"])
	com_num = len(subset[subset["INSPECTION_TYPE"] == "COMPLIANCE"])
	bai_num = len(subset[subset["INSPECTION_TYPE"] == "BAIT"])
	cle_num = len(subset[subset["INSPECTION_TYPE"] == "CLEAN_UPS"])

	context = dict(data = location)

	return render_template("plot.html", num_point=num_point, **context, 
		xmax=xmax, xmin=xmin, ymax=ymax, ymin=ymin, width=width, height=height,
		ini_num=ini_num, com_num=com_num, bai_num=bai_num, cle_num=cle_num)


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using
        python server.py
    Show the help text using
        python server.py --help
    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
