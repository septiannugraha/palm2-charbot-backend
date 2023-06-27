# CharBot Backend - A Character-based Chatbot

This is the backend for CharBot, an AI-powered chatbot that can emulate the style and personality of various characters. This project is built with Flask and uses the PaLM2 model from OpenAI to generate responses.

## Features

- Character-based chatbot: The chatbot can emulate the style and personality of various characters.
- AI-powered: The chatbot uses the PaLM2 model from OpenAI to generate responses.
- RESTful API: The backend provides a RESTful API for the front-end application to interact with.

## Installation

To run this project, you will need to have Python and pip installed on your machine.

1. Clone the repository:
   ```bash
   git clone https://github.com/septiannugraha/palm2-charbot-backend.git
   ```
2. Navigate into the project directory:
   ```bash
   cd palm2-charbot-backend
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the development server:
   ```bash
   flask run
   ```
The API will be available at `http://localhost:5000`.

## API Endpoints

- `/detail`: POST request to get the details of a character.
- `/chat`: POST request to send a message to the chatbot and get a response.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.