from celery.schedules import crontab
from jinja2 import Template
from weasyprint import HTML
from mail_config import email_send
from main import celery
from tables import Users,Books,Status,Feedbacks

@celery.task()
def daily_task():
    users=Users.query.all()
    for user in users:
        issued=Status.query.filter(Status.user_id==user.user_id,Status.status_type=="accept").all()
        l=[]
        for i in issued:
            book=Books.query.filter(Books.book_id==i.book_id).first()
            dic={"book_name":book.book_name,"book_author":book.author_name,"expiry":i.expiry}
            l.append(dic)
        
        file=open("templates/daily_rem.html")
        msg=Template(file.read())

        email_send(to=user.email,sub="Daily Reminder",msg=msg.render(username=user.user_name,expire_list=l))
    return 'sent'


@celery.task()
def monthly_task():
    books=Books.query.all()
    l=[]
    l1=[]
    for i in books:
        total_score=0
        counter=0
        feedbacks=Feedbacks.query.filter(Feedbacks.book_id==i.book_id).all()
        for j in feedbacks:
            total_score+=float(j.feedback_score)
            counter+=1
        if counter>0:

            l.append({"book_name":i.book_name,"book_author":i.author_name,"avg_rating":total_score/counter})
        else:
            l.append({"book_name":i.book_name,"book_author":i.author_name,"avg_rating":0})
    
    q=Status.query.filter(Status.status_type=="accept").all()
    for i in q:
        q2=Books.query.filter(Books.book_id == i.book_id).first()
        q1=Users.query.filter(Users.user_id==i.user_id).first()
        l1.append({"book_id":q2.book_id,"book_name":q2.book_name,"book_author":q2.author_name,"book_cover":q2.book_cover,"user_id":q1.user_id,"user_name":q1.user_name,"email":q1.email,"profile_pic":q1.profile_pic,"status_id":i.status_id,"expiry":i.expiry,"price":i.price,"status_type":i.status_type})
    file=open("templates/monthly_task.html")
    msg=Template(file.read())
    file1=open("templates/pdf.html")
    report=Template(file1.read())

    pdf_report=HTML(string=report.render(ratings_list=l,issued_list=l1))

    pdf_report.write_pdf(target="static/monthly_activity.pdf")

    email_send(to="admin2004@gmail.com",sub="Monthly Report",attach="static/monthly_activity.pdf",msg=msg.render())

    return 'sent'

@celery.on_after_finalize.connect
def setup_tasks(sender,**kwargs):
    #crontab(minute=0,hour=20)
    sender.add_periodic_task(crontab(minute=0,hour=20),daily_task.s(),name="daily_task")
    #crontab(minute=20,hour=17,day_of_month=25)
    sender.add_periodic_task(crontab(minute=20,hour=17,day_of_month=25),monthly_task.s(),name="monthly_task")
    