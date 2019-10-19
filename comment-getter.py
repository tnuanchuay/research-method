import os
import googleapiclient.discovery
import sys
import json

class CommentsGetter:
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    MAX_COMMENT_COUNT = 300

    def __init__(self, videoId, api_key):
        self.VideoId = videoId
        self.YouTube = googleapiclient.discovery.build(self.API_SERVICE_NAME, self.API_VERSION, developerKey=api_key)
        self.progress = 0;

    def __getCommentListFromVideoId(self, nextPageToken, comments):
        if comments is None:
            comments = list()
        elif len(comments) > self.MAX_COMMENT_COUNT:
            return comments

        print(len(comments))

        if nextPageToken is None:
            request = self.YouTube.commentThreads().list(
                part="id",
                videoId=self.VideoId,
                maxResults=100
            )
        else:
            request = self.YouTube.commentThreads().list(
                part="id",
                videoId=self.VideoId,
                maxResults=100,
                pageToken=nextPageToken
            )

        res = request.execute()

        for item in res["items"]:
            comments.append(item["id"])

        if "nextPageToken" in res:
            return self.__getCommentListFromVideoId(res["nextPageToken"], comments)
        else:
            return comments


    def __getComment(self, item):
        request = self.YouTube.comments().list(part="snippet", id=item)
        res = request.execute()
        self.progress = self.progress + 1
        print(self.progress)
        return res["items"][0]["snippet"]["textDisplay"]

    def start(self):
        print("Start")
        comments = map(self.__getComment, self.__getCommentListFromVideoId(None, None))
        f = open(self.VideoId + ".txt", "w")
        f.write(json.dumps(list(comments)))
        print("done")

def main():
    videoId = sys.argv[len(sys.argv) - 1]
    commentGetter = CommentsGetter(videoId, os.environ["API_KEY"])
    commentGetter.start()

if __name__ == "__main__":
    main()
