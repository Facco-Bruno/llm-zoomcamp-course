from IPython.display import display, HTML
import markdown

# Utilitário para cortar argumentos longos
def shorten(text, max_length=50):
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

# Interface de texto/HTML para o chat
class ChatInterface:
    def input(self):
        question = input("You: ")
        return question

    def display(self, message):
        print(message)

    def display_function_call(self, entry, result):
        call_html = f"""
            <details>
            <summary>Function call: <tt>{entry.name}({shorten(entry.arguments)})</tt></summary>
            <div>
                <b>Call</b>
                <pre>{entry}</pre>
            </div>
            <div>
                <b>Output</b>
                <pre>{result['output']}</pre>
            </div>
            </details>
        """
        display(HTML(call_html))

    def display_response(self, entry):
        response_html = markdown.markdown(entry.content[0].text)
        html = f"""
            <div>
                <div><b>Assistant:</b></div>
                <div>{response_html}</div>
            </div>
        """
        display(HTML(html))


# Classe principal do agente de chat
class ChatAssistant:
    def __init__(self, tools, developer_prompt, chat_interface, client):
        self.tools = tools
        self.developer_prompt = developer_prompt
        self.chat_interface = chat_interface
        self.client = client

    def gpt(self, chat_messages):
        return self.client.responses.create(
            model='gpt-4o-mini',
            input=chat_messages,
            tools=self.tools.get_tools(),
        )

    def run(self):
        chat_messages = [
            {"role": "developer", "content": self.developer_prompt},
        ]

        while True:
            question = self.chat_interface.input()
            if question.strip().lower() == 'stop':
                self.chat_interface.display("Chat ended.")
                break

            user_message = {"role": "user", "content": question}
            chat_messages.append(user_message)

            while True:
                response = self.gpt(chat_messages)

                has_message = False

                for entry in response.output:
                    chat_messages.append(entry)

                    if entry.type == "function_call":
                        result = self.tools.function_call(entry)
                        chat_messages.append(result)
                        self.chat_interface.display_function_call(entry, result)

                    elif entry.type == "message":
                        self.chat_interface.display_response(entry)
                        has_message = True

                if has_message:
                    break
