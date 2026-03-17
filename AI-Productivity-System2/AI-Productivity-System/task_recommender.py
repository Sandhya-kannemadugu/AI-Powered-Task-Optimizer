def recommend_task(emotion):

    tasks = {

        "happy": "Great mood! Work on creative tasks.",

        "neutral": "Good time for focused coding.",

        "sad": "Take a short break.",

        "angry": "Pause work and relax.",

        "surprise": "Review your tasks calmly."
    }

    return tasks.get(emotion.lower(),
                     "Continue working normally.")