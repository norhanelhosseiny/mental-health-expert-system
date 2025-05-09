from experta import *

class MentalHealthAssessment(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnoses = []

    @DefFacts()
    def _initial_action(self):
        yield Fact(action="start_assessment")

    def is_often_or_more(value):
        return value in ["often", "always"]

    def is_sometimes_or_more(value):
        return value in ["sometimes", "often", "always"]

    def is_rarely_or_never(value):
        return value in ["rarely", "never"]

    # Insomnia
    @Rule(Fact(sleep_hours=MATCH.hours),
          Fact(sleep_difficulty=MATCH.diff),
          Fact(wake_rest=MATCH.rest),
          TEST(lambda hours: int(hours) < 5),
          TEST(lambda diff: diff in ["often", "always"]),
          TEST(lambda rest: rest in ["never", "rarely"]))
    def diagnose_insomnia(self):
        self.diagnoses.append("You may be experiencing symptoms of **insomnia**. Consider improving your sleep hygiene or speaking to a professional.")

    # Depression
    @Rule(Fact(interest_loss=MATCH.interest),
          Fact(persistent_sadness=MATCH.sad),
          Fact(eating_changes=MATCH.eating),
          TEST(lambda interest: interest in ["often", "always"]),
          TEST(lambda sad: sad in ["often", "always"]),
          TEST(lambda eating: eating in ["sometimes", "often", "always"]))
    def diagnose_depression(self):
        self.diagnoses.append("You show signs of **depression**. Please consider speaking to a mental health professional.")

    # Anxiety
    @Rule(Fact(anxiety_freq=MATCH.freq),
          Fact(anxiety_physical=MATCH.phys),
          Fact(anxiety_avoidance=MATCH.avoid),
          TEST(lambda freq: freq in ["often", "always"]),
          TEST(lambda phys: phys in ["often", "always"]),
          TEST(lambda avoid: avoid in ["often", "always"]))
    def diagnose_anxiety(self):
        self.diagnoses.append("You may be experiencing **generalized anxiety disorder**. Coping strategies or therapy might help.")

    # Panic Disorder
    @Rule(Fact(anxiety_freq="always"),
          Fact(anxiety_physical="always"),
          Fact(stress_freq="always"),
          Fact(stress_management=MATCH.manage),
          TEST(lambda manage: manage in ["never", "rarely"]))
    def diagnose_panic_disorder(self):
        self.diagnoses.append("Symptoms suggest **panic disorder**. If you experience sudden, intense anxiety, seek support from a therapist.")

    # Seasonal Affective Disorder
    @Rule(Fact(persistent_sadness=MATCH.sad),
          Fact(interest_loss=MATCH.loss),
          Fact(lifestyle='sedentary'),
          Fact(wake_rest=MATCH.rest),
          TEST(lambda sad: sad in ["often", "always"]),
          TEST(lambda loss: loss in ["often", "always"]),
          TEST(lambda rest: rest in ["never", "rarely"]))
    def diagnose_sad(self):
        self.diagnoses.append("You may be showing signs of **Seasonal Affective Disorder (SAD)**. Light exposure, physical activity, and support can help.")

    # ADHD
    @Rule(Fact(focus_issues=MATCH.focus),
          Fact(forgetfulness=MATCH.forget),
          Fact(mental_fatigue=MATCH.fatigue),
          Fact(mood_swings=MATCH.mood),
          TEST(lambda focus: focus in ["often", "always"]),
          TEST(lambda forget: forget in ["often", "always"]),
          TEST(lambda fatigue: fatigue in ["often", "always"]),
          TEST(lambda mood: mood in ["often", "always"]))
    def diagnose_adhd(self):
        self.diagnoses.append("Your responses are consistent with **ADHD symptoms**. Consider a clinical evaluation if attention problems persist.")

    # Burnout
    @Rule(Fact(occupation='working'),
          Fact(stress_freq=MATCH.stress),
          Fact(mental_fatigue=MATCH.fatigue),
          Fact(irritability=MATCH.irritate),
          Fact(sleep_hours=MATCH.hours),
          TEST(lambda stress: stress in ["often", "always"]),
          TEST(lambda fatigue: fatigue in ["often", "always"]),
          TEST(lambda irritate: irritate in ["often", "always"]),
          TEST(lambda hours: int(hours) < 6))
    def diagnose_burnout(self):
        self.diagnoses.append("You may be experiencing **burnout**. It's important to rest, set boundaries, and talk to someone.")

    # Bipolar Disorder
    @Rule(Fact(mood_swings=MATCH.mood),
          Fact(emotional_numbness=MATCH.numb),
          Fact(irritability=MATCH.irritate),
          Fact(persistent_sadness=MATCH.sad),
          TEST(lambda mood: mood in ["often", "always"]),
          TEST(lambda numb: numb in ["often", "always"]),
          TEST(lambda irritate: irritate in ["often", "always"]),
          TEST(lambda sad: sad in ["often", "always"]))
    def diagnose_bipolar(self):
        self.diagnoses.append("Your answers suggest **bipolar symptoms**. Please consider speaking to a qualified mental health professional.")

    # Suicide Risk
    @Rule(Fact(suicidal_thoughts=MATCH.thoughts),
          Fact(suicide_intent=MATCH.intent),
          TEST(lambda thoughts: thoughts in ["often", "always"]),
          TEST(lambda intent: intent in ["sometimes", "often", "always"]))
    def diagnose_crisis(self):
        self.diagnoses.append("You mentioned suicidal thoughts with a plan. Please **seek immediate help** or call a suicide prevention hotline.")

    # Resilience
    @Rule(Fact(stress_management=MATCH.manage),
          Fact(wake_rest=MATCH.rest),
          Fact(persistent_sadness=MATCH.sad),
          Fact(focus_issues=MATCH.focus),
          Fact(mental_fatigue=MATCH.fatigue),
          TEST(lambda manage: manage in ["often", "always"]),
          TEST(lambda rest: rest in ["often", "always"]),
          TEST(lambda sad: sad in ["never", "rarely"]),
          TEST(lambda focus: focus in ["never", "rarely"]),
          TEST(lambda fatigue: fatigue in ["never", "rarely"]))
    def diagnose_resilience(self):
        self.diagnoses.append("You seem to have strong mental resilience and self-care habits. Keep it up and keep checking in with yourself!")


    @Rule(Fact(action='start_assessment'))
    def final_advice(self):
        if not self.diagnoses:
            self.diagnoses.append("No major red flags detected, but maintaining mental wellness is important. Consider regular self-check-ins.")


