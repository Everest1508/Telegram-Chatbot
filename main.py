from telegram import ParseMode,InlineKeyboardButton, InlineKeyboardMarkup
import telegram.ext
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext import ConversationHandler,CallbackQueryHandler
from telegram.ext.filters import Filters
from chat_res import chat_res
from datetime import date
# from webscrap import event
# from summarize import summary
import randfacts
from translate import Translator
from langdetect import detect
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import random
import logging
import csv

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)




API_KEY = "6202839270:AAE3bvVPSIVsfUzSgCRO-HRhJwSb7vgsPsU"

def detect_language(text):
    try:
        detected_lang = detect(text)
        return detected_lang
    except:
        return "Unknown"

def translate_to_english(text):
    translator = Translator(to_lang="en", from_lang=detect_language(text))
    translation = translator.translate(text)
    return translation




updater =Updater(API_KEY,use_context=True)

quiz_data = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
    {"question": "What is the square root of 64?", "answer": "8"},
    {"question": "Who painted the Mona Lisa?", "answer": "Leonardo da Vinci"},
    {"question": "Which year did World War II end?", "answer": "1945"},
    {"question": "What is the symbol for the chemical element gold?", "answer": "Au"},
    {"question": "Who wrote the novel 'Pride and Prejudice'?", "answer": "Jane Austen"},
    {"question":"Which country is known as the Land of the Rising Sun?","answer":"Japan"},
    {"question":"What is the largest organ in the human body?","answer":"Skin"},
    {"question":"Which country hosted the 2016 Summer Olympics?","answer":"Brazil"},
    {"question":"Who was the first President of the United States?","answer":"George Washington"},
    {"question":"Who is the CEO of Tesla and SpaceX?","answer":"Elon Musk"},
    {"question":"What does the acronym \"HTML\" stand for?","answer":"Hypertext Markup Language"},
    {"question":"Who was the first person to step foot on the moon?","answer":"Neil Armstrong"},
    {"question":"Which year did the Titanic sink?","answer":"1912"},
    {"question":"What is the smallest unit of matter?","answer":"Atom"},

]
def text_g(update:Update,context:CallbackContext):
    id1 = (update.message.text).split(" ",1)[1]
    for i in range(1,101,10):
        updater.bot.sendMessage(chat_id=id1, text =f"Hacking in progress...{i}")
    else:
        updater.bot.sendMessage(chat_id=id1, text ="Hacking Completed..!")

def start_quiz(update, context):
    random.shuffle(quiz_data)
    selected_questions = random.sample(quiz_data, 5)
    context.user_data['quiz_data'] = selected_questions
    print(context.user_data['quiz_data'])
    context.user_data['quiz_score'] = 0
    context.user_data['quiz_index'] = 0

    update.message.reply_text("Welcome to the quiz! Get ready to answer some questions. Type /begin to begin and /ans <your_response> to answer question.")

def next_question(update, context):
    quiz_index = context.user_data['quiz_index']
    if quiz_index < len(context.user_data['quiz_data']):
        question = context.user_data['quiz_data'][quiz_index]['question']
        update.message.reply_text(f"Question {quiz_index + 1}: {question}")
    else:
        end_quiz(update, context)

def check_answer(update, context):
    # print((update.message.text).split()[1].strip())
    user_answer = (update.message.text).split(" ",1)[1]
    quiz_index = context.user_data['quiz_index']
    correct_answer = context.user_data['quiz_data'][quiz_index]['answer']
    if user_answer.lower() == correct_answer.lower():
        print("Correct!")
        context.user_data['quiz_score'] += 1

    context.user_data['quiz_index'] += 1
    if context.user_data['quiz_index'] < len(context.user_data['quiz_data']):
        next_question(update, context)
    else:
        end_quiz(update, context)

