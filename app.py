import boto3
from flask import Flask, render_template, url_for

app = Flask(__name__)


def get_data():
    session = boto3.Session(profile_name="bishweashwar-sukla")
    s3_client = session.client("s3")
    bucket_name = "tiger-mle-pg"
    response = s3_client.list_objects_v2(
        Bucket=bucket_name, Prefix="home/bishweashwar.sukla/", Delimiter="/"
    )
    sub_folder = []
    for x in response.get("CommonPrefixes"):
        sub_folder.append(x.get("Prefix"))
    # Print the files within each subfolder
    s3_resource = session.resource("s3")
    my_bucket = s3_resource.Bucket(bucket_name)
    dictionary = {}
    for i in sub_folder:
        for j in my_bucket.objects.filter(Prefix=i):
            if j.key != i:
                dictionary[i] = j.key.replace(i, "")
    return dictionary


@app.route("/")
@app.route("/home")
def home():
    posts = get_data()
    return render_template("index.html", posts=posts, title="Demo")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)
