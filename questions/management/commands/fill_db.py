from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import Tag, Question, Answer, QuestionLikes, AnswerLikes
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
    questions_per_user = max(1, (ratio * 10) // len(users))
    
    question_index = 0
    for user in users:
        for _ in range(questions_per_user):
            if question_index >= ratio * 10:
                break
            question = Question(
                title=f"Вопрос #{question_index}",
                content=f"Содержание вопроса {question_index}",
                author=user,
                likes=0,
                answers_cnt=0,
            )
            questions.append(question)
            question_index += 1
    
    return questions

def form_answers(questions, users):
    answers = []
    answers_per_question = 3
    
    for question in questions:
        answer_users = sample(users, min(answers_per_question, len(users)))
        for user in answer_users:
            answer = Answer(
                question=question,
                author=user,
                content=f"Ответ на вопрос '{question.title}'",
                likes=0,
                is_correct=0
            )
            answers.append(answer)
    
    return answers

def form_question_likes(questions, users):
    likes = []
    pairs = set()
    
    for question in questions:
        likers_count = randint(0, len(users) // 2)
        likers = sample(users, min(likers_count, len(users)))
        
        for user in likers:
            if (user.id, question.id) in pairs:
                continue
                
            like_type = randint(0, 1)
            like = QuestionLikes(
                question=question,
                user=user,
                type=like_type,
                is_active=True
            )
            likes.append(like)
            pairs.add((user.id, question.id))
    
    return likes

def form_answer_likes(answers, users):
    likes = []
    pairs = set()
    
    for answer in answers:
        likers_count = randint(0, len(users) // 3)
        likers = sample(users, min(likers_count, len(users)))
        
        for user in likers:
            if (user.id, answer.id) in pairs:
                continue
                
            like_type = randint(0, 1)
            like = AnswerLikes(
                answer=answer,
                user=user,
                type=like_type,
                is_active=True
            )
            likes.append(like)
            pairs.add((user.id, answer.id))
    
    return likes

def update_question_stats(questions):
    for question in questions:
        answers = Answer.objects.filter(question=question)
        question.answers_cnt = answers.count()
        
        likes = QuestionLikes.objects.filter(question=question, is_active=True)
        like_count = likes.filter(type=1).count()
        dislike_count = likes.filter(type=0).count()
        question.likes = like_count - dislike_count
        
        question.save(update_fields=['answers_cnt', 'likes'])

def update_answer_stats(answers):
    for answer in answers:
        likes = AnswerLikes.objects.filter(answer=answer, is_active=True)
        like_count = likes.filter(type=1).count()
        dislike_count = likes.filter(type=0).count()
        answer.likes = like_count - dislike_count
        
        answer.save(update_fields=['likes'])

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
        questions = form_questions(users, tags, ratio)
        created_questions = Question.objects.bulk_create(questions, batch_size=batch_size)
        print(f"Создано {len(created_questions)} вопросов")

        questions = list(Question.objects.all())
        answers = form_answers(questions, users)
        created_answers = Answer.objects.bulk_create(answers, batch_size=batch_size)
        print(f"Создано {len(created_answers)} ответов")

        for question in questions:
            question_tags = sample(tags, randint(2, min(5, len(tags))))
            question.tags.set(question_tags)
        print("Теги установлены для вопросов")

        question_likes = form_question_likes(questions, users)
        created_question_likes = QuestionLikes.objects.bulk_create(question_likes, batch_size=batch_size)
        print(f"Создано {len(created_question_likes)} лайков на вопросы")

        answers = list(Answer.objects.all())
        answer_likes = form_answer_likes(answers, users)
        created_answer_likes = AnswerLikes.objects.bulk_create(answer_likes, batch_size=batch_size)
        print(f"Создано {len(created_answer_likes)} лайков на ответы")

        update_question_stats(questions)

        update_answer_stats(answers)