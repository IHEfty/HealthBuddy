import os
import random
import spacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

nlp = spacy.load("en_core_web_sm")

symptom_responses = {
    "fever": [
        "It looks like you might have a fever. Make sure you're staying hydrated and getting plenty of rest. Keep an eye on your temperature, and if it goes over 102°F or if your symptoms stick around, it’s a good idea to consult a healthcare provider. Would you like more tips on managing a fever?",
        "A fever can be your body’s way of fighting something off. Try to stay cool and drink lots of fluids. If it doesn’t go down, it might be wise to seek medical attention. Want advice on how to reduce your fever?"
    ],
    "headache": [
        "Headaches can come from many things like stress, dehydration, or not getting enough sleep. Try taking a break, drinking some water, and reducing your screen time. If the headaches continue or get severe, it might be time to consult a healthcare provider. Would you like some tips for relief?",
        "If you have a headache, it’s worth checking if you’re drinking enough water. Sometimes a cold compress can help ease the pain. Have you noticed any particular triggers?"
    ],
    "cough": [
        "Coughing can be caused by allergies, a cold, or other irritants. Staying hydrated, resting, and avoiding smoke can be beneficial. If your cough lingers for more than a week or if you're having trouble breathing, consider seeing a healthcare provider. Are you experiencing any other symptoms?",
        "Coughing can be really annoying. Honey and warm liquids might soothe your throat. If this has lasted more than a week, please reach out to a healthcare professional. How long have you been dealing with this cough?"
    ],
    "fatigue": [
        "Feeling fatigued can be linked to lack of sleep, stress, or diet. Ensure you’re getting enough rest, drinking water, and eating well. If this continues, it may be a good idea to consult a healthcare provider. Would you like to talk about ways to manage fatigue?",
        "Constant tiredness can be frustrating. Consider looking into your sleep schedule and stress levels. Are there specific activities that seem to drain your energy?"
    ],
    "difficulty breathing": [
        "Trouble breathing can be serious. If this is a persistent or worsening issue, please seek medical attention right away. For immediate concerns, heading to the ER or contacting a healthcare provider is advisable.",
        "If you're struggling to breathe, it’s crucial to stay calm and seek medical help immediately. Can you tell me more about when this started or what might have triggered it?"
    ],
    "sore throat": [
        "A sore throat is often caused by infections or allergies. Gargling warm salt water and sipping warm fluids can help ease the discomfort. If it sticks around for more than a few days, consider seeing a doctor. Would you like some tips on soothing a sore throat?"
    ],
    "nausea": [
        "Nausea can be quite uncomfortable and can stem from various factors. Ginger tea or peppermint might help settle your stomach. If you’re experiencing vomiting or it lasts more than a day, it’s a good idea to see a healthcare provider. Have you noticed anything specific that triggers your nausea?"
    ],
    "stomach ache": [
        "Stomach aches can arise from several causes, like indigestion or stress. Try resting and avoiding heavy meals for a while. If the pain is severe or lingers for more than a couple of days, please reach out to a healthcare provider. Did anything specific upset your stomach?"
    ],
    "allergies": [
        "If you’re dealing with allergy symptoms, consider taking an antihistamine and steering clear of known allergens. If things worsen or you notice swelling or trouble breathing, please consult a doctor. Do you have any specific allergens in mind?"
    ],
    "dizziness": [
        "Dizziness can be due to dehydration, low blood sugar, or sudden changes in position. Make sure you’re drinking enough water and eating balanced meals. If this continues or you feel faint, please seek medical attention. When do you usually feel dizzy?"
    ],
    "muscle pain": [
        "Muscle pain can happen from overexertion or tension. Rest, gentle stretching, and warm baths might help. If the pain persists or is linked to other symptoms, consider seeing a healthcare provider. Where are you feeling the muscle pain?"
    ],
    "chills": [
        "Chills can often accompany a fever or indicate an infection. Try to stay warm and keep an eye on your temperature. If the chills persist or if you experience other concerning symptoms, it's wise to seek medical help. Are you feeling feverish as well?"
    ],
    "rash": [
        "A rash can be a response to allergies, irritants, or infections. Try to avoid scratching it and consider applying a cool compress. If it spreads or comes with other symptoms, please consult a healthcare provider. Have you noticed any specific triggers for your rash?"
    ],
    "joint pain": [
        "Joint pain can come from various issues, including arthritis or injury. Resting the affected joint and applying ice might help alleviate the discomfort. If it doesn’t go away, it’s a good idea to consult a healthcare professional. Which joint is bothering you?"
    ],
    "vomiting": [
        "Vomiting can have many causes, like a stomach virus or food poisoning. Staying hydrated is really important. If it continues or if you can’t keep fluids down, seek medical help right away. Have you eaten anything unusual recently?"
    ],
    "sweating": [
        "Excessive sweating can result from anxiety, heat, or other medical issues. Try to keep cool and wear breathable clothing. If this continues or if you notice other symptoms, consider consulting a healthcare provider. Have you experienced any specific triggers for your sweating?"
    ],
    "insomnia": [
        "Struggling to fall asleep or stay asleep can be really tough. Establishing a bedtime routine and cutting down on screen time before bed might help. If this keeps happening, talking to a healthcare provider could be beneficial. What worries keep you awake at night?"
    ],
    "heartburn": [
        "Heartburn might be linked to certain foods or acid reflux. Avoiding spicy or fatty foods and not lying down right after eating can help. If this happens often, please consult a healthcare provider. What foods have you noticed trigger this?"
    ],
    "dehydration": [
        "Dehydration can lead to various health issues. Ensure you’re drinking enough fluids, especially if you’re active or it's hot outside. If you’re feeling very thirsty or lightheaded, seeking medical help is important. Are you experiencing any severe symptoms?"
    ],
    "urinary problems": [
        "Frequent urination or pain while urinating could indicate a urinary tract infection. It’s best to consult a healthcare provider for an evaluation. Have you noticed any changes in your urine?"
    ],
    "weight loss": [
        "Unexplained weight loss can be concerning and should be discussed with a healthcare provider. It could be linked to stress, diet, or other health conditions. How long have you noticed this change?"
    ],
    "mood changes": [
        "Mood changes can stem from many factors, including stress, diet, or hormonal fluctuations. Talking to someone about how you feel can be really helpful. Would you like resources for managing stress or mood?"
    ],
    "memory issues": [
        "Memory issues can be caused by stress, lack of sleep, or other factors. Keeping your mind active with puzzles and staying engaged can help. If this is a constant issue, please consult a healthcare provider. How long have you been experiencing these memory problems?"
    ],
    "cold symptoms": [
        "Common cold symptoms include sneezing, a runny nose, and a sore throat. Rest, hydration, and over-the-counter medications can be useful. If symptoms get worse, consider talking to a healthcare provider. Are you noticing any other symptoms along with these?"
    ],
    "skin issues": [
        "Skin problems like dryness or acne can come from many sources, including the weather and diet. Using a good moisturizer and keeping a solid skincare routine can help. What specific skin issues are you dealing with?"
    ],
    "eye strain": [
        "Eye strain can occur after long hours in front of screens. Try taking breaks and adjusting your screen brightness. If the discomfort persists, it might be a good idea to consult an eye specialist. How often do you use screens throughout the day?"
    ],
    "earache": [
        "Earaches can be caused by infections or sinus issues. Applying a warm compress may help provide some relief. If the pain is severe or lasts more than a few days, please consult a healthcare provider. Have you had any recent sinus problems?"
    ],
    "sinus congestion": [
        "Sinus congestion can make it hard to breathe. Over-the-counter decongestants and staying hydrated might help ease symptoms. If it continues or is severe, consider consulting a healthcare provider. How long have you been experiencing this?"
    ],
    "mood swings": [
        "Mood swings can be influenced by stress, hormonal changes, or lifestyle factors. Keeping a journal might help you pinpoint your triggers. Would you like suggestions for managing stress?"
    ],
    "anxiety": [
        "Anxiety can show up in many ways, including restlessness and racing thoughts. Mindfulness exercises and breathing techniques can help ease those feelings. If this continues, it might be helpful to reach out to a mental health professional. What situations tend to trigger your anxiety?"
    ],
    "depression": [
        "Dealing with depression can be tough. It’s really important to seek support from friends, family, or a mental health professional. Are there specific thoughts or feelings you’d like to talk about?"
    ],
    "stress": [
        "Stress can impact your physical and mental well-being. Finding healthy outlets like exercise or hobbies can help relieve stress. If it feels overwhelming, consider reaching out to a mental health professional. What’s been stressing you out lately?"
    ],
    "fatigue": [
        "Chronic fatigue can stem from various factors like stress, sleep issues, or medical conditions. Taking time to rest and evaluate your lifestyle can be beneficial. If it persists, consulting a healthcare provider is wise. How long have you been feeling this way?"
    ],
}

