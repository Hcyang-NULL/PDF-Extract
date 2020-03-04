import tornado
import tornado.web
import tornado.ioloop
import os
import time
import traceback
from pdf_process import *


current_path = os.path.dirname(__file__)


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template.html", js_code='', trans_id='0', pdf_code='', trans_result='', file_label='Choose file')


class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            file_metas = self.request.files["pdf_file"]
            # only support one file
            trans_id = '0'
            file_label = 'Choose file'
            for meta in file_metas:
                file_name = meta['filename']
                print(f'file_name: {file_name}')
                file_label = file_name
                trans_id = str(time.time()).replace('.', '')
                gen_name = trans_id + '.pdf'
                file_path = os.path.join('./bootstrap/pdf', gen_name)
                with open(file_path, 'wb') as f:
                    f.write(meta['body'])
                break
            print(f'trans_id: {trans_id}')
            js_code = '''alert("上传成功");$("#choose").empty();'''
            self.render("template.html", js_code=js_code, trans_id=trans_id, pdf_code='', trans_result='', file_label=file_label)
        except Exception as e:
            traceback.print_exc()
            js_code = '''alert("上传失败");$("#choose").empty();'''
            self.render("template.html", js_code=js_code, trans_id='0', pdf_code='', trans_result='', file_label=file_label)


class TransHandler(tornado.web.RequestHandler):
    def post(self, trans_id):
        try:
            trans_id = int(trans_id)
        except:
            self.render("template.html", js_code='alert("非法操作")', trans_id='0', pdf_code='', trans_result='', file_label='Choose file')
            return
        if trans_id == 0:
            self.render("template.html", js_code='alert("请先上传PDF文件")', trans_id='0', pdf_code='', trans_result='', file_label='Choose file')
            return
        else:
            file_path = os.path.join('./bootstrap/pdf', str(trans_id) + '.pdf')
            content = read_pdf(file_path)
            pdf_code = 'PDFObject.embed("/static/pdf/' + str(trans_id) + '.pdf", "#pdf");'
            js_code = '''$("#choose").append('<input type="file" class="custom-file-input" id="inputGroupFile03" name="pdf_file">');'''
            self.render("template.html", js_code=js_code, trans_id=trans_id, pdf_code=pdf_code, trans_result=content, file_label='Choose file again')


def init():
    app = tornado.web.Application(
        handlers = [
            (r'/', HomeHandler),
            (r'/pdf_upload', UploadHandler),
            (r'/pdf_trans/(?P<trans_id>\d*)', TransHandler)
        ],
        template_path='template',
        static_path=os.path.join(os.path.dirname(__file__),"bootstrap"),
        debug=True
    )
    return app


if __name__ == '__main__':
    app = init()
    app.listen(8021)
    tornado.ioloop.IOLoop.current().start()
