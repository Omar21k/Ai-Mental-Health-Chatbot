from flask import Flask, jsonify
import sqlite3
import random
import schedule
import time
import sqlite3
from datetime import datetime

QUOTES = {
    "Deep Sadness": [
         "The pain you feel today is the strength you feel tomorrow. "
        ,"Tears come from the heart and not from the brain.",
        "“Cheer up, my dear. After every storm comes the sun. Happiness is waiting for you ahead.”",
        "“What doesn\'t kill you makes you stronger.”",
        "“Life is a mixture of sunshine and rain, teardrops and laughter, pleasure and pain. Just remember, there was never a cloud that the sun couldn\'t shine through.”",
        "“Good people are good because they\'ve come to wisdom through failure.”",
        "“Life is too short for us to dwell on sadness. Cheer up and live life to the fullest.”",
        "Sometimes you have to fight through your worst days in order to earn the best days of your life.",
        "If you\'re going through a hard time right now, make sure you do something today that makes you smile.",
        "Sadness is but a wall between two gardens.",
        "Life\'s under no obligation to give us what we expect.",
        "“We cannot solve problems with the kind of thinking we employed when we came up with them.”"
        "“What brings us to tears, will lead us to grace. Our pain is never wasted.” ",
        "“Every life has a measure of sorrow, and sometimes this is what awakens us.”",
        "“People cry, not because they are weak. It is because they've been strong for too long.” ",
        "“Your greatest highs come from overcoming your greatest lows.” ",
        "“First, accept sadness. Realize that without losing, winning isn\'t so great.” ",
        "“When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.”",
        "“You cannot always control what goes on outside. But you can always control what goes on inside.”",
        "“Nothing ever goes away until it teaches us what we need to know.” ",
        "“If there is no struggle, there is no progress.”",
        "“Courage is like a muscle. We strengthen it by use.”",
        "“If you don\'t like the road you\'re walking, start paving another one.”",
        "Life has got all those twists and turns. You've got to hold on tight and off you go.",
    ],
    "Fear": [
        "You don’t have to control your thoughts. You just have to stop letting them control you.",
        "Do not anticipate trouble or worry about what may never happen.",
        # More anxiety quotes...
    ],
    "depression": [
        "It\'s OK to not feel OK",
        "You\'re not alone",
        "You can move forward in the face of your depression",
        "Your story isn\'t over",
        "“If you are still breathing maybe it is not such a bad day after all.”",
        "“You alone are enough. You have nothing to prove to anybody.”",
        "It is never too late to be what you might have been.",
        "Don\'t close the book when bad things happen in your life! Just turn the page and start a new chapter!",
        "Please remember that you\'re capable, brave and loved even when it feels like you\'re not."
        "Do not give the past the power to define your future.",
        "Even the darkest hour only has 60 minutes.",
        "Don\'t hate yourself for everything you aren\'t. Instead, love yourself for everything you are."
        "Running away from your problems is a race you\'ll never win. Instead, reach out for help and try to confront them.",
        "Don\'t let your struggle become your identity. After all, you are so much more than just your illness."
        "Be proud of who you are, instead of ashamed of how someone else sees you.",
        "Crying doesn\'t mean that you\'re weak. Since birth, it\'s always been a sign that you\'re alive.",
        "Don\'t dwell on those who hold you down. Instead, cherish those who helped you up.",
        "Even if you can\'t see any reason to keep on going, then it doesn\'t mean that there aren\'t any. It just means that in that moment, your depression is telling you even more lies than usual.",
        "Even the worst depressive episodes won\'t last forever.",
        "If you need a confidence booster, then remind yourself of all the difficult things you\'ve endured and overcome."
        "When your depression says, 'Give up', hope whispers, 'Try one more time'.",
        "One day, if not already, your refusal to give up will inspire someone else.",
        "Please remember that having a bad day does not mean you have or will have a bad life.",
        "Hope is one of the most powerful emotions a person can have. Combine it with determination and there\'s no stopping you.",
        "Never put the key to your happiness in someone else\'s pocket.",
        "Just because you have a mental illness, it doesn't mean that you are that illness. You're still a person just like everybody else.",
        "Sometimes, you just need to cry your eyes out to be able to keep going. And you know what? That's OK.",
        "Healing is a process, not an event. Give it time. Good things happen to those who never give up.",
        "When something goes wrong, take a moment to be thankful for all the things in your life that are going right.",
        "Never forget that you are worthy of love and respect.",
        "“Don\'t let yesterday take up too much of today.”",
        "“Experience is a hard teacher because she gives the test first, the lesson afterwards.”",
        "“When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.”",
        "Life has got all those twists and turns. You've got to hold on tight and off you go.",
    ],
    "Frustration": [
         "“If you really love something set it free. If it comes back it\'s yours, if not it wasn\'t meant to be.”",
        "“People will always throw stones in your path. What will happen depends on what you make out of it a wall or a bridge! So cheer up and move on.”",
        "Never give up. Today is hard, tomorrow will be worse, but the day after tomorrow will be sunshine.",
        "Life is like riding a bicycle. To keep your balance, you must keep moving.",
        "Fall seven times, stand up eight.",
        "Tough times never last, but tough people do.",
        "Some people go through hard times, so bad that they can\'t even talk about it, but no matter what, we should never give up.",
        "Let them ridicule you, laugh at you, hurt you & ignore you but never let them stop you.",
        "It does not matter how slowly you go as long as you do not stop.",
        "I never lose. I either win or learn.",
        "Our greatest glory is not in never falling but in rising every time we fall.",
        "You\'re allowed to scream, you\'re allowed to cry, but do not give up.",
        "It always seems impossible until it\'s done.",
        "You never fall until you stop trying."
        "Don't go around saying the world owes you a living. The world owes you nothing. It was here first.",
        "“Stay away from those people who try to disparage your ambitions. Small minds will always do that, but great minds will give you a feeling that you can become great too.” ",
        "It is better to fail in originality than to succeed in imitation.",
        "“You learn more from failure than from success. Don\'t let it stop you. Failure builds character.”",
        "“Setting goals is the first step in turning the invisible into the visible.” ",
        "“The elevator to success is out of order. You\'ll have to use the stairs, one step at a time.”",
        "“When everything seems to be going against you, remember that the airplane takes off against the wind, not with it.”",
        "Nothing is impossible. The word itself says Im possible!",
    ],
    "sadness_anxiety": [
        "It’s okay to not be okay all the time. You’re doing the best you can, and that’s enough.",
        "Remember, you’re not alone in this. Breathe, and take one step at a time.",
        # More combination quotes...
    ],
    "General sadness": [
        "Keep pushing forward. The best is yet to come.",
        "Believe in yourself and all that you are.",
        "Your potential is limitless. Don't give up.",
        "Life is 10% what happens to you and 90% how you react to it.",
        "Change your thoughts, and you change your world.",
        "All our dreams can come true if we have the courage to pursue them",
        "Success is a journey not a destination.",
        "What you get by achieving your goals is not as important as what you become by achieving your goals",
        "It always seems impossible until it's done",
        "Success is liking yourself, liking what you do, and liking how you do it",
        "If you cannot do great things, do small things in a great way.",
        "Success only comes to those who dare to attempt",
        "If opportunity doesn't knock, build a door",
        "Joy does not simply happen to us. We have to choose joy and keep choosing it every day.",
        "Be happy for this moment. This moment in your life.",
        "If you carry joy in your heart, you can heal any moment",
        "If you can dream it, you can do it.",
        "To live is the rarest thing in the world. Most people just exist",
        "Life is difficult because… we don\'t appreciate the things that come easily.",
        "Life teaches you a new lesson every day, if you are attentive enough in the class of life.",
        "Don\'t wait. The time will never be just right."
        "You can, you should, and if you\'re brave enough to start, you will.",
        "He who does not understand your silence will probably not understand your words.",
        "Happiness often sneaks in through a door you didn\'t know you left open.",
        "If you have to introduce yourself then understand that success is still far away.",
        "The only place where your dream becomes impossible is in your own thinking",
        "Belief and hope don\'t make goals easy… but make them possible.",
        "Happening Good things may not make you positive. You have to be positive. And, when you\'re positive, good things are bound to happen.",
        "If you look at what you have in life, you\'ll always have more.",
        "Every saint has a past, and every sinner has a future.",
        "Life is not a problem to be solved, but a reality to be experienced.",
        "It does not matter how slowly you go, so long as you do not stop.",
        "If you continue to think the way you\'ve always thought, you\'ll continue to get what you\'ve always got.",

    ]
}
def select_quote(user_input):
    emotion = classify_emotion(user_input)
    return random.choice(QUOTES[emotion])
  


def send_notifications():
    conn = sqlite3.connect('healthquote.db')
    cursor = conn.cursor()

    # Fetch pending notifications
    cursor.execute("SELECT id, user_id, quote FROM notifications WHERE status='pending' AND scheduled_time <= ?", 
                   (datetime.now(),))
    
    for notif_id, user_id, quote in cursor.fetchall():
        # Here you would integrate your messaging system (e.g., email, SMS, or push notifications)
        print(f"Sending to User {user_id}: {quote}")
        
        # Update notification status
        cursor.execute("UPDATE notifications SET status='sent' WHERE id=?", (notif_id,))
    
    conn.commit()
    conn.close()

# Schedule the function to run every hour
schedule.every().day.at("09:00").do(send_notifications)
schedule.every().day.at("15:00").do(send_notifications)
schedule.every().day.at("21:00").do(send_notifications)

while True:
    schedule.run_pending()
    time.sleep(1)
