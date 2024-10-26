# HealthBuddy

HealthBuddy is a virtual healthcare assistant that provides general guidance based on the symptoms described by users. It utilizes natural language processing to identify symptoms and deliver relevant health advice.

## Preview

![Preview](./preview.gif)

---

## Features

- **Symptom Recognition**: The bot identifies various health symptoms from user input and offers tailored responses.
- **General Health Tips**: Users receive general health advice based on their symptoms.
- **Friendly Interface**: Engaging greetings and follow-up questions to enhance user interaction.
- **Developer Information**: Provides information about the project creator upon request.

## Technologies Used

- **Python**: The main programming language used for the application.
- **Spacy**: Natural language processing library for understanding user input.
- **FuzzyWuzzy**: For approximate string matching to identify symptoms.
- **Random**: To select random responses for a varied interaction.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IHEfty/HealthBuddy.git
   ```
2. Navigate to the project directory:
   ```bash
   cd HealthBuddy
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python healthbuddy.py
   ```
2. Interact with HealthBuddy by typing your symptoms or questions into the console.
3. You can type 'quit' to exit the application at any time.

## Example Interaction

```
User: Hello, I have a headache.
HealthBuddy: If you have a headache, it’s worth checking if you’re drinking enough water. Sometimes a cold compress can help ease the pain. Have you noticed any particular triggers?
```

## Developer Information

This project was developed by [IH Efty](https://github.com/IHEfty/).

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Spacy](https://spacy.io/) for NLP capabilities.
- [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) for string matching.

## Contact

For any inquiries, please reach out to [IH Efty](mailto:youremail@example.com).
