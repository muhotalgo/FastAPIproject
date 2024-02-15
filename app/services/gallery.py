import os
from datetime import datetime

import requests
from sqlalchemy import insert, select, update, func, or_

from app.dbfactory import Session
from app.models.gallery import Gallery

# 이미지 파일 저장 경로 설정
UPLOAD_DIR = r'C:\Java\nginx-1.25.3\html\cdn'


class GalleryService():
    @staticmethod
    def gallery_convert(gdto):
        data = gdto.model_dump()
        # data.pop('response')  # captcha 확인용 변수 response는 제거
        bd = Gallery(**data)
        data = {'userid': bd.userid, 'title': bd.title,
                'contents': bd.contents}
        return data

    @staticmethod
    def insert_gallery(gdto, fname, fsize):
        data = GalleryService.gallery_convert(gdto)
        with Session() as sess:
            stmt = insert(Gallery).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result

    @staticmethod
    async def proccess_upload(attach):
        today = datetime.today().strftime('%Y%m%d%H%M%S')
        nfname = f'{today}{attach.filename}'    # 파일 이름
        fsize = attach.size     # 파일 크기
        # os.path.join(A, B) => A/B (경로 생성)
        fname = os.path.join(UPLOAD_DIR, nfname)

        # 비동기 처리를 위해 함수에 await 지시자 추가
        # 이럴 경우 함수 정의부분에 async 라는 지시자 추가 필요!
        content = await attach.read()  # 업로드한 파일의 내용을 비동기로 모두 읽어옴

        with open(fname, 'wb') as f:
            f.write(content)  # 파일의 내용을 지정한 파일이름으로 저장

        return nfname, fsize

    # @staticmethod
    # def select_gallery(cpg):
    #     stnum = (cpg - 1) * 25
    #     with Session() as sess:
    #         cnt = sess.query(func.count(Gallery.bno)).scalar()  # 총 게시글 수
    #
    #         stmt = select(Gallery.bno, Gallery.title, Gallery.userid, Gallery.regdate, Gallery.views) \
    #             .order_by(Gallery.bno.desc()).offset(stnum).limit(25)
    #         result = sess.execute(stmt)
    #     return result, cnt

    # @staticmethod
    # def find_select_gallery(ftype, fkey, cpg):
    #     stnum = (cpg - 1) * 25
    #     with Session() as sess:
    #         stmt = select(Gallery.bno, Gallery.title, Gallery.userid, Gallery.regdate, Gallery.views)
    #
    #         # 동적 쿼리 작성 - 조건에 따라 where절이 바뀜
    #         myfilter = Gallery.title.like(fkey)
    #         if ftype == 'userid':
    #             myfilter = Gallery.userid.like(fkey)
    #         elif ftype == 'contents':
    #             myfilter = Gallery.contents.like(fkey)
    #         elif ftype == 'titconts':
    #             myfilter = or_(Gallery.title.like(fkey), Gallery.contents.like(fkey))
    #
    #         stmt = stmt.filter(myfilter) \
    #             .order_by(Gallery.bno.desc()).offset(stnum).limit(25)
    #         result = sess.execute(stmt)
    #
    #         cnt = sess.query(func.count(Gallery.bno)) \
    #             .filter(myfilter).scalar()  # 총 게시글 수
    #
    #     return result, cnt

    # @staticmethod
    # def selectone_gallery(bno):
    #     with Session() as sess:
    #         stmt = select(Gallery).filter_by(bno=bno)
    #         result = sess.execute(stmt).first()
    #     return result
    #
    # @staticmethod
    # def update_count_gallery(bno):
    #     with Session() as sess:
    #         stmt = update(Gallery).filter_by(bno=bno).values(views=Gallery.views + 1)
    #         result = sess.execute(stmt)
    #         sess.commit()
    #
    #     return result
    #
    # @staticmethod
    # def check_captcha(gdto):
    #     data = gdto.model_dump()  # 클라이언트가 보낸 객체를 dict로 변환
    #     req_url = 'https://www.google.com/recaptcha/api/siteverify'
    #     params = {'secret': '',
    #               'response': data['response']}
    #     res = requests.get(req_url, params=params)
    #     result = res.json()
    #     # print('check', result)
    #
    #     # return result['success']
    #     return True