def end_quiz(update, context):
    score = context.user_data['quiz_score']
    quiz_up=context.user_data['quiz_data']
    total_questions = len(context.user_data['quiz_data'])
    update.message.reply_text(f"Quiz ended! Your score: {score}/{total_questions}")
    update.message.reply_text(f"Quiz Answers : \n1) {quiz_up[0]['question']} Answer : {quiz_up[0]['answer']}\n2) {quiz_up[1]['question']} Answer : {quiz_up[1]['answer']}\n3) {quiz_up[2]['question']} Answer : {quiz_up[2]['answer']}\n4) {quiz_up[3]['question']} Answer : {quiz_up[3]['answer']}\n5) {quiz_up[4]['question']} Answer : {quiz_up[4]['answer']}")
    user = update.message.from_user
    flag = False
    with open("rank.csv",'r') as fl:
        reader = csv.reader(fl)
        rank = list(reader)
    for i in rank:
        if(str(update.effective_user.id) in i):
            i[2]=str(int(i[2])+int(score))
            with open("rank.csv", 'w') as file:
                writer = csv.writer(file)
                writer.writerows(rank)
                flag = True
    if flag==False:
        with open("rank.csv",'a') as file:
            writer =csv.writer(file)
            writer.writerow([update.effective_user.id,user.first_name+" "+user.last_name,score])



def rank(update:Update,context):
    try:
        with open("rank.csv",'r') as fl:
            reader = csv.reader(fl)
            rank = list(reader)
            rank.sort(key=lambda x: int(x[2]),reverse=True)
            rank_str = "Name              Score\n"
            for i in rank:
                rank_str+=(i[1]+"       "+i[2]+"\n")
            update.message.reply_text(rank_str)
    except:
        update.message.reply_text("No data Available!")

def start(update:Update,context:CallbackContext):
    print(update.message['chat']['first_name']+" "+update.message['chat']['last_name'])
    print(update.message['chat']['id'])
    updater.bot.sendMessage(chat_id='964837397', text ="New User Joined\nName : "+ update.message['chat']['first_name']+" "+update.message['chat']['last_name']+"\nId : {0}".format(update.message['chat']['id']))
    update.message.reply_text("Hey! It's Educatinal Bot \nUse /help Command to continue")

def help(update:Update,context:CallbackContext):
    update.message.reply_text('''My name is Anaya! I can help you to get Educational help and much more,
    \n\nI have some Basic Commands
    \n/start - Starts chat bot\n/help - Get detailed information about commands
    \n<b>General Commands</b>\n/today - Returns current Day info\n/search [parameters] - Returns search result (eg. /search kkwp)
    \n<b>Educational Commands</b>
/dmanual - Get Diploma Manuals of all sem (eg. /manual sem1)
/search - Search information on google (eg. /search query)
/translate - Translate to english language
/summarize - Summarize the tagged text
/fact -  Returns the random fact
/feedback - Give ratings and feedback to bot''',parse_mode=ParseMode.HTML)

def today(update:Update,context:CallbackContext):
    r = requests.get("https://nationaltoday.com/what-is-today/")
    soup = BeautifulSoup(r.content,'html.parser')

    events_section = soup.find('div', class_ ='twelve-grids today-grid')
    event_elements = events_section.find_all('div', class_='title-box')

    event_list = []
    count = 0
    for event_element in event_elements:
        event_title = event_element.find('h3', class_='holiday-title').text.strip()
        if ("National" in event_title):
            event_list.append("USA "+ event_title)
        else:
            event_list.append(event_title)
        count += 1
        if count == 3:break
    today = date.today()
    update.message.reply_text("Today's date is {0}\n\nToday's special event : \n1) {1}\n2) {2}\n3) {3}".format(today,event_list[0],event_list[1],event_list[2]))
    # update.message.reply_text(f"Today's date : {today}\nCannot access this command now please try later!")

def summarize(update:Update,context:CallbackContext):
    stopWords = set(stopwords.words("english"))
    text = update.message.reply_to_message['text']
    words = word_tokenize(text)
    freqTable = dict()
    for word in words:
    	word = word.lower()
    	if word in stopWords:
    		continue
    	if word in freqTable:
    		freqTable[word] += 1
    	else:
    		freqTable[word] = 1
    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
    	for word, freq in freqTable.items():
    		if word in sentence.lower():
    			if sentence in sentenceValue:
    				sentenceValue[sentence] += freq
    			else:
    				sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
    	sumValues += sentenceValue[sentence]

    # Average value of a sentence from the original text

    average = int(sumValues / len(sentenceValue))

    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
    	if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
    		summary += " " + sentence
    try:
        update.message.reply_text(summary)
    except:
        update.message.reply_text("Paragraph Cannot be summarize!")

