from google_play_scraper import Sort, reviews
import csv

""" This file contains utility functions to fetch users reviews of an android application
 from Google Play Store. We will fetch"""

""" This function fetch reviews of an app page by page as a json format using 
google_play_scraper library, and save those data as rows into a csv file. 
Inputs->  app_package_name: app package name or identifier name in play store.
          filename: reviews data will be store here.
          number_of_reviews: how many review we want to fetch.
          limit: how many reviews to fetch per api call. """
def fetch_reviews_from_play_store(app_package_name, filename, number_of_reviews, limit):
    total_reviews_fetched = 0

    # fetching initial reviews page
    results, continuation_token = reviews(
        app_package_name,  # app identifier or app package name
        lang='en',  # defaults to 'en'
        country='us',  # defaults to 'us'
        sort=Sort.NEWEST,  # defaults to Sort.NEWEST
        count=limit,  # defaults to 100
    )

    # creating a csv file
    create_a_csv_file_with_columns(filename)
    # appending records into a csv file
    append_records_into_csv_file(filename, convert_reviews_into_records(results))

    total_reviews_fetched += len(results)

    # fetching reviews page by page until we fetch reviews equal to no_of_reviews
    while total_reviews_fetched < number_of_reviews:
        results, continuation_token = reviews(
            app_package_name,
            continuation_token=continuation_token  # load from the point where last review was fetched
        )
        # appending records into a csv file
        append_records_into_csv_file(filename, convert_reviews_into_records(results))

        total_reviews_fetched += len(results)

    return total_reviews_fetched


# this function create or replace an existing csv file with reviews columns name
def create_a_csv_file_with_columns(filename):
    columns = ['reviewId', 'userName', 'userImage', 'content',
               'score', 'thumbsUpCount', 'reviewCreatedVersion', 'at',
               'replyContent', 'repliedAt']
    # creating or replacing an existing csv file
    with open(filename, 'w', encoding="utf-8") as csvfile:
        # csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the columns
        csvwriter.writerow(columns)
        # closing the file
        csvfile.close()


# this function appends reviews into the csv file
def append_records_into_csv_file(filename, records):
    # opening a file to append data
    with open(filename, 'a', encoding="utf-8") as csvfile:
        # csv writer object
        csvwriter = csv.writer(csvfile)
        # writing new records
        csvwriter.writerows(records)
        # closing the file
        csvfile.close()


# this function convert each review dict object as a record in the csv file
def convert_review_into_record(review):
    # taking each key's value from review dict
    review_id = review['reviewId']
    user_name = review['userName']
    user_image = review['userImage']
    content = review['content']
    score = review['score']
    thumbs_up_count = review['thumbsUpCount']
    review_created_version = review['reviewCreatedVersion']
    at = review['at']
    reply_content = review['replyContent']
    replied_at = review['repliedAt']

    # returning values as a list
    return [review_id, user_name, user_image, content,
            score, thumbs_up_count, review_created_version,
            at, reply_content, replied_at]


# this function converts reviews dict list into records list
def convert_reviews_into_records(results):
    records = []
    for item in results:
        records.append(convert_review_into_record(item))
    return records

# total_reviews_fetched = fetch_reviews_from_play_store("com.facebook.katana", "../Data/reviews.csv", 40, 20)
# print("Total review fetched: " + str(total_reviews_fetched))

# print("Fetching reviews started...")
# total_review_fetched = fetch_reviews_from_play_store(
   
# print("Total reviews fetched : " + str(total_review_fetched))

if __name__ == '__main__':
    app_package_name="com.facebook.katana"
    filename="play_store_reviews1.csv"
    number_of_reviews=3000
    limit=20
    fetch_reviews_from_play_store(app_package_name, filename, number_of_reviews, limit)