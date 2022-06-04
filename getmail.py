
import imaplib
import email
import base64
from email.header import decode_header, make_header



ADDRESS = "aaa@gmail.com"
PASSWORD = ""
imapobj = imaplib.IMAP4_SSL("imap.gmail.com", '993')
imapobj.login(ADDRESS, PASSWORD)

#workラベル下のメールを取得
imapobj.select()
typ, data = imapobj.search(None, 'ALL')

#取得したメールから表題と本文を出力し、添付ファイルを同階層に書き出す
for num in data[0].split():
    typ, data = imapobj.fetch(num, '(RFC822)')

    #メール内容(タイトル、本文、添付ファイルなど)
    mail = email.message_from_string(data[0][1].decode('utf-8'))

    #表題出力
    subject = str(make_header(decode_header(mail["Subject"])))
    print(f"タイトル：{subject}")
    

    # message = mail.get_payload()
    # print(f"メッセージ：{message}")


    body = ""
    if mail.is_multipart():
        for payload in mail.get_payload():
            if payload.get_content_type() == "text/plain":
                body = payload.get_payload()

                print(base64.b64decode(body).decode())

    else:
        if mail.get_content_type() == "text/plain":
            body = mail.get_payload()

imapobj.close()


# PythonでGMAILの本文を日本語で取得したい
# https://ja.stackoverflow.com/questions/83465/python%E3%81%A7gmail%E3%81%AE%E6%9C%AC%E6%96%87%E3%82%92%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%81%A7%E5%8F%96%E5%BE%97%E3%81%97%E3%81%9F%E3%81%84