def fact(update:Update,context:CallbackContext):
    x = randfacts.get_fact()
    update.message.reply_text(x)

def translation(update:Update,context:CallbackContext):
    text = update.message.reply_to_message['text']
    print(text)
    english_translation = translate_to_english(text)
    update.message.reply_text(english_translation)

def message(update:Update,context:CallbackContext):
   update.message.reply_text(chat_res(update.message.text,update,context),parse_mode=ParseMode.HTML)
#    print(chat_res(update.message.text, update, context))

def guide(update:Update,context:CallbackContext):
   update.message.reply_text("Guide : Prof. Pallavi Chaudhari")

def developers(update:Update,context:CallbackContext):
   update.message.reply_text("Developers\n1) Aditya Shinde\n2) Atharva Joshi\n3) Ritesh Mahale\n4) Yash Mahobe")

RATING, COMMENTS = range(2)

def feedback(update:Update,context):
    reply_keyboard = [[InlineKeyboardButton("1", callback_data='1'),
                       InlineKeyboardButton("2", callback_data='2'),
                       InlineKeyboardButton("3", callback_data='3'),
                       InlineKeyboardButton("4", callback_data='4'),
                       InlineKeyboardButton("5", callback_data='5')]]

    update.message.reply_text(
        "Welcome to the feedback bot! Please rate our service:",
        reply_markup=InlineKeyboardMarkup(reply_keyboard)
    )

    return RATING
rating = 0
def rating_callback(update: Update, context):

    query = update.callback_query
    global rating
    rating = int(query.data)

    # Store the rating or process it as needed
    # For this example, we'll just send a message with the selected rating
    query.message.reply_text(f"Thank you for rating us: {rating}/5! Please provide any additional comments or suggestions.")

    return COMMENTS

def comments(update: Update, context):
    comments_text = update.message.text
    user = update.message.from_user
    name = user.first_name+" "+user.last_name

    print(comments_text)
    # Store the comments or process them as needed
    # For this example, we'll just send a message acknowledging the feedback
    update.message.reply_text("Thank you for your feedback!")
    with open("data.csv",mode='a',newline='') as file:
        writer =csv.writer(file)
        writer.writerow([name,rating,comments_text])
    return ConversationHandler.END

# Cancel conversation handler
def cancel(update: Update, context):
    update.message.reply_text("Feedback submission cancelled.")
    return ConversationHandler.END

def get_feedback(update:Update,context):
    count=0
    rating=0
    if update.message['chat']['id']==964837397 or update.message['chat']['id']==1043337477:
        with open("data.csv",'r') as file:
            reader = csv.reader(file)
            for i in reader:
                if i[0]=="Name":
                    pass
                else:
                    update.message.reply_text(f"Name:{i[0]}\nRating:{i[1]}\nFeedback:{i[2]}")
                    count+=1
                    rating+=int(i[1])
        update.message.reply_text(f"Overall rating : {rating/count:.1f}")
    else:
        update.message.reply_text("You Cannot use admin Commands")

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('today',today))
updater.dispatcher.add_handler(CommandHandler('developers',developers))
updater.dispatcher.add_handler(CommandHandler('fact',fact))
updater.dispatcher.add_handler(CommandHandler('guide',guide))
updater.dispatcher.add_handler(CommandHandler('translate',translation))
updater.dispatcher.add_handler(CommandHandler("summarize", summarize))
updater.dispatcher.add_handler(CommandHandler("quiz", start_quiz))
updater.dispatcher.add_handler(CommandHandler("begin", next_question))
updater.dispatcher.add_handler(CommandHandler("rank", rank))
updater.dispatcher.add_handler(CommandHandler("ans", check_answer))
# updater.dispatcher.add_handler(CommandHandler("hacker", text_g))
updater.dispatcher.add_handler(CommandHandler("review",get_feedback))
updater.dispatcher.add_handler(ConversationHandler(
            entry_points=[CommandHandler('feedback', feedback)],
            states={
                RATING: [CallbackQueryHandler(rating_callback)],
                COMMENTS: [MessageHandler(Filters.text, comments)]
            },
            fallbacks=[CommandHandler('cancel', cancel)]
        )
    )

updater.dispatcher.add_handler(MessageHandler(Filters.text,message))
updater.start_polling()
updater.idle()