def get_symptom_response(symptom):
    responses = symptom_responses.get(symptom)
    if responses:
        return random.choice(responses)
    return "I'm not sure how to help with that. Can you provide more details?"


greeting_responses = [
    "Hello! How can I assist you today?",
    "Hi there! What health concerns can I help you with?",
    "Greetings! Feel free to share any symptoms you're experiencing.",
    "Hey! I'm here to assist you. How can I help today?"
]

follow_up_phrases = [
    "Let me know if you need more information.",
    "I'm here to help if you have any other questions.",
    "Would you like more details on this topic?",
    "Feel free to ask if you'd like further assistance."
]

def with_greeting(response):
    greeting = random.choice(greeting_responses)
    return f"{greeting} {response}"

def get_closest_symptom(user_input):
    best_match, score = process.extractOne(user_input, symptom_responses.keys(), scorer=fuzz.partial_ratio)
    return best_match if score >= 70 else None  

def extract_name(user_input):
    match = re.search(r"(?:i'm|i am|my name is|im) (\w+)", user_input, re.IGNORECASE)
    return match.group(1) if match else None

def generate_response(user_input):
    name = extract_name(user_input)
    if name:
        return f"Nice to meet you, {name}! How can I assist with any health-related concerns today?"

    found_symptom = get_closest_symptom(user_input)

    if any(keyword in user_input for keyword in ["dev", "developer", "creator", "created you"]):
        return ("This project was developed by IH Efty.\n"
                "Username > @IHEfty\n"
                "GitHub > https://github.com/IHEfty/\n"
                "I'm proud to be part of their project! Let me know how I can assist further.")

    if found_symptom:
        return random.choice(symptom_responses[found_symptom])
        
    elif any(greeting in user_input for greeting in ["hello", "hi", "hey"]):
        return with_greeting("")
        
    elif any(exit_word in user_input for exit_word in ["bye", "exit", "quit", "goodbye"]):
        return "Goodbye! Remember to prioritize your health, and feel free to reach out for more guidance."
    
    else:
        return with_greeting(
            "I'm here to provide guidance on health-related topics. Could you specify any symptoms you're experiencing? "
            "Describing how you feel might help me assist you more effectively."
        )

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear') 
    print("\033[92mWelcome to HealthBuddy, your virtual healthcare assistant.\033[0m")
    print("You can describe your symptoms, and I will offer general guidance based on your input.")
    print("Type 'quit' at any time to exit the chat or 'clr' to clear the chat and start over.")

def healthbuddy():
    clear_console()  

    try:
        while True:
            user_input = input("\033[92mYou: \033[0m").lower()
            
            if user_input in ['clr', 'clear']:
                clear_console()  
                continue
            elif user_input in ['exit', 'quit', 'goodbye']:
                print("\033[92mBot: Goodbye! Stay healthy and take care.\033[0m")
                break
            
            response = generate_response(user_input)
            print("\033[92mBot:\033[0m", response)

    except KeyboardInterrupt:
        print("\n\033[92mBot: Goodbye! Stay healthy and take care.\033[0m")

if __name__ == "__main__":
    healthbuddy()