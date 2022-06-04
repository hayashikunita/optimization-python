import urllib
from requests_oauthlib import  OAuth1
import requests


def main():

    # APIの秘密鍵
    CK = 'xxxxxx'
    CKS = 'xxxxxx'
    AT = 'xxxxxx'
    ATS = 'xxxxx'
    # ユーザー・ツイートID
    user_id = '@muratamika2021'
    tweet_id = '1501979094149304320' # str型で指定
    # 検索時のパラメーター
    count = 100 # 一回あたりの検索数(最大100/デフォルトは15)
    range = 100 # 検索回数の上限値(最大180/15分でリセット)

    # ツイート検索・リプライの抽出
    tweets= search_tweets(CK, CKS, AT, ATS, user_id, tweet_id, count, range)

    # 抽出結果を表示
    print(tweets[0:100])


def search_tweets(CK, CKS, AT, ATS, user_id, tweet_id, count, range):
    # 文字列設定
    user_id += ' exclude:retweets' # RTは除く
    user_id = urllib.parse.quote_plus(user_id)
    # リクエスト
    url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+user_id+"&count="+str(count)
    auth = OAuth1(CK, CKS, AT, ATS)
    response = requests.get(url, auth=auth)
    data = response.json()['statuses']

    # ２回目以降のリクエスト
    cnt = 0
    reply_cnt = 0
    tweets = []
    tweetcreated = []
    tweetid = []
    dic ={}
    while True:
        if len(data) == 0:
            break
        cnt += 1
        if cnt > range:
            break
        for tweet in data:
            if tweet['in_reply_to_status_id_str'] == tweet_id: # ツイートIDに一致するものを抽出
                tweets.append(tweet['text']) 
                tweetcreated.append(tweet['created_at']) 
                tweetid.append(tweet['user']['name'])

                reply_cnt += 1
            maxid = int(tweet["id"]) - 1
        url = "https://api.twitter.com/1.1/search/tweets.json?lang=ja&q="+user_id+"&count="+str(count)+"&max_id="+str(maxid)
        response = requests.get(url, auth=auth)
        try:
            data = response.json()['statuses']
        except KeyError: # リクエスト回数が上限に達した場合のデータのエラー処理
            print('上限まで検索しました')
            break
    print('検索回数 :', cnt)
    print('リプライ数 :', reply_cnt)
    return tweets ,tweetcreated, tweetid

if __name__ == '__main__':
    main()
