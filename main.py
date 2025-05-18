from flask import Flask, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn
import pandas as pd

app = Flask(__name__)

@app.route('/plot', methods=['POST'])
def plot():
    content = request.json
    df = pd.DataFrame(content['data'])
    plot_type = content.get("plot_type", "line")
    xlabel = content.get("xlabel", "")
    ylabel = content.get("ylabel", "")
    title = content.get("title", "")
    colors = content.get("colors", ["blue"])

    plt.clf()
    seaborn.set_style("whitegrid")

    if plot_type == "line":
        seaborn.lineplot(data=df, palette=colors)
    elif plot_type == "bar":
        seaborn.barplot(x=df.columns[0], y=df.columns[1], data=df, palette=colors)
    else:
        return jsonify({"error": "Invalid plot type"}), 400

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plot_path = "static/plot.png"
    plt.savefig(plot_path)

    return send_file(plot_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

