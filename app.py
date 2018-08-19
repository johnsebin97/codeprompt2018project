from flask import Flask, request, render_template, send_file
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, RadioField
from matplotlib import pyplot as plt
import os


def convertToInt(temp):
    if temp == ['']:
        return [0]
    else:
        result = []
        for i in temp:
            result.append(int(i))
        return result


def getItems(listName, itemNumber):
    temp = []
    for i in listName:
        temp.append(i[itemNumber])
    return temp



def enterString(listName, name):
    temp = []
    for i in listName:
        temp.append(name + str(i))
    return temp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'LOL'


class MainForm(FlaskForm):
    productName = StringField('productName')
    itemsSold = StringField('itemsSold')
    costPrice = StringField('costPrice')
    sellPrice = StringField('sellPrice')
    addButton = SubmitField('Add')
    graphType = RadioField('Type of Graph', choices=[('line', 'Line Graph'), ('bar', 'Bar Graph')], default='line')
    lineColor = RadioField('Color of Line', choices=[('r', 'Red'), ('g', 'Green'), ('b', 'Blue')], default='r')
    lineType = RadioField('Type of Line', choices=[('-', 'Solid'), ('--', 'Dashed'), ('-.', 'Dash-Dotted'), (':', 'Dotted')], default='-')
    finalSubmit = SubmitField('Submit')
    downloadButton = SubmitField('Download')



allEntries = []
newEntry = []
profit = 0
totalProfit = 0


@app.route('/', methods=['POST', 'GET'])
def index_post():
    day = len(allEntries)
    if request.method == 'GET':
        form = MainForm()
        return render_template('index.html', form=form)
    elif request.method == 'POST':
        form = MainForm()
        if form.validate_on_submit():
            if form.addButton.data:
                newEntry = []
                newEntry.append(day)
                newEntry.append(int(form.itemsSold.data))
                newEntry.append(int(form.costPrice.data))
                newEntry.append(int(form.sellPrice.data))
                profit = int(int(form.sellPrice.data) - int(form.costPrice.data))
                newEntry.append(profit)
                totalProfit = int(profit * int(form.itemsSold.data))
                newEntry.append(totalProfit)
                form.itemsSold.data = ""
                form.costPrice.data = ""
                form.sellPrice.data = ""
                allEntries.append(newEntry)
                # newEntry is like [Day Number, Items Sold, Cost Price, Sell Price, Profit for each item, Total Profit]
            elif form.finalSubmit.data:
                dates = getItems(allEntries, 0)
                dates = enterString(dates, "Day ")
                profitPlot = getItems(allEntries, 5)
                plt.xlabel("Days")
                plt.ylabel("Total Profit")
                plt.title(form.productName.data)
                if form.graphType.data == 'line':
                    plt.plot(dates, profitPlot, color=form.lineColor.data, linestyle=form.lineType.data)
                elif form.graphType.data == 'bar':
                    plt.bar(dates, profitPlot)
                from io import BytesIO
                figfile = BytesIO()
                plt.savefig(figfile, format='png')
                figfile.seek(0)
                import base64
                figdata_png = base64.b64encode(figfile.getvalue())
                return render_template('index.html', form=form, days=allEntries, graph=figdata_png.decode('utf8'))
            elif form.downloadButton.data:
                plt.savefig("graph")
        return render_template('index.html', form=form, days=allEntries)


if __name__ == '__main__':
    app.run(debug=True)