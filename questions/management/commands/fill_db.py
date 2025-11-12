from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import Tag, Question, Answer, QuestionLikes, AnswerLikes, Profile
from random import choices, randint, sample 
from string import ascii_lowercase

def form_users(ratio):
    users = []
    for i in range(ratio):
        username = f"user_{i}"
        user = User(username=username, email=f"{username}@m.ru")
        users.append(user)
    return users

def form_tags(ratio):
    tags = []
    for _ in range(ratio):
        tag_name = ''.join(choices(ascii_lowercase, k=7))
        tag = Tag(name=tag_name)
        tags.append(tag)
    return tags

def form_questions(users, tags, ratio):
    questions = []
    for i in range(ratio):
        user = users[randint(0, len(users)-1)]
        question = Question(
            title=f"Вопрос {i}",
            content=f"Содержание вопроса {i}",
            author=user,
            likes = randint(0, 100),
            answers_cnt = randint(0, 100),
        )
        questions.append(question)
    return questions

def form_answers(questions, users):
    answers = []
    len_ans = len(questions)
    for question in questions[:-len(users)//100]:  
        if len(answers) == len_ans * 10:
            break
        for _ in range(15):
            user = users[randint(0, len(users)-1)]
            answer = Answer(
                question=question,
                author=user,
                content=f"Ответ на вопрос c id {question.id} ({question.title})",
                likes = randint(0, 100),
            )
            answers.append(answer)
    return answers

def form_question_likes(questions, users, ratio):
    likes = []
    pairs = set() 
    for _ in range(ratio * 3):  
        if len(likes) >= ratio:
            break
        question = questions[randint(0, len(questions)-1)]
        user = users[randint(0, len(users)-1)]
        
        if (user.id, question.id) in pairs:
            continue
    
        like = QuestionLikes(question=question, user=user)
        likes.append(like)
        pairs.add((user.id, question.id))
        
    return likes

def form_answer_likes(answers, users, ratio):
    likes = []
    pairs = set() 
    
    for _ in range(ratio * 3):  
        if len(likes) >= ratio:
            break
            
        answer = answers[randint(0, len(answers)-1)]
        user = users[randint(0, len(users)-1)]
 
        if (user.id, answer.id) in pairs:
            continue
            
        like = AnswerLikes(answer=answer, user=user)
        likes.append(like)
        pairs.add((user.id, answer.id))
        
    return likes

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--ratio", type=int)

    def handle(self, *args, **options):
        batch_size = 100
        User.objects.filter(is_staff=False).delete()
        QuestionLikes.objects.all().delete()
        AnswerLikes.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()

        ratio = options["ratio"]

        users = User.objects.bulk_create(form_users(ratio), batch_size=batch_size)
        print(f"Создано {len(users)} пользователей")

        tags = Tag.objects.bulk_create(form_tags(ratio), batch_size=batch_size)
        print(f"Создано {len(tags)} тегов")

        users = list(User.objects.all())
        questions = form_questions(users, tags, ratio * 10)
        created_questions = Question.objects.bulk_create(questions, batch_size=batch_size)
        print(f"Создано {len(created_questions)} вопросов")

        questions = list(Question.objects.all())
        answers = form_answers(questions, users)
        created_answers = Answer.objects.bulk_create(answers, batch_size=batch_size)
        print(f"Создано {len(created_answers)} ответов")

        for question in created_questions:
            question_tags = sample(tags, randint(2, 5))
            question.tags.set(question_tags)
        print("Теги установлены для вопросов")


        # Лайки не формирую, потому что пока они не отобразятся (у меня денормализующие поля)
        #answers = list(Answer.objects.all())
        #question_likes = form_question_likes(questions, users, ratio * 100)
        #created_question_likes = QuestionLikes.objects.bulk_create(question_likes, batch_size=batch_size)
        #print(f"Создано {len(created_question_likes)} лайков на вопросы")

       
        # answer_likes = form_answer_likes(answers, users, ratio * 100)
        # created_answer_likes = AnswerLikes.objects.bulk_create(answer_likes, batch_size=batch_size)
        # print(f"Создано {len(created_answer_likes)} лайков на ответы")