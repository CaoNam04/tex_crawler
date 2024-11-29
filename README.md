crawl tex tags of formula, figure, table

1 Tải Miktex để làm tool render tex -> image (update full package ngay khi vào miktex console)

2 Add path của miktex vào environment

3 Tải file arxiv dưới source là latex, giải nén

4 Chạy file crawl.py để crawl tag formula, figure,table bên trong folder giải nén vào lưu giữ vào file .json

5 Chạy file process.py để render tex tag sang image

Note: nhiều tag ko render đc, mới đa phần là formula chạy đc tốt
