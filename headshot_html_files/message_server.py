import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import datetime
import smtplib


class MessageHandler(tornado.web.RequestHandler):
    def set_headers(self):
        self.set_header("Content-Type", "application/javascript")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header('Access-Control-Allow-Origin','*');
        self.set_header('Access-Control-Allow-Methods',
                         'POST, GET, PUT, PATCH, DELETE, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, Content-Range, Content-Disposition, Content-Description');

    def post(self):
        self.set_headers()
        a = self.request.body
        a = a.split('&')
        print a
        outlist = []
        outlist.append([ele.replace('Name=', 'Name = ') for ele in a if ele.startswith('Name')][0])
        outlist.append([ele.replace('%40','@').replace('Email=', 'Email = ') for ele in a if ele.startswith('Email')][0])
        outlist.append([ele.replace('subject=', 'Subject = ') for ele in a if ele.startswith('subject')][0])
        outlist.append([ele.replace('Message=', 'Message = ') for ele in a if ele.startswith('Message')][0])
        outstr = '\n'.join(outlist)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("quizzycashdb@gmail.com", "quizzycash_db")
        server.sendmail("quizzycashdb@gmail.com", "playwithus@quizzycash.com", outstr)
        server.quit()
        with open('Messages.log', 'a') as fp:
            time = datetime.datetime.utcnow()
            fp.write(self.request.body + "\n" + str(time))
        self.finish({'success': {'code': 200,
                                'message': 'Successful'}})

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/saveMesssage/", MessageHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


if __name__ == "__main__":
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(9080)
    ioloop =tornado.ioloop.IOLoop.instance()
    ioloop.start()
