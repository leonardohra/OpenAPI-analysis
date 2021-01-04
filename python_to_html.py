import os

def generate_html_pretty_table():
    html = """<style>
    @import "https://fonts.googleapis.com/css?family=Montserrat:300,400,700";
    .rwd-table {
      margin: 1em 0;
      min-width: 300px;
    }
    .rwd-table tr {
      border-top: 1px solid #ddd;
      border-bottom: 1px solid #ddd;
    }
    .rwd-table th {
      display: none;
    }
    .rwd-table td {
      display: block;
    }
    .rwd-table td:first-child {
      padding-top: .5em;
    }
    .rwd-table td:last-child {
      padding-bottom: .5em;
    }
    .rwd-table td:before {
      content: attr(data-th) ": ";
      font-weight: bold;
      width: 6.5em;
      display: inline-block;
    }
    @media (min-width: 480px) {
      .rwd-table td:before {
        display: none;
      }
    }
    .rwd-table th, .rwd-table td {
      text-align: left;
    }
    @media (min-width: 480px) {
      .rwd-table th, .rwd-table td {
        display: table-cell;
        padding: .25em .5em;
      }
      .rwd-table th:first-child, .rwd-table td:first-child {
        padding-left: 0;
      }
      .rwd-table th:last-child, .rwd-table td:last-child {
        padding-right: 0;
      }
    }


    h1 {
      font-weight: normal;
      letter-spacing: -1px;
      color: #34495E;
    }

    .rwd-table {
      background: #34495E;
      color: #fff;
      border-radius: .4em;
      overflow: hidden;
    }
    .rwd-table tr {
      border-color: #46637f;
    }
    .rwd-table th, .rwd-table td {
      margin: .5em 1em;
    }
    @media (min-width: 480px) {
      .rwd-table th, .rwd-table td {
        padding: 1em !important;
      }
    }
    .rwd-table th, .rwd-table td:before {
      color: #dd5;
    }
    </style>
    <script>
      window.console = window.console || function(t) {};
    </script>
    <script>
      if (document.location.search.match(/type=embed/gi)) {
        window.parent.postMessage("resize", "*");
      }
    </script>


    <h1>Open API Analysis</h1>
    <table class="rwd-table">
    <tr>

      <table class="rwd-table">
    <tr>
    <th>Topic</th>
    <th>Topic Words</th>
    <th>Endpoint</th>
    <th>Score</th>
    </tr>


    <---content_topics--->

    <tr>

      <table class="rwd-table">
    <tr>
    <th>Topic</th>
    <th>Coherence</th>
    <th>Average Score</th>
    <th>Standard deviation scores</th>
    <th>Average Weights</th>
    <th>Standard deviation Weights</th>
    <th>Endpoint quantity</th>
    </tr>

    <---content_statistics--->


    </table>"""
    return html

# ================================== Python ===
def define_topic_info(csv_vals, html):
    lines = len(csv_vals) // 4

    placeholders = """
    <tr>
    <td data-th="Topic">{}</td>
    <td data-th="Topic Words">{}</td>
    <td data-th="Endpoint">{}</td>
    <td data-th="Score">{}</td>
    </tr>"""*lines

    print(csv_vals)
    placeholders = placeholders.format(*csv_vals)
    html = html.replace("<---content_topics--->", placeholders)
    return html

def define_statistical_info(csv_vals, html):
    lines = len(csv_vals) // 7

    placeholders = """
    <tr>
    <td data-th="Topic">{}</td>
    <td data-th="Coherence">{}</td>
    <td data-th="Average Score">{}</td>
    <td data-th="Standard deviation scores">{}</td>
    <td data-th="Average Weights">{}</td>
    <td data-th="Standard deviation Weights">{}</td>
    <td data-th="Endpoint quantity">{}</td>
    </tr>"""*lines

    print(csv_vals)
    placeholders = placeholders.format(*csv_vals)
    html = html.replace("<---content_statistics--->", placeholders)
    return html

def create_html(csv_topics, csv_statistics):
    html = generate_html_pretty_table()
    print(type(html))

    html = define_topic_info(csv_topics, html)
    print(type(html))
    html = define_statistical_info(csv_statistics, html)
    print(type(html))

    myfile = "table.html"
    with open(myfile, "w") as file:
        file.write(html)

    os.startfile(myfile)
