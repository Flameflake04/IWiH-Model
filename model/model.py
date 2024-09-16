import textract
import re
import spacy
from nameparser import HumanName
import requests
from genderize import Genderize
from GenderSpecificDisease import GenderDisease
from classification import GenderClassifier
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# Regex is just like magic...
# It is so cool...
class PaperAnalysis:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_text = self.extract_text_from_pdf_with_ocr(pdf_path)
        self.male_pronouns = 0
        self.female_pronouns = 0
        self.case_study = 0
        self.author_names = []
        self.male_count = 0
        self.female_count = 0
        self.male_participant_ratio = 0.5
        self.male_author_ratio = 0.5
        self.male_pronouns_ratio = 0.5
        self.male_participants_count = 0
        self.female_participants_count = 0
        self.disease_male_or_female_only = "neutral"
        self.model_result = 0
        self.genderSpecficDisease = GenderDisease(self.pdf_path)
        self.genderBiasedClassifier = GenderClassifier()
    # Process pdf into text
    def extract_text_from_pdf_with_ocr(self, pdf_path):
        try:
            text = textract.process(pdf_path)
            return text.decode('utf-8')
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""

    
    def count_gendered_pronouns(self):
        self.male_pronouns = len(re.findall(r'\b(he|him|his|male|males|men|man)\b', self.pdf_text, re.IGNORECASE))
        self.female_pronouns = len(re.findall(r'\b(she|her|hers|females|female|woman|women)\b', self.pdf_text, re.IGNORECASE))
        print(f"Male Pronouns: {self.male_pronouns}, Female Pronouns: {self.female_pronouns}")

    def extract_names_with_spacy(self, text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        cleaned_names = self.clean_author_name(names)
        unique_names = list(set(cleaned_names))
        return unique_names

    # Handle the participant number
    # I am really scared of this function at first, because some research has like men (n = 234), female (n = 235) 
    # And some research has like 9999 males, 10000 females
    # So I just think about solving BOTH case 
    # I try to find both pronouns in the SAME sentence, and that sentence should have the same characteristic describe before
    def count_participants(self):
    # Updated pattern to match the format in the provided text
        pattern = (r'(\d{1,3}(?:,\d{3})*)\s*(?:women|female|females?)\s*and\s*(\d{1,3}(?:,\d{3})*)\s*(?:men|male|males?)' r'|'
                  r'(\d{1,3}(?:,\d{3})*)\s*\(\s*n\s*=\s*(\d{1,3}(?:,\d{3})*)\s*\)\s*(?:men|male|males?)\s*,\s*'
        r'(\d{1,3}(?:,\d{3})*)\s*\(\s*n\s*=\s*(\d{1,3}(?:,\d{3})*)\s*\)\s*(?:female|females?)'
    )
        match = re.search(pattern, self.pdf_text, re.IGNORECASE | re.DOTALL)

        if match:
            if match.group(1) and match.group(2):
                self.female_participants_count = int(match.group(1).replace(',', ''))
                self.male_participants_count = int(match.group(2).replace(',', ''))
            elif match.group(3) and match.group(4) and match.group(5) and match.group(6):  # "men (n = X), female (n = Y)" format
                self.male_participants_count = int(match.group(4).replace(',', ''))
                self.female_participants_count = int(match.group(6).replace(',', ''))
            print(f"Male Participants: {self.male_participants_count}, Female Participants: {self.female_participants_count}")
        else:
            print("No matching male and female participants found.")

    # Clean the author name
    # 3 conditions: No number in names, no et al in names, need to have both lowercase and uppercase
    def clean_author_name(self, string_list):
        return [s for s in string_list if not re.search(r'\d', s) 
            and 'et al' not in s.lower() 
            and re.search(r'[A-Z]', s)  
            and re.search(r'[a-z]', s)]  
    
    # See the referneces part and extract author name using spacy
    # Spacy kinda bad... so I still need to clean it the second times using clean_author_name
    def extract_author_from_references(self):
        match = re.search(r'\b(?:References|Literature Cited)\b', self.pdf_text, re.IGNORECASE)
        if match:
            references_text = self.pdf_text[match.end():].strip()
            self.author_names = self.extract_names_with_spacy(references_text)
            print(f"Author Names: {self.author_names}")
            return self.author_names
        else:
            print("No references section found.")
            return []
 
    # Really important: Check the paper has case study or not
    # If the paper has case study, high chance it is being biased
    def check_if_case_study(self):
        if re.search(r'\bcase study\b', self.pdf_text, re.IGNORECASE):
            self.case_study = 1
            print("The paper is a case study")
        else:
            self.case_study = 0
            print("The paper is not case study")

    # I use genderize API to determine the name of the author, male or female
    # I think there is better way to do this, using national reseacher name for example
    def genderize_author(self):
        api_key_genderize = 'ff6bfb2eabac483948e08d20c52a9436'
        genderize = Genderize(api_key=api_key_genderize)
        self.author_gender = genderize.get(self.author_names)
        for entry in self.author_gender:
            if entry['gender'] == 'male':
                self.male_count += 1
            elif entry['gender'] == 'female':
                self.female_count += 1

    def data_combination(self):
        
        self.count_gendered_pronouns()
        self.extract_author_from_references()
        self.check_if_case_study()
        self.genderize_author()
        self.count_participants()
        if (self.male_pronouns + self.female_pronouns > 3):
            self.male_pronouns_ratio = round((self.male_pronouns / (self.male_pronouns + self.female_pronouns)),2)
        if (self.male_count + self.female_count > 0):
            self.male_author_ratio = round((self.male_count / (self.male_count + self.female_count)),2)
        total_participants = self.male_participants_count + self.female_participants_count
        if total_participants > 0:
            self.male_participant_ratio = round((self.male_participants_count / total_participants), 2)
        self.disease_male_or_female_only = self.genderSpecficDisease.open_AI_classification()
        print(self.genderSpecficDisease)
        self.genderBiasedClassifier.train("train.csv")
        self.model_result = self.genderBiasedClassifier.predict(np.array([self.male_participant_ratio, self.male_author_ratio, self.male_pronouns_ratio]))[0][0]
        self.disease_male_or_female_only = self.disease_male_or_female_only.strip("'").lower()
        if (self.disease_male_or_female_only == "female"):
            self.male_participant_ratio = 0
            self.male_participants_count = 0
            self.female_participants_count = 255
            print("This study conducted a research in female-related diseases")
        elif (self.disease_male_or_female_only == "male"):
            self.model_result = 0
            self.male_participant_ratio = 1
            self.female_participants_count = 0
            self.male_participant_count = 361
            print("This study conducted a resaerch in male-related diseases")
        else:
            print("The diesase affected both genders")
        print(self.male_participant_ratio)
        print(self.male_author_ratio)
        print(self.male_pronouns_ratio)
        
        print(f"Male Participants: {self.male_participants_count}, Female Participants: {self.female_participants_count}")
        print(f"Male Participant Ratio: {self.male_participant_ratio}")
        print(f"Model result: {self.model_result} (0 for not biased toward male, 1 for biased toward male)")
        return [self.male_participants_count, self.female_participants_count, self.male_count, self.female_count, self.male_pronouns, self.female_pronouns, 
                self.male_participant_ratio, self.male_author_ratio, self.male_pronouns_ratio, self.case_study, self.model_result, self.disease_male_or_female_only]

    
if __name__ == "__main__":
    analyzer = PaperAnalysis("HotFlashes.pdf")
    analyzer.data_combination()    